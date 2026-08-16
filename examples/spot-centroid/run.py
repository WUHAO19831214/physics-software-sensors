"""Run CameraSource -> SpotCentroidSensor and generate synthetic demo evidence."""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

import cv2
import numpy as np

from physics_sensors.capture import BackendFrame, CameraSource, ImageSequenceCameraBackend
from physics_sensors.core import SensorContext
from physics_sensors.tracking import SpotCentroidSensor


HERE = Path(__file__).resolve().parent
SAMPLE = HERE / "sample"
OUTPUT = HERE / "output"


def titled(image: np.ndarray, title: str) -> np.ndarray:
    enlarged = cv2.resize(image, (480, 360), interpolation=cv2.INTER_NEAREST)
    panel = cv2.copyMakeBorder(enlarged, 58, 0, 0, 0, cv2.BORDER_CONSTANT, value=(248, 248, 248))
    cv2.putText(panel, title, (18, 36), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (35, 35, 35), 2, cv2.LINE_AA)
    return panel


def annotate(frame: np.ndarray, event: dict) -> np.ndarray:
    output = frame.copy()
    source = event["payload"]["source_projection"]
    if source["locked"]:
        center = (int(round(source["x"])), int(round(source["y"])))
        cv2.circle(output, center, int(round(source["radius"])), (0, 220, 40), 2, cv2.LINE_AA)
        cv2.drawMarker(output, center, (255, 230, 50), cv2.MARKER_CROSS, 18, 2)
        cv2.putText(output, f"centroid=({source['x']:.0f},{source['y']:.0f})px", (5, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.34, (240, 240, 240), 1, cv2.LINE_AA)
    cv2.putText(output, f"status: {event['status']}", (7, 112), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (80, 230, 80) if event["status"] == "ok" else (70, 70, 235), 1, cv2.LINE_AA)
    return output


async def execute(output: Path) -> list[dict]:
    filenames = ["bright.png", "horizontal.png", "vertical.png", "dim.png", "blank.png", "roi-edge.png"]
    pixels = [cv2.imread(str(SAMPLE / name)) for name in filenames]
    backend_frames = [BackendFrame(image, image.shape[1], image.shape[0], "BGR", "image/png", source_timestamp=index / 20, observed_at=f"2026-08-16T17:00:00.{index * 50:03d}Z", monotonic_ns=9_000_000_000 + index * 50_000_000, artifact_uri=f"recorded://spot-centroid/{name}", quality_flags=("synthetic-fixture", "recorded-replay")) for index, (name, image) in enumerate(zip(filenames, pixels, strict=True))]
    context = SensorContext.minimal("camera-to-spot-centroid-demo")
    camera = CameraSource(ImageSequenceCameraBackend(backend_frames, nominal_fps=20, device_name="synthetic-spot-sequence"))
    sensor = SpotCentroidSensor()
    await camera.start(context)
    await sensor.start(context)
    events: list[dict] = []
    masks: list[np.ndarray] = []
    overlays: list[np.ndarray] = []
    async for frame in camera.read():
        event = sensor.process_frame(frame)
        events.append(event)
        masks.append(sensor.tracker.last_mask.copy())
        overlays.append(annotate(frame.pixels, event))
    await sensor.stop()
    await camera.stop()

    output.mkdir(parents=True, exist_ok=True)
    (output / "events.json").write_text(json.dumps(events, ensure_ascii=False, indent=2), encoding="utf-8")
    cv2.imwrite(str(output / "overview.png"), titled(overlays[0], "Synthetic replay: image-space centroid only"))
    weighted = cv2.applyColorMap(masks[0], cv2.COLORMAP_INFERNO)
    cv2.imwrite(str(output / "processing.png"), cv2.hconcat([titled(pixels[0], "1  Original BGR frame"), titled(weighted, "2  Accepted weighted pixels"), titled(overlays[0], "3  SpotCentroid SensorEvent")]))
    cv2.imwrite(str(output / "movement.png"), cv2.hconcat([titled(overlays[0], "Frame 0: initial centroid"), titled(overlays[1], "Frame 1: horizontal movement"), titled(overlays[2], "Frame 2: vertical movement")]))
    return events


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    events = asyncio.run(execute(args.output))
    print(f"wrote {len(events)} CameraSource -> SpotCentroidSensor events to {args.output}")
    print("statuses:", ", ".join(event["status"] for event in events))


if __name__ == "__main__":
    main()
