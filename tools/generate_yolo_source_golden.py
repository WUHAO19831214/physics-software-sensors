#!/usr/bin/env python3
"""Generate YOLO/centroid golden data by executing the fixed source modules."""

from __future__ import annotations

import argparse
import importlib
import json
import platform
import subprocess
import sys
import tempfile
from dataclasses import asdict
from pathlib import Path
from typing import Any

import cv2
import numpy as np


SOURCE_SHA = "85740d686c67452a057540edb564d713e01ccc51"


class FakeBox:
    def __init__(self, xyxy, confidence, class_id, track_id=None) -> None:
        self.xyxy = np.asarray([xyxy], dtype=float)
        self.conf = np.asarray([confidence], dtype=float)
        self.cls = np.asarray([class_id], dtype=float)
        self.id = None if track_id is None else np.asarray([track_id], dtype=float)


class FakeResult:
    names = {0: "person", 1: "sports ball"}

    def __init__(self, boxes) -> None:
        self.boxes = boxes


class ScriptedYolo:
    names = FakeResult.names

    def __init__(self, prediction_frames, tracking_frames) -> None:
        self.prediction_frames = iter(prediction_frames)
        self.tracking_frames = iter(tracking_frames)
        self.predict_calls: list[dict[str, Any]] = []
        self.track_calls: list[dict[str, Any]] = []

    @staticmethod
    def filtered(boxes, classes):
        if classes is None:
            return boxes
        allowed = set(classes)
        return [box for box in boxes if int(box.cls[0]) in allowed]

    def predict(self, **kwargs):
        self.predict_calls.append(kwargs)
        return [FakeResult(self.filtered(next(self.prediction_frames), kwargs.get("classes")))]

    def track(self, **kwargs):
        self.track_calls.append(kwargs)
        return [FakeResult(self.filtered(next(self.tracking_frames), kwargs.get("classes")))]


def source_modules(source_root: Path):
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=source_root, text=True).strip()
    if head != SOURCE_SHA:
        raise SystemExit(f"source HEAD must be {SOURCE_SHA}, found {head}")
    sys.path.insert(0, str(source_root))
    detector = importlib.import_module("src.detector")
    processor = importlib.import_module("src.camera_processor")
    return detector, processor


def detection_payload(item: Any) -> dict[str, Any]:
    value = asdict(item)
    value["center"] = list(item.center)
    value["bbox"] = {
        "x": item.x1,
        "y": item.y1,
        "width": item.x2 - item.x1,
        "height": item.y2 - item.y1,
    }
    return value


