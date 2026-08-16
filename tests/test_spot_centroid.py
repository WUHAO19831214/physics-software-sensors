from __future__ import annotations

import asyncio
import json
import math
from pathlib import Path

import cv2
import jsonschema
import numpy as np

from physics_sensors.capture import BackendFrame, CameraSource, ImageSequenceCameraBackend
from physics_sensors.core import RuntimeFrame, SensorContext
from physics_sensors.tracking import SpotCentroidSensor, SpotCentroidTracker


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "examples" / "spot-centroid" / "sample"
GOLDEN = json.loads((ROOT / "tests" / "fixtures" / "spot_centroid" / "golden.json").read_text(encoding="utf-8"))
EVENT_SCHEMA = json.loads((ROOT / "contracts" / "schemas" / "sensor-event.schema.json").read_text(encoding="utf-8"))


def packet(pixels: np.ndarray, sequence: int = 0, run_id: str = "spot-centroid-test") -> RuntimeFrame:
    return RuntimeFrame(metadata={
        "schema_version": "1.0.0", "frame_id": f"91000000-0000-4000-8000-{sequence:012d}",
        "run_id": run_id, "source_sensor_id": "camera.capture", "sequence": sequence,
        "observed_at": f"2026-08-16T15:00:{sequence:02d}.000Z", "monotonic_ns": 7_000_000_000 + sequence,
        "source_timestamp": float(sequence),
        "media": {"kind": "camera-frame", "media_type": "application/x-raw-bgr", "width": pixels.shape[1], "height": pixels.shape[0], "color_space": "BGR", "orientation": "0", "mirrored": False},
        "artifact": {"uri": f"recorded://spot/{sequence}", "media_type": "image/png", "sha256": "9" * 64, "bytes": int(pixels.nbytes)},
        "quality": {"dropped_since_last": 0, "flags": ["synthetic-fixture"]},
    }, pixels=pixels)


def test_python_tracker_matches_js_source_harness_golden() -> None:
    tracker = SpotCentroidTracker()
    for case in GOLDEN["cases"]:
        pixels = cv2.imread(str(SAMPLE / case["file"]))
        result = tracker.update(pixels).source_projection()
        expected = case["source_result"]
        assert result["locked"] is expected["locked"], case["id"]
        for field in ("x", "y", "radius", "weight_sum"):
            if expected[field] is None:
                assert result[field] is None, (case["id"], field)
            else:
                assert math.isclose(result[field], expected[field], rel_tol=0, abs_tol=GOLDEN["tolerance_px"]), (case["id"], field)


def test_sensor_event_is_schema_valid_and_only_reports_image_pixels() -> None:
    async def run():
        sensor = SpotCentroidSensor()
        await sensor.start(SensorContext.minimal("spot-centroid-test"))
        event = sensor.process_frame(packet(cv2.imread(str(SAMPLE / "bright.png"))))
        await sensor.stop()
        return event

    event = asyncio.run(run())
    jsonschema.Draft202012Validator(EVENT_SCHEMA, format_checker=jsonschema.FormatChecker()).validate(event)
    assert event["status"] == "ok"
    values = {item["name"]: item for item in event["measurements"]}
    assert values["centroid_x"]["value"] == 80
    assert values["centroid_y"]["unit"] == "px"
    assert "displacement" not in values and "amplitude" not in values
    assert event["quality"]["confidence"] is None
    assert event["coordinate_frame"]["calibration_id"] is None


def test_blank_and_low_signal_do_not_reuse_stale_centroid() -> None:
    async def run():
        sensor = SpotCentroidSensor()
        await sensor.start(SensorContext.minimal("spot-centroid-test"))
        sensor.process_frame(packet(cv2.imread(str(SAMPLE / "bright.png")), 0))
        blank = sensor.process_frame(packet(cv2.imread(str(SAMPLE / "blank.png")), 1))
        return blank

    event = asyncio.run(run())
    assert event["status"] == "lost"
    assert event["measurements"] == []
    assert "spot-lost" in event["quality"]["flags"]
    assert event["payload"]["source_projection"]["x"] is None


def test_low_signal_and_overexposure_flags_are_evidence_based() -> None:
    async def run():
        pixels = np.full((80, 100, 3), 15, dtype=np.uint8)
        cv2.circle(pixels, (50, 40), 2, (0, 0, 255), -1)
        low = SpotCentroidSensor()
        low.configure({"lost_weight_threshold": 100000})
        await low.start(SensorContext.minimal("spot-centroid-test"))
        low_event = low.process_frame(packet(pixels))
        hot = SpotCentroidSensor()
        hot.configure({"overexposure_fraction": 0.2})
        await hot.start(SensorContext.minimal("spot-centroid-test"))
        hot_event = hot.process_frame(packet(pixels))
        return low_event, hot_event

    low_event, hot_event = asyncio.run(run())
    assert {"spot-lost", "low-signal"}.issubset(low_event["quality"]["flags"])
    assert "overexposed" in hot_event["quality"]["flags"]


def test_roi_edge_flag_uses_configured_roi_not_whole_frame_guess() -> None:
    async def run():
        sensor = SpotCentroidSensor()
        sensor.configure({"roi": {"x": 0.0125, "y": 0, "width": 0.9875, "height": 1}})
        await sensor.start(SensorContext.minimal("spot-centroid-test"))
        return sensor.process_frame(packet(cv2.imread(str(SAMPLE / "roi-edge.png"))))

    event = asyncio.run(run())
    assert event["status"] == "ok"
    assert "roi-edge" in event["quality"]["flags"]


def test_camera_source_composes_directly_with_spot_centroid_sensor() -> None:
    async def run():
        pixels = cv2.imread(str(SAMPLE / "horizontal.png"))
        camera = CameraSource(ImageSequenceCameraBackend([BackendFrame(pixels, 160, 120, "BGR", "image/png", observed_at="2026-08-16T15:00:00.000Z", monotonic_ns=1, quality_flags=("synthetic-fixture",))]))
        await camera.start(SensorContext.minimal("camera-to-spot"))
        frame = await anext(camera.read())
        sensor = SpotCentroidSensor()
        await sensor.start(SensorContext.minimal("camera-to-spot"))
        event = sensor.process_frame(frame)
        await sensor.stop(); await camera.stop()
        return event

    event = asyncio.run(run())
    assert event["status"] == "ok"
    values = {item["name"]: item["value"] for item in event["measurements"]}
    assert values["centroid_x"] == 112


def test_non_red_generalization_is_rejected_in_source_compatible_version() -> None:
    sensor = SpotCentroidSensor()
    try:
        sensor.configure({"color_channel": "green"})
    except ValueError as exc:
        assert "only color_channel='red'" in str(exc)
    else:
        raise AssertionError("unsupported generalization must be rejected")
