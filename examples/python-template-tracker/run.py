"""Run CameraSource -> ROI-initialized TemplateTrackerSensor with real OpenCV."""

from __future__ import annotations

import argparse
import asyncio
import json
import platform
from pathlib import Path

import cv2
import numpy as np

from physics_sensors.capture import BackendFrame, CameraSource, ImageSequenceCameraBackend
from physics_sensors.core import SensorContext
from physics_sensors.tracking import TemplateTrackerSensor


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "output"
ROI = (60, 90, 70, 60)


def scene(x: int | None, sequence: int) -> np.ndarray:
    image = np.full((240, 360, 3), (232, 232, 228), dtype=np.uint8)
    cv2.putText(image, "SYNTHETIC ROI TRACKER REPLAY", (18, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.67, (40, 40, 40), 2)
    cv2.line(image, (20, 180), (340, 180), (80, 80, 80), 2)
    for tick in range(40, 341, 40):
        cv2.line(image, (tick, 174), (tick, 187), (80, 80, 80), 1)
    if x is not None:
        cv2.rectangle(image, (x, 90), (x + 70, 150), (35, 45, 180), -1)
        for index in range(5):
            cv2.circle(image, (x + 10 + index * 13, 105 + (index % 2) * 25), 5, (240, 220, 30), -1)
        cv2.putText(image, "A7", (x + 15, 133), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(image, f"frame {sequence}", (278, 224), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (55, 55, 55), 1)
    return image


def titled(image: np.ndarray, title: str) -> np.ndarray:
    panel = cv2.copyMakeBorder(image, 48, 0, 0, 0, cv2.BORDER_CONSTANT, value=(248, 248, 248))
    cv2.putText(panel, title, (14, 31), cv2.FONT_HERSHEY_SIMPLEX, 0.58, (35, 35, 35), 2, cv2.LINE_AA)
    return panel


def initialization_overlay(frame: np.ndarray) -> np.ndarray:
    output = frame.copy()
    x, y, width, height = ROI
    cv2.rectangle(output, (x, y), (x + width, y + height), (20, 140, 240), 3)
    cv2.putText(output, "initialization ROI", (x, y - 9), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (20, 100, 210), 2)
    return output


def event_overlay(frame: np.ndarray, event: dict) -> np.ndarray:
    output = frame.copy()
    source = event["payload"]["source_projection"]
    color = (30, 155, 30) if source["ok"] else (20, 20, 220)
    if source["ok"]:
        p1 = (int(round(source["bbox_x1"])), int(round(source["bbox_y1"])))
        p2 = (int(round(source["bbox_x2"])), int(round(source["bbox_y2"])))
        center = (int(round(source["center_x"])), int(round(source["center_y"])))
        cv2.rectangle(output, p1, p2, color, 3)
        cv2.drawMarker(output, center, color, cv2.MARKER_CROSS, 18, 2)
    cv2.putText(output, f"{event['status']} | backend={event['payload']['tracker_backend']}", (18, 218), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return output


async def execute(output: Path) -> list[dict]:
    positions = [60, 70, 85, 100, None]
    frames = [scene(position, sequence) for sequence, position in enumerate(positions)]
    backend = ImageSequenceCameraBackend([BackendFrame(frame, 360, 240, "BGR", "image/png", source_timestamp=index / 20, observed_at=f"2026-08-16T18:00:00.{index * 50:03d}Z", monotonic_ns=10_000_000_000 + index * 50_000_000, artifact_uri=f"recorded://template-tracker/{index}.png", quality_flags=("synthetic-fixture", "recorded-replay")) for index, frame in enumerate(frames)], nominal_fps=20, device_name="synthetic-template-sequence")
    context = SensorContext.minimal("camera-to-template-tracker-demo")
    camera = CameraSource(backend)
    sensor = TemplateTrackerSensor()
    await camera.start(context)
    stream = camera.read()
    initial = await anext(stream)
    await sensor.start(context)
    if not sensor.initialize_target(initial, ROI):
        raise RuntimeError(sensor.tracker.last_error)
    events: list[dict] = []
    overlays: list[np.ndarray] = []
    async for frame in stream:
        event = sensor.process_frame(frame)
        events.append(event)
        overlays.append(event_overlay(frame.pixels, event))
    await sensor.stop()
    await camera.stop()
    output.mkdir(parents=True, exist_ok=True)
    report = {"synthetic": True, "roi": list(ROI), "opencv": cv2.__version__, "python": platform.python_version(), "platform": platform.platform(), "events": events}
    (output / "events.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    cv2.imwrite(str(output / "initialization.png"), titled(initialization_overlay(initial.pixels), "Initialization ROI (not a template image asset)"))
    cv2.imwrite(str(output / "tracking.png"), titled(overlays[1], "Actual OpenCV single-object update"))
    cv2.imwrite(str(output / "lost.png"), titled(overlays[-1], "Blank replay frame: explicit lost state"))
    cv2.imwrite(str(output / "overview.png"), cv2.hconcat([titled(initialization_overlay(initial.pixels), "1  Select ROI"), titled(overlays[1], "2  Track object"), titled(overlays[-1], "3  Emit lost")]))
    return events


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    events = asyncio.run(execute(args.output))
    print(f"wrote {len(events)} CameraSource -> TemplateTrackerSensor events to {args.output}")
    print("statuses:", ", ".join(event["status"] for event in events))
    print("backend:", events[0]["payload"]["tracker_backend"])


if __name__ == "__main__":
    main()
