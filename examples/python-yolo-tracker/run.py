"""Run CameraSource -> YoloTrackerSensor with offline recorded or explicit local YOLO backend."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import importlib.metadata
import json
from pathlib import Path

import cv2
import numpy as np

from physics_sensors.capture import BackendFrame, CameraSource, ImageSequenceCameraBackend
from physics_sensors.core import ModelArtifact, SensorContext
from physics_sensors.tracking import RecordedDetectorBackend, YoloDetectorBackend, YoloTrackerSensor


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FIXTURE = ROOT / "tests/fixtures/yolo_tracker/source-golden.json"
OUTPUT = HERE / "output"


def fixture_artifact() -> ModelArtifact:
    return ModelArtifact(
        model_id="source-recorded-yolo-fixture-v1",
        model_family="recorded-detector-fixture",
        uri="recorded://tests/fixtures/yolo_tracker/source-golden.json",
        sha256=hashlib.sha256(FIXTURE.read_bytes()).hexdigest(),
        runtime="physics_sensors.recorded",
        runtime_version="1.0.0",
        class_names=("person", "sports ball"),
        license_state="repository-generated-mit",
    )


def recorded_scene(item: dict, sequence: int) -> np.ndarray:
    image = np.full((260, 360, 3), (238, 238, 234), dtype=np.uint8)
    cv2.putText(image, "RECORDED DETECTOR REPLAY", (14, 27), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (35, 35, 35), 2)
    cv2.putText(image, str(item["label"]), (14, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (65, 65, 65), 1)
    for detection in item.get("detections", []):
        bbox = detection["bbox"]
        x, y = int(bbox["x"]), int(bbox["y"])
        width, height = int(bbox["width"]), int(bbox["height"])
        color = (55, 95, 190) if detection["class_name"] == "person" else (50, 170, 215)
        cv2.rectangle(image, (x, y), (x + width, y + height), color, -1)
        cv2.putText(image, detection["class_name"], (x + 5, min(252, y + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
    cv2.putText(image, f"synthetic frame {sequence}", (222, 247), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (70, 70, 70), 1)
    return image


def titled(image: np.ndarray, title: str) -> np.ndarray:
    panel = cv2.copyMakeBorder(image, 50, 0, 0, 0, cv2.BORDER_CONSTANT, value=(250, 250, 250))
    cv2.putText(panel, title, (12, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.57, (35, 35, 35), 2, cv2.LINE_AA)
    return panel


def annotate(frame: np.ndarray, event: dict) -> np.ndarray:
    image = frame.copy()
    for detection in event["payload"]["detections"]:
        bbox = detection["bbox"]
        x, y = int(round(bbox["x"])), int(round(bbox["y"]))
        x2, y2 = int(round(x + bbox["width"])), int(round(y + bbox["height"]))
        track_id = detection["track_id"]
        color = (20, 150, 30) if detection["class_name"] == "person" else (220, 145, 25)
        cv2.rectangle(image, (x, y), (x2, y2), color, 3)
        cv2.drawMarker(image, (int(round(detection["center"]["x"])), int(round(detection["center"]["y"]))), color, cv2.MARKER_CROSS, 18, 2)
        cv2.putText(image, f"{detection['class_name']} #{track_id} {detection['detector_confidence']:.2f}", (x, max(68, y - 7)), cv2.FONT_HERSHEY_SIMPLEX, 0.44, color, 2)
    cv2.rectangle(image, (0, 226), (360, 260), (248, 248, 248), -1)
    cv2.putText(image, f"{event['status']} | {event['payload']['actual_backend']}", (10, 249), cv2.FONT_HERSHEY_SIMPLEX, 0.43, (30, 30, 210) if event["status"] != "ok" else (30, 130, 30), 1)
    return image


def explicit_model_artifact(model: Path, family: str, license_state: str) -> ModelArtifact:
    if not model.is_file():
        raise ValueError(f"model does not exist: {model}")
    try:
        runtime_version = importlib.metadata.version("ultralytics")
    except importlib.metadata.PackageNotFoundError as exc:
        raise RuntimeError("--backend yolo requires an explicitly installed ultralytics runtime") from exc
    return ModelArtifact(
        model_id=f"user-local-{model.stem}", model_family=family, uri=str(model.resolve()),
        sha256=hashlib.sha256(model.read_bytes()).hexdigest(), runtime="ultralytics",
        runtime_version=runtime_version, class_names=(), license_state=license_state,
    )


async def execute(args: argparse.Namespace) -> list[dict]:
    if args.backend == "recorded":
        fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        entries = fixture["recorded_frames"]
        pixels = [recorded_scene(item, index) for index, item in enumerate(entries)]
        detector_backend = RecordedDetectorBackend(entries, fixture_artifact())
        evidence = "Recorded detector replay / Synthetic fixture"
    else:
        if args.model is None or not args.input or not args.model_license_state:
            raise ValueError("--backend yolo requires --model, --model-license-state and at least one --input; no download is attempted")
        artifact = explicit_model_artifact(args.model, args.model_family, args.model_license_state)
        pixels = [cv2.imread(str(path)) for path in args.input]
        if any(image is None for image in pixels):
            raise ValueError("one or more --input images could not be read")
        detector_backend = YoloDetectorBackend(artifact)
        evidence = "Real YOLO inference smoke test / User-supplied local artifact"

    backend_frames = [BackendFrame(image, image.shape[1], image.shape[0], "BGR", "image/png", source_timestamp=index / 20, observed_at=f"2026-08-16T20:00:00.{index * 50:03d}Z", monotonic_ns=12_000_000_000 + index * 50_000_000, artifact_uri=f"recorded://yolo-demo/{index}.png", quality_flags=("synthetic-fixture", "recorded-replay") if args.backend == "recorded" else ("user-supplied-input",)) for index, image in enumerate(pixels)]
    context = SensorContext.minimal("camera-to-yolo-demo")
    camera = CameraSource(ImageSequenceCameraBackend(backend_frames, nominal_fps=20, device_name=f"{args.backend}-yolo-demo"))
    sensor = YoloTrackerSensor(detector_backend)
    sensor.configure({"tracking": True, "class_filter": {"mode": "all", "values": []}})
    await camera.start(context)
    await sensor.start(context)
    events: list[dict] = []
    overlays: list[np.ndarray] = []
    originals: list[np.ndarray] = []
    async for frame in camera.read():
        originals.append(frame.pixels)
        event = sensor.process_frame(frame)
        events.append(event)
        overlays.append(annotate(frame.pixels, event))
    await sensor.stop()
    await camera.stop()

    if args.backend == "yolo" and not any(
        event["payload"]["actual_backend"].startswith("ultralytics-yolo") for event in events
    ):
        raise RuntimeError("the requested real YOLO smoke test fell back before inference; no real-inference asset was written")

    args.output.mkdir(parents=True, exist_ok=True)
    report = {"evidence": evidence, "backend_argument": args.backend, "events": events}
    (args.output / "events.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.backend == "recorded":
        cv2.imwrite(str(args.output / "overview.png"), cv2.hconcat([titled(overlays[0], "1  Zero target"), titled(overlays[1], "2  Single target"), titled(overlays[3], "3  Multiple targets")]))
        cv2.imwrite(str(args.output / "multi-target.png"), titled(overlays[3], "Recorded detector replay: payload.detections[]"))
        cv2.imwrite(str(args.output / "tracking.png"), cv2.hconcat([titled(overlays[1], "track 7: first"), titled(overlays[2], "track 7: move"), titled(overlays[4], "temporary lost"), titled(overlays[5], "track 7: reappear")]))
        cv2.imwrite(str(args.output / "fallback.png"), titled(overlays[-1], "Recorded fallback metadata: requested YOLO, actual HOG"))
    else:
        cv2.imwrite(str(args.output / "real-inference-smoke.png"), titled(overlays[0], evidence))
    return events


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend", choices=("recorded", "yolo"), default="recorded")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--model", type=Path)
    parser.add_argument("--model-family", default="YOLOv8")
    parser.add_argument("--model-license-state")
    parser.add_argument("--input", type=Path, action="append", default=[])
    args = parser.parse_args()
    events = asyncio.run(execute(args))
    print(f"wrote {len(events)} CameraSource -> YoloTrackerSensor events to {args.output}")
    print("statuses:", ", ".join(event["status"] for event in events))
    print("actual backends:", ", ".join(dict.fromkeys(event["payload"]["actual_backend"] for event in events)))


if __name__ == "__main__":
    main()
