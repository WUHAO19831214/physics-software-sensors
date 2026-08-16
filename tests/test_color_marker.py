from __future__ import annotations

import asyncio
import json
import math
from pathlib import Path

import cv2
import jsonschema
import numpy as np
import pytest

from physics_sensors.core import RuntimeFrame, SensorContext
from physics_sensors.tracking import ColorMarkerConfig, ColorMarkerSensor, ColorMarkerTracker


ROOT = Path(__file__).resolve().parents[1]
GOLDEN = json.loads((ROOT / "tests" / "fixtures" / "color_marker" / "golden.json").read_text(encoding="utf-8"))
EVENT_SCHEMA = json.loads((ROOT / "contracts" / "schemas" / "sensor-event.schema.json").read_text(encoding="utf-8"))
FRAME_SCHEMA = json.loads((ROOT / "contracts" / "schemas" / "frame-packet.schema.json").read_text(encoding="utf-8"))


def synthetic_frame(center: list[int] | None, radius: int = 14) -> np.ndarray:
    frame = np.zeros((120, 160, 3), dtype=np.uint8)
    if center is not None:
        cv2.circle(frame, tuple(center), radius, (0, 255, 255), -1)
    return frame


def runtime_frame(pixels: np.ndarray, sequence: int = 0) -> RuntimeFrame:
    return RuntimeFrame(
        metadata={
            "schema_version": "1.0.0",
            "frame_id": f"20000000-0000-4000-8000-{sequence:012d}",
            "run_id": "color-marker-golden",
            "source_sensor_id": "camera.capture",
            "sequence": sequence,
            "observed_at": "2026-08-16T08:00:00.000Z",
            "monotonic_ns": 1_000_000 + sequence,
            "source_timestamp": float(sequence),
            "media": {
                "kind": "camera-frame",
                "media_type": "image/raw-bgr",
                "width": pixels.shape[1],
                "height": pixels.shape[0],
                "color_space": "BGR",
                "orientation": "0",
                "mirrored": False,
            },
            "artifact": {
                "uri": f"runtime://color-marker/{sequence}",
                "media_type": "image/raw-bgr",
                "sha256": "c" * 64,
                "bytes": int(pixels.nbytes),
            },
            "quality": {"dropped_since_last": 0, "flags": []},
        },
        pixels=pixels,
    )


def assert_source_result(actual: dict, expected: dict, tolerance: float = 1e-6) -> None:
    assert actual.keys() == expected.keys()
    for key, expected_value in expected.items():
        actual_value = actual[key]
        if isinstance(expected_value, float):
            assert math.isclose(actual_value, expected_value, rel_tol=0.0, abs_tol=tolerance), key
        else:
            assert actual_value == expected_value, key


def test_golden_master_matches_fixed_source_outputs() -> None:
    config = ColorMarkerConfig(**GOLDEN["config"])
    tracker = ColorMarkerTracker(config)
    for item in GOLDEN["cases"]:
        frame_spec = item["frame"]
        result = tracker.update(synthetic_frame(frame_spec["center"], frame_spec["radius"]))
        assert_source_result(result.to_source_dict(), item["source_result"])


def test_sensor_emits_schema_valid_event_and_preserves_source_raw() -> None:
    async def run() -> dict:
        sensor = ColorMarkerSensor()
        sensor.configure(GOLDEN["config"])
        await sensor.start(SensorContext.minimal("color-marker-golden"))
        event = sensor.process_frame(runtime_frame(synthetic_frame([60, 60])))
        await sensor.stop()
        return event

    event = asyncio.run(run())
    jsonschema.Draft202012Validator(EVENT_SCHEMA, format_checker=jsonschema.FormatChecker()).validate(event)
    assert event["status"] == "ok"
    assert event["payload"]["source_raw"]["center_x"] == 60.0
    roles = {item["name"]: item["role"] for item in event["measurements"]}
    assert roles["center_x"] == "filtered"
    assert event["coordinate_frame"]["space"] == "image-pixel"


def test_runtime_metadata_is_a_schema_valid_frame_packet() -> None:
    frame = runtime_frame(synthetic_frame([60, 60]))
    jsonschema.Draft202012Validator(FRAME_SCHEMA, format_checker=jsonschema.FormatChecker()).validate(dict(frame.metadata))


def test_lost_event_has_no_measurements_or_stale_position() -> None:
    async def run() -> dict:
        sensor = ColorMarkerSensor()
        sensor.configure(GOLDEN["config"])
        await sensor.start(SensorContext.minimal("color-marker-golden"))
        sensor.process_frame(runtime_frame(synthetic_frame([60, 60]), 0))
        return sensor.process_frame(runtime_frame(synthetic_frame(None), 1))

    event = asyncio.run(run())
    assert event["status"] == "lost"
    assert event["measurements"] == []
    assert "target-lost" in event["quality"]["flags"]
    assert event["payload"]["source_raw"]["center_x"] is None


def test_unknown_configuration_is_rejected() -> None:
    sensor = ColorMarkerSensor()
    with pytest.raises(ValueError, match="unknown color marker settings"):
        sensor.configure({"ui_theme": "dark"})


def test_frame_run_id_must_match_context() -> None:
    async def run() -> None:
        sensor = ColorMarkerSensor()
        await sensor.start(SensorContext.minimal("another-run"))
        sensor.process_frame(runtime_frame(synthetic_frame([60, 60])))

    with pytest.raises(RuntimeError, match="run_id"):
        asyncio.run(run())


def test_runtime_frame_rejects_pixel_dimension_mismatch() -> None:
    frame = runtime_frame(synthetic_frame([60, 60]))
    metadata = dict(frame.metadata)
    metadata["media"] = {**metadata["media"], "width": 999}
    with pytest.raises(ValueError, match="pixel dimensions"):
        RuntimeFrame(metadata=metadata, pixels=frame.pixels)
