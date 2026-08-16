#!/usr/bin/env python3
"""Generate tracker.template golden output by executing the fixed source module."""

from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any

import numpy as np

SOURCE_SHA = "85740d686c67452a057540edb564d713e01ccc51"
SOURCE_FILE = "src/object_template_tracker.py"


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


def source_module(source_root: Path):
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=source_root, text=True
    ).strip()
    if head != SOURCE_SHA:
        raise SystemExit(f"source HEAD must be {SOURCE_SHA}, found {head}")
    module_path = source_root / SOURCE_FILE
    spec = importlib.util.spec_from_file_location("phase3b_source_template_tracker", module_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot import {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def snapshot(label: str, tracker: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {
        "label": label,
        "result": result,
        "requested_backend": tracker.requested_tracker_type,
        "actual_backend": tracker.actual_tracker_type,
        "initialized": tracker.initialized,
        "lost_frame_count": tracker.lost_frame_count,
        "consecutive_lost_frames": tracker.consecutive_lost_frames,
        "total_frame_count": tracker.total_frame_count,
        "tracked_frame_count": tracker.tracked_frame_count,
    }


def generate(module: Any) -> dict[str, Any]:
    frame = np.zeros((120, 180, 3), dtype=np.uint8)
    calls: list[str] = []

    def fallback_factory(backend: str):
        calls.append(backend)
        if backend == "CSRT":
            raise RuntimeError("scripted unavailable")
        if backend == "KCF":
            return ScriptedTracker(False, [])
        return ScriptedTracker(
            True,
            [
                (True, (12.0, 22.0, 40.0, 30.0)),
                (False, None),
                RuntimeError("scripted update failure"),
            ],
        )

    module.create_opencv_tracker = fallback_factory
    tracker = module.ObjectTemplateTracker("CSRT")
    cases: list[dict[str, Any]] = []
    initialized = tracker.initialize(frame, (10.2, 20.4, 40.1, 30.3))
    cases.append(snapshot("initialize-fallback", tracker, tracker.last_result.copy()))
    cases.append(snapshot("move", tracker, tracker.update(frame)))
    cases.append(snapshot("disappear", tracker, tracker.update(frame)))
    cases.append(snapshot("tracker-failure", tracker, tracker.update(frame)))

    def reinitialize_factory(backend: str):
        calls.append(backend)
        return ScriptedTracker(True, [(True, (31.0, 41.0, 24.0, 18.0))])

    module.create_opencv_tracker = reinitialize_factory
    reinitialized = tracker.initialize(frame, (30, 40, 24, 18))
    cases.append(snapshot("reinitialize", tracker, tracker.last_result.copy()))
    cases.append(snapshot("post-reinitialize-move", tracker, tracker.update(frame)))

    def unavailable_factory(backend: str):
        calls.append(backend)
        raise RuntimeError(f"{backend} unavailable")

    module.create_opencv_tracker = unavailable_factory
    unavailable = module.ObjectTemplateTracker("CSRT")
    unavailable_initialized = unavailable.initialize(frame, (10, 10, 20, 20))
    cases.append(snapshot("all-backends-unavailable", unavailable, unavailable.last_result.copy()))

    import cv2

    return {
        "fixture_version": "1.0.0",
        "generated_by": "tools/generate_template_tracker_golden.py",
        "source": {
            "repository": "WUHAO19831214/audio-visual-soundfield-tracker-stable",
            "commit": SOURCE_SHA,
            "file": SOURCE_FILE,
            "class": "ObjectTemplateTracker",
        },
        "environment": {
            "python": platform.python_version(),
            "opencv": cv2.__version__,
            "platform": platform.platform(),
        },
        "script": {
            "frame_shape": list(frame.shape),
            "initialization_roi": [10.2, 20.4, 40.1, 30.3],
            "fallback_order": list(module.TRACKER_FALLBACK_ORDER),
            "factory_calls": calls,
        },
        "assertions": {
            "initialized": initialized,
            "reinitialized": reinitialized,
            "unavailable_initialized": unavailable_initialized,
        },
        "cases": cases,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    payload = generate(source_module(args.source_root.resolve()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(f"wrote {len(payload['cases'])} source-executed cases to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
