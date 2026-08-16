#!/usr/bin/env python3
"""Run the fixed source tracker and new adapter algorithm on identical frames."""

from __future__ import annotations

import argparse
import importlib.util
import math
import subprocess
from pathlib import Path

import cv2
import numpy as np

from physics_sensors.tracking import ColorMarkerConfig, ColorMarkerTracker


EXPECTED_COMMIT = "85740d686c67452a057540edb564d713e01ccc51"
NUMERIC_FIELDS = {
    "bbox_x1",
    "bbox_y1",
    "bbox_x2",
    "bbox_y2",
    "bbox_width",
    "bbox_height",
    "center_x",
    "center_y",
    "confidence",
    "marker_radius",
    "marker_area",
    "marker_circularity",
}


def synthetic_frame(center: tuple[int, int] | None, radius: int = 14) -> np.ndarray:
    frame = np.zeros((120, 160, 3), dtype=np.uint8)
    if center is not None:
        cv2.circle(frame, center, radius, (0, 255, 255), -1)
    return frame


def load_source(source_root: Path):
    actual = subprocess.check_output(
        ["git", "-C", str(source_root), "rev-parse", "HEAD"], text=True
    ).strip()
    if actual != EXPECTED_COMMIT:
        raise SystemExit(f"source checkout must be {EXPECTED_COMMIT}; found {actual}")
    source_file = source_root / "src" / "tennis_ball_tracker.py"
    spec = importlib.util.spec_from_file_location("source_tennis_ball_tracker", source_file)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {source_file}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def equivalent(left: dict, right: dict, tolerance: float) -> list[str]:
    differences: list[str] = []
    if set(left) != set(right):
        differences.append(f"keys differ: {sorted(set(left) ^ set(right))}")
    for key in sorted(set(left) & set(right)):
        a, b = left[key], right[key]
        if key in NUMERIC_FIELDS and a is not None and b is not None:
            if not math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=tolerance):
                differences.append(f"{key}: source={a!r}, new={b!r}")
        elif a != b:
            differences.append(f"{key}: source={a!r}, new={b!r}")
    return differences


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--tolerance", type=float, default=1e-6)
    args = parser.parse_args()
    source = load_source(args.source_root.resolve())
    kwargs = {
        "hsv_lower": (20, 100, 100),
        "hsv_upper": (40, 255, 255),
        "min_area": 100,
        "max_area": 2000,
        "min_circularity": 0.6,
        "smoothing": 0.5,
    }
    old_tracker = source.TennisBallTracker(**kwargs)
    new_tracker = ColorMarkerTracker(ColorMarkerConfig(**kwargs))
    cases = [
        ("first", synthetic_frame((60, 60))),
        ("second", synthetic_frame((80, 60))),
        ("lost", synthetic_frame(None)),
        ("reacquired", synthetic_frame((82, 62))),
    ]
    all_differences: list[str] = []
    for name, frame in cases:
        old_result = old_tracker.update(frame)
        new_result = new_tracker.update(frame).to_source_dict()
        differences = equivalent(old_result, new_result, args.tolerance)
        if differences:
            all_differences.extend(f"{name}: {item}" for item in differences)
        else:
            print(f"PASS {name}: source and adapter outputs match")
    if all_differences:
        for difference in all_differences:
            print(f"FAIL {difference}")
        return 1
    print(f"PASS 4/4 cases at absolute tolerance {args.tolerance:g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
