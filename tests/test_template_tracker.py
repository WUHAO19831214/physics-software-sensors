from __future__ import annotations

import asyncio
import json
import math
from pathlib import Path
from typing import Any

import jsonschema
import numpy as np
import pytest

from physics_sensors.capture import BackendFrame, CameraSource, ImageSequenceCameraBackend
from physics_sensors.core import RuntimeFrame, SensorContext
from physics_sensors.tracking import TemplateTracker, TemplateTrackerSensor


ROOT = Path(__file__).resolve().parents[1]
GOLDEN = json.loads((ROOT / "tests" / "fixtures" / "template_tracker" / "golden.json").read_text(encoding="utf-8"))
EVENT_SCHEMA = json.loads((ROOT / "contracts" / "schemas" / "sensor-event.schema.json").read_text(encoding="utf-8"))


class ScriptedTracker:
    def __init__(self, initialize: bool | None, updates: list[Any]) -> None:
        self.initialize_result = initialize
        self.updates = iter(updates)

    def init(self, frame: np.ndarray, bbox: tuple[int, int, int, int]):
        self.initialization_bbox = bbox
        return self.initialize_result

    def update(self, frame: np.ndarray):
        result = next(self.updates)
        if isinstance(result, BaseException):
            raise result
        return result


def packet(pixels: np.ndarray, sequence: int = 0, run_id: str = "template-golden") -> RuntimeFrame:
    return RuntimeFrame(metadata={
        "schema_version": "1.0.0", "frame_id": f"92000000-0000-4000-8000-{sequence:012d}",
        "run_id": run_id, "source_sensor_id": "camera.capture", "sequence": sequence,
        "observed_at": f"2026-08-16T16:00:{sequence:02d}.000Z", "monotonic_ns": 8_000_000_000 + sequence,
        "source_timestamp": float(sequence),
        "media": {"kind": "camera-frame", "media_type": "application/x-raw-bgr", "width": pixels.shape[1], "height": pixels.shape[0], "color_space": "BGR", "orientation": "0", "mirrored": False},
        "artifact": {"uri": f"recorded://template/{sequence}", "media_type": "image/png", "sha256": "8" * 64, "bytes": int(pixels.nbytes)},
        "quality": {"dropped_since_last": 0, "flags": ["synthetic-fixture"]},
    }, pixels=pixels)


def comparable(result: dict[str, Any]) -> dict[str, Any]:
    """Compare stable source fields; diagnostic error prose is intentionally localized."""
    return {key: value for key, value in result.items() if key != "error"}


def assert_source_projection(actual: dict[str, Any], expected: dict[str, Any], tolerance: float = 1e-9) -> None:
    actual = comparable(actual)
    expected = comparable(expected)
    assert actual.keys() == expected.keys()
    for key, expected_value in expected.items():
        actual_value = actual[key]
        if isinstance(expected_value, float):
            assert math.isclose(actual_value, expected_value, rel_tol=0, abs_tol=tolerance), key
        else:
            assert actual_value == expected_value, key


def test_source_executed_golden_covers_fallback_move_lost_failure_and_reinitialize() -> None:
    frame = np.zeros((120, 180, 3), dtype=np.uint8)
    calls: list[str] = []

    def fallback_factory(backend: str):
        calls.append(backend)
        if backend == "CSRT":
            raise RuntimeError("scripted unavailable")
        if backend == "KCF":
            return ScriptedTracker(False, [])
        return ScriptedTracker(True, [(True, (12.0, 22.0, 40.0, 30.0)), (False, None), RuntimeError("scripted update failure")])

    tracker = TemplateTracker("CSRT", fallback_factory)
    assert tracker.initialize(frame, (10.2, 20.4, 40.1, 30.3))
    results = [tracker.last_result, tracker.update(frame), tracker.update(frame), tracker.update(frame)]
    for result, expected in zip(results, GOLDEN["cases"][:4], strict=True):
        assert_source_projection(result.source_projection(), expected["result"])
        assert tracker.requested_tracker_type == "CSRT"
    assert calls == ["CSRT", "KCF", "MIL"]
    assert tracker.actual_tracker_type == "MIL"
    assert tracker.fallback_used is True
    assert tracker.lost_frame_count == 2

    def reinitialize_factory(backend: str):
        calls.append(backend)
        return ScriptedTracker(True, [(True, (31.0, 41.0, 24.0, 18.0))])

    tracker.tracker_factory = reinitialize_factory
    assert tracker.initialize(frame, (30, 40, 24, 18))
    assert_source_projection(tracker.last_result.source_projection(), GOLDEN["cases"][4]["result"])
    assert_source_projection(tracker.update(frame).source_projection(), GOLDEN["cases"][5]["result"])
    assert tracker.lost_frame_count == 0


def test_all_backends_unavailable_matches_source_state_and_order() -> None:
    calls: list[str] = []

    def unavailable(backend: str):
        calls.append(backend)
        raise RuntimeError(f"{backend} unavailable")

    tracker = TemplateTracker("CSRT", unavailable)
    assert tracker.initialize(np.zeros((120, 180, 3), dtype=np.uint8), (10, 10, 20, 20)) is False
    expected = GOLDEN["cases"][6]
    assert_source_projection(tracker.last_result.source_projection(), expected["result"])
    assert calls == GOLDEN["script"]["fallback_order"]
    assert tracker.actual_tracker_type is None
    assert tracker.last_error


