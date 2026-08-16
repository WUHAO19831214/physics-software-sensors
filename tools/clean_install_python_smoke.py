"""Smoke test intended to run outside the repository against an installed wheel."""

from __future__ import annotations

import asyncio

import cv2
import numpy as np

from physics_sensors.core import SensorContext
from physics_sensors.capture import BackendFrame, CameraSource, ImageSequenceCameraBackend
from physics_sensors.tracking import (
    ColorMarkerSensor,
    RecordedDetectorBackend,
    SpotCentroidSensor,
    TemplateTrackerSensor,
    YoloTrackerSensor,
)


async def main() -> None:
    pixels = np.zeros((160, 240, 3), dtype=np.uint8)
    cv2.circle(pixels, (185, 50), 14, (0, 255, 255), -1)
    cv2.circle(pixels, (190, 120), 10, (0, 0, 245), -1)
    cv2.rectangle(pixels, (40, 55), (105, 115), (35, 45, 180), -1)
    cv2.putText(pixels, "A7", (52, 92), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    updated = pixels.copy()
    camera = CameraSource(
        ImageSequenceCameraBackend([
            BackendFrame(
                pixels=pixels,
                width=240,
                height=160,
                color_space="BGR",
                media_type="application/x-raw-bgr",
                observed_at="2026-08-16T12:00:00.000Z",
                monotonic_ns=1,
                quality_flags=("synthetic-fixture",),
            ),
            BackendFrame(
                pixels=updated,
                width=240,
                height=160,
                color_space="BGR",
                media_type="application/x-raw-bgr",
                observed_at="2026-08-16T12:00:00.050Z",
                monotonic_ns=50_000_001,
                quality_flags=("synthetic-fixture",),
            ),
        ])
    )
    await camera.start(SensorContext.minimal("clean-wheel-smoke"))
    stream = camera.read()
    captured = await anext(stream)
    next_frame = await anext(stream)
    context = SensorContext.minimal("clean-wheel-smoke")

    color = ColorMarkerSensor()
    await color.start(context)
    color_event = color.process_frame(captured)
    await color.stop()

    spot = SpotCentroidSensor()
    await spot.start(context)
    spot_event = spot.process_frame(captured)
    await spot.stop()

    template = TemplateTrackerSensor()
    await template.start(context)
    assert template.initialize_target(captured, (40, 55, 65, 60))
    template_event = template.process_frame(next_frame)
    await template.stop()

    yolo = YoloTrackerSensor(RecordedDetectorBackend([{
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
    }]))
    await yolo.start(context)
    yolo_event = yolo.process_frame(captured)
    await yolo.stop()
    await camera.stop()

    assert color_event["status"] == "ok" and color_event["sensor"]["id"] == "tracker.color-marker"
    assert spot_event["status"] == "ok" and spot_event["sensor"]["id"] == "tracker.spot-centroid"
    assert template_event["status"] == "ok" and template_event["sensor"]["id"] == "tracker.template"
    assert yolo_event["status"] == "ok" and yolo_event["sensor"]["id"] == "tracker.yolo"
    assert yolo_event["payload"]["detections"][0]["track_id"] == 7
    print("PASS clean wheel CameraSource -> ColorMarker/SpotCentroid/TemplateTracker/YoloTracker compositions")


if __name__ == "__main__":
    asyncio.run(main())
