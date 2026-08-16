from __future__ import annotations

import asyncio

import cv2
import numpy as np

from physics_sensors.capture import BackendFrame, CameraSource, ImageSequenceCameraBackend
from physics_sensors.core import SensorContext
from physics_sensors.tracking import (
    ColorMarkerSensor,
    RecordedDetectorBackend,
    SpotCentroidSensor,
    TemplateTrackerSensor,
    YoloTrackerSensor,
)


def backend_frame(pixels: np.ndarray, sequence: int = 0) -> BackendFrame:
    return BackendFrame(
        pixels,
        pixels.shape[1],
        pixels.shape[0],
        "BGR",
        "application/x-raw-bgr",
        observed_at=f"2026-08-16T21:00:0{sequence}.000Z",
        monotonic_ns=13_000_000_000 + sequence,
        quality_flags=("synthetic-fixture",),
    )


async def capture_one(pixels: np.ndarray, run_id: str):
    source = CameraSource(ImageSequenceCameraBackend([backend_frame(pixels)]))
    await source.start(SensorContext.minimal(run_id))
    frame = await anext(source.read())
    return source, frame


def test_camera_to_color_marker() -> None:
    async def run():
        pixels = np.zeros((160, 240, 3), dtype=np.uint8)
        cv2.circle(pixels, (185, 50), 14, (0, 255, 255), -1)
        source, frame = await capture_one(pixels, "composition-camera-color")
        sensor = ColorMarkerSensor()
        await sensor.start(SensorContext.minimal("composition-camera-color"))
        event = sensor.process_frame(frame)
        await sensor.stop()
        await source.stop()
        return event

    event = asyncio.run(run())
    assert event["status"] == "ok"
    assert event["sensor"]["id"] == "tracker.color-marker"
    assert event["parent_event_ids"]


def test_camera_to_spot_centroid() -> None:
    async def run():
        pixels = np.zeros((160, 240, 3), dtype=np.uint8)
        cv2.circle(pixels, (190, 120), 10, (0, 0, 245), -1)
        source, frame = await capture_one(pixels, "composition-camera-spot")
        sensor = SpotCentroidSensor()
        await sensor.start(SensorContext.minimal("composition-camera-spot"))
        event = sensor.process_frame(frame)
        await sensor.stop()
        await source.stop()
        return event

    event = asyncio.run(run())
    assert event["status"] == "ok"
    assert event["sensor"]["id"] == "tracker.spot-centroid"


def textured_scene() -> np.ndarray:
    pixels = np.full((160, 240, 3), 225, dtype=np.uint8)
    cv2.rectangle(pixels, (40, 55), (105, 115), (35, 45, 180), -1)
    cv2.putText(pixels, "A7", (52, 92), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    for index in range(5):
        cv2.circle(pixels, (48 + index * 12, 105), 3, (20, 220, 220), -1)
    return pixels


def test_camera_to_template_tracker() -> None:
    async def run():
        pixels = textured_scene()
        source = CameraSource(
            ImageSequenceCameraBackend([backend_frame(pixels, 0), backend_frame(pixels.copy(), 1)])
        )
        context = SensorContext.minimal("composition-camera-template")
        await source.start(context)
        stream = source.read()
        initial = await anext(stream)
        update = await anext(stream)
        sensor = TemplateTrackerSensor()
        await sensor.start(context)
        assert sensor.initialize_target(initial, (40, 55, 65, 60))
        event = sensor.process_frame(update)
        await sensor.stop()
        await source.stop()
        return event

    event = asyncio.run(run())
    assert event["status"] == "ok"
    assert event["sensor"]["id"] == "tracker.template"
    assert event["payload"]["tracker_backend"] in {"CSRT", "KCF", "MIL"}


def test_camera_to_yolo_tracker() -> None:
    async def run():
        pixels = np.zeros((160, 240, 3), dtype=np.uint8)
        source, frame = await capture_one(pixels, "composition-camera-yolo")
        backend = RecordedDetectorBackend(
            [{
                "requested_backend": "recorded-detector",
                "actual_backend": "recorded-detector",
                "attempted_backends": ["recorded-detector"],
                "tracking_mode": "recorded-tracks",
                "detections": [{
                    "track_id": 7,
                    "tracking_id_available": True,
                    "class_id": 0,
                    "class_name": "person",
                    "bbox": {"x": 40, "y": 20, "width": 65, "height": 95},
                    "detector_confidence": 0.91,
                }],
            }]
        )
        sensor = YoloTrackerSensor(backend)
        await sensor.start(SensorContext.minimal("composition-camera-yolo"))
        event = sensor.process_frame(frame)
        await sensor.stop()
        await source.stop()
        return event

    event = asyncio.run(run())
    assert event["status"] == "ok"
    assert event["sensor"]["id"] == "tracker.yolo"
    assert event["payload"]["detections"][0]["track_id"] == 7