def test_sensor_event_records_backend_fallback_and_no_invented_confidence() -> None:
    frame = np.zeros((120, 180, 3), dtype=np.uint8)

    def factory(backend: str):
        if backend != "MIL":
            raise RuntimeError("unavailable")
        return ScriptedTracker(True, [(True, (14.0, 24.0, 40.0, 30.0))])

    async def run():
        sensor = TemplateTrackerSensor(tracker_factory=factory)
        await sensor.start(SensorContext.minimal("template-golden"))
        assert sensor.initialize_target(packet(frame, 0), (10, 20, 40, 30))
        event = sensor.process_frame(packet(frame, 1))
        await sensor.stop()
        return event

    event = asyncio.run(run())
    jsonschema.Draft202012Validator(EVENT_SCHEMA, format_checker=jsonschema.FormatChecker()).validate(event)
    assert event["status"] == "ok"
    assert event["quality"]["confidence"] is None
    assert "tracker-backend-fallback" in event["quality"]["flags"]
    assert event["payload"]["requested_backend"] == "CSRT"
    assert event["payload"]["tracker_backend"] == "MIL"
    assert event["payload"]["attempted_backends"] == ["CSRT", "KCF", "MIL"]
    assert event["payload"]["confidence_available"] is False


def test_initialization_roi_is_distinct_from_template_asset_metadata() -> None:
    sensor = TemplateTrackerSensor(tracker_factory=lambda backend: ScriptedTracker(True, []))
    result = sensor.configure({"tracker_type": "KCF", "template_asset_uri": "artifact://reference.png"})
    assert result.effective_config["template_asset_uri"] == "artifact://reference.png"
    assert result.warnings and "does not perform static template matching" in result.warnings[0]


def test_camera_source_composes_directly_with_template_sensor() -> None:
    pixels = np.zeros((120, 180, 3), dtype=np.uint8)
    frames = [BackendFrame(pixels.copy(), 180, 120, "BGR", "image/png", observed_at=f"2026-08-16T16:00:0{i}.000Z", monotonic_ns=i + 1, quality_flags=("synthetic-fixture",)) for i in range(2)]

    async def run():
        camera = CameraSource(ImageSequenceCameraBackend(frames))
        sensor = TemplateTrackerSensor(tracker_factory=lambda backend: ScriptedTracker(True, [(True, (22, 32, 36, 28))]))
        context = SensorContext.minimal("camera-to-template")
        await camera.start(context)
        stream = camera.read()
        initialization_frame = await anext(stream)
        update_frame = await anext(stream)
        await sensor.start(context)
        assert sensor.initialize_target(initialization_frame, (20, 30, 36, 28))
        event = sensor.process_frame(update_frame)
        await sensor.stop(); await camera.stop()
        return event

    event = asyncio.run(run())
    assert event["status"] == "ok"
    measurements = {item["name"]: item["value"] for item in event["measurements"]}
    assert measurements["center_x"] == 40
    assert measurements["center_y"] == 46
    assert len(event["parent_event_ids"]) == 2
    assert event["parent_event_ids"][0] != event["parent_event_ids"][1]


def test_lost_event_has_no_stale_bbox_measurements() -> None:
    pixels = np.zeros((120, 180, 3), dtype=np.uint8)

    async def run():
        sensor = TemplateTrackerSensor(tracker_factory=lambda backend: ScriptedTracker(True, [(False, None)]))
        await sensor.start(SensorContext.minimal("template-golden"))
        assert sensor.initialize_target(packet(pixels), (20, 30, 36, 28))
        return sensor.process_frame(packet(pixels, 1))

    event = asyncio.run(run())
    assert event["status"] == "lost"
    assert event["measurements"] == []
    assert "target-lost" in event["quality"]["flags"]
    assert event["payload"]["source_projection"]["center_x"] is None


def test_actual_opencv_contrib_replay_tracks_then_reports_blank_lost() -> None:
    cv2 = pytest.importorskip("cv2")

    def scene(x: int | None) -> np.ndarray:
        image = np.full((240, 360, 3), 232, dtype=np.uint8)
        cv2.line(image, (20, 180), (340, 180), (80, 80, 80), 2)
        if x is not None:
            cv2.rectangle(image, (x, 90), (x + 70, 150), (35, 45, 180), -1)
            for index in range(5):
                cv2.circle(image, (x + 10 + index * 13, 105 + (index % 2) * 25), 5, (240, 220, 30), -1)
            cv2.putText(image, "A7", (x + 15, 133), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        return image

    tracker = TemplateTracker("CSRT")
    if not tracker.initialize(scene(60), (60, 90, 70, 60)):
        pytest.skip(f"no classical OpenCV tracker in {cv2.__version__}: {tracker.last_error}")
    results = [tracker.update(scene(x)) for x in (70, 85, 100, None)]
    assert tracker.actual_tracker_type in ("CSRT", "KCF", "MIL")
    assert [result.ok for result in results] == [True, True, True, False]
    assert max(abs(result.center_y - 120) for result in results[:3]) <= 1
