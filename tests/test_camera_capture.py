from __future__ import annotations

import asyncio
import json
from pathlib import Path

import jsonschema
import numpy as np
import pytest

from physics_sensors.capture import (
    BackendFrame,
    CameraConfig,
    CameraSource,
    ImageSequenceCameraBackend,
    OpenCVCameraBackend,
)
from physics_sensors.core import SensorContext


ROOT = Path(__file__).resolve().parents[1]
FRAME_SCHEMA = json.loads(
    (ROOT / "contracts" / "schemas" / "frame-packet.schema.json").read_text(encoding="utf-8")
)


def recorded_frames() -> list[BackendFrame]:
    return [
        BackendFrame(
            pixels=np.full((2, 3, 3), value, dtype=np.uint8),
            width=3,
            height=2,
            color_space="BGR",
            media_type="application/x-raw-bgr",
            source_timestamp=sequence / 20,
            observed_at=f"2026-08-16T12:00:00.{sequence * 50:03d}Z",
            monotonic_ns=1_000_000_000 + sequence * 50_000_000,
            dropped_since_last=1 if sequence == 1 else 0,
            quality_flags=("recorded-replay",),
            artifact_uri=f"recorded://camera/frame-{sequence}",
        )
        for sequence, value in enumerate((0, 64, 128))
    ]


async def capture_all(source: CameraSource) -> list:
    source.configure({"width": 1920, "height": 1080, "requested_fps": 30})
    await source.start(SensorContext.minimal("camera-replay"))
    frames = [frame async for frame in source.read()]
    await source.stop()
    return frames


def test_image_sequence_emits_schema_valid_runtime_frames() -> None:
    source = CameraSource(
        ImageSequenceCameraBackend(recorded_frames(), nominal_fps=20),
        frame_id_factory=iter(
            [
                "81000000-0000-4000-8000-000000000001",
                "81000000-0000-4000-8000-000000000002",
                "81000000-0000-4000-8000-000000000003",
            ]
        ).__next__,
    )
    frames = asyncio.run(capture_all(source))
    validator = jsonschema.Draft202012Validator(
        FRAME_SCHEMA, format_checker=jsonschema.FormatChecker()
    )
    assert len(frames) == 3
    for frame in frames:
        validator.validate(dict(frame.metadata))
        assert frame.metadata["source_sensor_id"] == "camera.capture"
        assert frame.pixels.shape == (2, 3, 3)


def test_requested_nominal_and_measured_rates_are_not_conflated() -> None:
    source = CameraSource(ImageSequenceCameraBackend(recorded_frames(), nominal_fps=20))
    frames = asyncio.run(capture_all(source))
    capture = frames[1].metadata["payload"]["capture"]
    assert capture["requested"]["fps"] == 30
    assert capture["actual"]["nominal_fps"] == 20
    assert capture["actual"]["measured_fps"] == pytest.approx(20)
    assert source.health().actual_rate_hz == pytest.approx(20)


def test_dropped_frame_information_is_preserved() -> None:
    source = CameraSource(ImageSequenceCameraBackend(recorded_frames(), nominal_fps=20))
    frames = asyncio.run(capture_all(source))
    assert frames[1].metadata["quality"] == {
        "dropped_since_last": 1,
        "flags": ["recorded-replay", "frame-dropped"],
    }
    assert source.health().dropped_count == 1


def test_camera_source_is_finite_and_stop_is_idempotent() -> None:
    async def run() -> None:
        source = CameraSource(ImageSequenceCameraBackend(recorded_frames()))
        await source.start(SensorContext.minimal("camera-replay"))
        assert len([frame async for frame in source.read()]) == 3
        await source.stop()
        await source.stop()
        assert source.health().state == "stopped"

    asyncio.run(run())


def test_unknown_camera_configuration_is_rejected() -> None:
    source = CameraSource(ImageSequenceCameraBackend([]))
    with pytest.raises(ValueError, match="unknown camera settings"):
        source.configure({"classroom_store": True})


def test_opencv_backend_is_public_without_opening_hardware() -> None:
    backend = OpenCVCameraBackend(device_index=7)
    assert backend.backend_id == "opencv"
    assert backend.device_index == 7


def test_opencv_backend_counts_recovered_failed_reads_as_drops() -> None:
    class FakeCapture:
        def __init__(self) -> None:
            self.reads = iter([(False, None), (False, None), (True, np.zeros((2, 3, 3), dtype=np.uint8))])

        def isOpened(self): return True
        def set(self, _key, _value): return True
        def get(self, _key): return 0
        def getBackendName(self): return "FAKE"
        def read(self): return next(self.reads)
        def release(self): pass

    capture = FakeCapture()
    backend = OpenCVCameraBackend(
        capture_factory=lambda _index: capture,
        max_consecutive_failures=3,
        retry_delay_s=0,
    )
    backend.start(CameraConfig())
    frame = backend.read()
    backend.stop()
    assert frame.dropped_since_last == 2
