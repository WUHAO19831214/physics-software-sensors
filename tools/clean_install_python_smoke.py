"""Smoke test intended to run outside the repository against an installed wheel."""

from __future__ import annotations

import asyncio

import cv2
import numpy as np

from physics_sensors.core import RuntimeFrame, SensorContext
from physics_sensors.tracking import ColorMarkerSensor


async def main() -> None:
    pixels = np.zeros((100, 140, 3), dtype=np.uint8)
    cv2.circle(pixels, (70, 50), 14, (0, 255, 255), -1)
    metadata = {
        "schema_version": "1.0.0",
        "frame_id": "60000000-0000-4000-8000-000000000001",
        "run_id": "clean-wheel-smoke",
        "source_sensor_id": "camera.capture",
        "sequence": 0,
        "observed_at": "2026-08-16T12:00:00.000Z",
        "monotonic_ns": 1,
        "source_timestamp": 0,
        "media": {
            "kind": "image-frame",
            "media_type": "image/raw-bgr",
            "width": 140,
            "height": 100,
            "color_space": "BGR",
            "orientation": "0",
            "mirrored": False,
        },
        "artifact": {
            "uri": "runtime://clean-wheel-smoke/frame.png",
            "media_type": "image/png",
            "sha256": "6" * 64,
            "bytes": int(pixels.nbytes),
        },
        "quality": {"dropped_since_last": 0, "flags": ["synthetic-fixture"]},
    }
    sensor = ColorMarkerSensor()
    await sensor.start(SensorContext.minimal("clean-wheel-smoke"))
    event = sensor.process_frame(RuntimeFrame(metadata=metadata, pixels=pixels))
    await sensor.stop()
    assert event["status"] == "ok"
    assert event["sensor"]["id"] == "tracker.color-marker"
    print("PASS clean wheel import and ColorMarkerSensor processing")


if __name__ == "__main__":
    asyncio.run(main())