def generate(source_root: Path) -> dict[str, Any]:
    detector_module, processor_module = source_modules(source_root)
    frame = np.zeros((260, 360, 3), dtype=np.uint8)
    person_0 = FakeBox((10, 20, 110, 220), 0.91, 0, 7)
    person_1 = FakeBox((20, 20, 120, 220), 0.90, 0, 7)
    person_2 = FakeBox((30, 20, 130, 220), 0.89, 0, 7)
    ball = FakeBox((220, 100, 270, 150), 0.82, 1, 12)
    person_reappear = FakeBox((36, 20, 136, 220), 0.88, 0, 7)
    missing_id = FakeBox((40, 20, 140, 220), 0.87, 0, None)

    model = ScriptedYolo(
        prediction_frames=[[], [person_0], [person_0, ball]],
        tracking_frames=[[person_0], [person_1], [person_2, ball], [], [person_reappear], [missing_id]],
    )
    with tempfile.TemporaryDirectory() as temporary:
        weight = Path(temporary) / "yolov8n.pt"
        weight.write_bytes(b"source-golden-placeholder-not-a-model")
        source_detector = detector_module.Detector(
            confidence_threshold=0.25,
            person_only=False,
            model_paths=[weight],
            yolo_factory=lambda path: model,
        )
        detection_cases = []
        for label in ("zero-target", "single-target", "multi-target"):
            values = source_detector.detect(frame)
            detection_cases.append({"label": label, "detections": [detection_payload(item) for item in values]})
        tracking_cases = []
        for label in ("single-track", "move", "two-tracks", "lost", "reappear", "missing-native-id"):
            values = source_detector.track(frame)
            tracking_cases.append({
                "label": label,
                "detections": [detection_payload(item) for item in values],
                "tracking_warning": source_detector.tracking_warning,
            })

    centroid = processor_module.CentroidTracker(max_missed=2, max_distance_ratio=0.18)
    centroid_inputs = [
        [detector_module.Detection(10, 20, 110, 220, 0.91)],
        [detector_module.Detection(20, 20, 120, 220, 0.90)],
        [detector_module.Detection(30, 20, 130, 220, 0.89), detector_module.Detection(220, 100, 270, 150, 0.82, 1, "sports ball")],
        [],
        [detector_module.Detection(36, 20, 136, 220, 0.88)],
    ]
    centroid_cases = []
    for index, (label, values) in enumerate(zip(("single", "move", "double", "lost", "reappear"), centroid_inputs, strict=True)):
        tracks = centroid.update(values, float(index), frame.shape)
        centroid_cases.append({"label": label, "tracks": [track.to_dict() for track in tracks]})
    centroid.reset()
    reset_tracks = centroid.update(centroid_inputs[0], 10.0, frame.shape)
    centroid_cases.append({"label": "after-reset", "tracks": [track.to_dict() for track in reset_tracks]})

    recorded_frames = []
    for case in tracking_cases[:5]:
        recorded_frames.append({
            "label": case["label"],
            "requested_backend": "ultralytics-yolo-bytetrack",
            "actual_backend": "ultralytics-yolo-bytetrack",
            "attempted_backends": ["ultralytics-yolo-bytetrack"],
            "tracking_mode": "bytetrack",
            "fallback_used": False,
            "detections": [
                {
                    "track_id": item["track_id"],
                    "tracking_id_available": item["tracking_id_available"],
                    "class_id": item["class_id"],
                    "class_name": item["class_name"],
                    "bbox": item["bbox"],
                    "detector_confidence": item["confidence"],
                }
                for item in case["detections"]
            ],
        })
    recorded_frames.insert(0, {
        "label": "zero-target",
        "requested_backend": "ultralytics-yolo-detect",
        "actual_backend": "ultralytics-yolo-detect",
        "attempted_backends": ["ultralytics-yolo-detect"],
        "tracking_mode": "detection-only",
        "fallback_used": False,
        "detections": [],
    })
    recorded_frames.append({
        "label": "hog-fallback",
        "requested_backend": "ultralytics-yolo-bytetrack",
        "actual_backend": "opencv-hog",
        "attempted_backends": ["ultralytics-yolo-bytetrack", "opencv-hog"],
        "tracking_mode": "centroid",
        "fallback_used": True,
        "fallback_reason": "recorded source-equivalent missing local weight",
        "detections": [],
    })

    return {
        "fixture_version": "1.0.0",
        "generated_by": "tools/generate_yolo_source_golden.py",
        "source": {
            "repository": "WUHAO19831214/audio-visual-soundfield-tracker-stable",
            "commit": SOURCE_SHA,
            "files": ["src/detector.py", "src/camera_processor.py"],
            "symbols": ["Detector.detect", "Detector.track", "CentroidTracker.update", "CentroidTracker.reset"],
        },
        "environment": {"python": platform.python_version(), "opencv": cv2.__version__, "platform": platform.platform()},
        "source_detector_cases": detection_cases,
        "source_tracking_cases": tracking_cases,
        "source_centroid_cases": centroid_cases,
        "recorded_frames": recorded_frames,
        "source_call_arguments": {
            "predict": [{key: value for key, value in call.items() if key != "source"} for call in model.predict_calls],
            "track": [{key: value for key, value in call.items() if key != "source"} for call in model.track_calls],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    payload = generate(args.source_root.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(payload['recorded_frames'])} recorded frames and source comparisons to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
