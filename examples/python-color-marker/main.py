"""Minimal UI-free ColorMarkerSensor example using one synthetic frame."""

from __future__ import annotations

import asyncio

import cv2
import numpy as np

from physics_sensors.core import RuntimeFrame, SensorContext
from physics_sensors.tracking import ColorMarkerSensor


async def main() -> None:
    pixels = np.zeros((120, 160, 3), dtype=np.uint8)
    cv2.circle(pixels, (80, 60), 14, (0, 255, 255), -1)
    packet = {
        "schema_version": "1.0.0",
        "frame_id": "30000000-0000-4000-8000-000000000001",
        "run_id": "minimal-color-marker",
        "source_sensor_id": "camera.capture",
        "sequence": 0,
        "observed_at": "2026-08-16T08:00:00.000Z",
        "monotonic_ns": 1_000_000,
        "source_timestamp": 0,
        "media": {
            "kind": "image-frame",
            "media_type": "image/raw-bgr",
            "width": 160,
            "height": 120,
            "color_space": "BGR",
            "orientation": "0",
            "mirrored": False,
        },
        "artifact": {
            "uri": "runtime://minimal-color-marker/frame-0",
            "media_type": "image/raw-bgr",
            "sha256": "d" * 64,
            "bytes": int(pixels.nbytes),
        },
        "quality": {"dropped_since_last": 0, "flags": []},
    }
    sensor = ColorMarkerSensor()
    sensor.configure({"hsv_lower": [20, 100, 100], "hsv_upper": [40, 255, 255]})
    await sensor.start(SensorContext.minimal("minimal-color-marker"))
    event = sensor.process_frame(RuntimeFrame(metadata=packet, pixels=pixels))
    print(event)
    await sensor.stop()


if __name__ == "__main__":
    asyncio.run(main())
