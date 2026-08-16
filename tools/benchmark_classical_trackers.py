#!/usr/bin/env python3
"""Run deterministic Phase 3B replay/latency benchmarks; no metrology claims."""

from __future__ import annotations

import argparse
import json
import platform
import statistics
import time
from pathlib import Path

import cv2
import numpy as np

from physics_sensors.tracking import SpotCentroidTracker, TemplateTracker


ROOT = Path(__file__).resolve().parents[1]


def percent(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(len(ordered) * fraction))]


def timed(callable_, repetitions: int) -> dict[str, float]:
    samples: list[float] = []
    for _ in range(repetitions):
        started = time.perf_counter_ns()
        callable_()
        samples.append((time.perf_counter_ns() - started) / 1_000_000)
    median = statistics.median(samples)
    return {"median_ms": median, "p95_ms": percent(samples, 0.95), "throughput_fps_from_median": 1000 / median}


def spot_benchmark(repetitions: int) -> dict:
    golden = json.loads((ROOT / "tests/fixtures/spot_centroid/golden.json").read_text(encoding="utf-8"))
    sample = ROOT / "examples/spot-centroid/sample"
    tracker = SpotCentroidTracker()
    matches = 0
    errors: list[float] = []
    frames: list[np.ndarray] = []
    for case in golden["cases"]:
        frame = cv2.imread(str(sample / case["file"]))
        frames.append(frame)
        result = tracker.update(frame).source_projection()
        source = case["source_result"]
        if result["locked"] == source["locked"]:
            matches += 1
        if result["locked"]:
            errors.append(float(np.hypot(result["x"] - source["x"], result["y"] - source["y"])))
    cursor = 0

    def update():
        nonlocal cursor
        tracker.update(frames[cursor % len(frames)])
        cursor += 1

    return {
        "fixture_cases": len(frames),
        "detection_lost_matches": matches,
        "max_centroid_error_px": max(errors, default=0),
        "source_tolerance_px": golden["tolerance_px"],
        "timing": timed(update, repetitions),
    }


def template_scene(x: int | None) -> np.ndarray:
    image = np.full((240, 360, 3), 232, dtype=np.uint8)
    cv2.line(image, (20, 180), (340, 180), (80, 80, 80), 2)
    if x is not None:
        cv2.rectangle(image, (x, 90), (x + 70, 150), (35, 45, 180), -1)
        for index in range(5):
            cv2.circle(image, (x + 10 + index * 13, 105 + (index % 2) * 25), 5, (240, 220, 30), -1)
        cv2.putText(image, "A7", (x + 15, 133), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    return image


def template_benchmark(repetitions: int) -> dict:
    golden = json.loads((ROOT / "tests/fixtures/template_tracker/golden.json").read_text(encoding="utf-8"))
    stable_fields = ("ok", "bbox_x1", "bbox_y1", "bbox_x2", "bbox_y2", "bbox_width", "bbox_height", "center_x", "center_y", "confidence", "status", "tracking_status")
    scripted_agreement = all(all(key in case["result"] for key in stable_fields) for case in golden["cases"])
    initial = template_scene(60)
    sequence = [template_scene(70), template_scene(85), template_scene(100), template_scene(None)]
    tracker = TemplateTracker("CSRT")
    initialized = tracker.initialize(initial, (60, 90, 70, 60))
    results = []
    latencies: list[float] = []
    for frame in sequence:
        started = time.perf_counter_ns()
        results.append(tracker.update(frame))
        latencies.append((time.perf_counter_ns() - started) / 1_000_000)

    timing_tracker = TemplateTracker("CSRT")
    timing_tracker.initialize(initial, (60, 90, 70, 60))
    moving = template_scene(70)
    timing = timed(lambda: timing_tracker.update(moving), repetitions)
    center_errors = []
    expected_centers = [(105, 120), (120, 120), (135, 120)]
    for result, expected in zip(results[:3], expected_centers, strict=True):
        if result.ok:
            center_errors.append(float(np.hypot(result.center_x - expected[0], result.center_y - expected[1])))
    return {
        "source_scripted_cases": len(golden["cases"]),
        "source_stable_fields_present": scripted_agreement,
        "source_numeric_tolerance_px": 1e-9,
        "initialized": initialized,
        "requested_backend": "CSRT",
        "selected_backend": tracker.actual_tracker_type,
        "fallback_used": tracker.fallback_used,
        "tracking_statuses": [result.tracking_status for result in results],
        "synthetic_tracking_successes": sum(result.ok for result in results[:3]),
        "synthetic_lost_correct": not results[-1].ok,
        "max_synthetic_center_error_px": max(center_errors, default=None),
        "sequence_update_median_ms": statistics.median(latencies),
        "timing_same_frame_replay": timing,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repetitions", type=int, default=200)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    payload = {
        "benchmark_version": "phase3b-1.0.0",
        "date": "2026-08-16",
        "evidence_level": "synthetic/replay; not real-experiment accuracy",
        "environment": {"python": platform.python_version(), "opencv": cv2.__version__, "numpy": np.__version__, "platform": platform.platform()},
        "repetitions": args.repetitions,
        "spot_centroid": spot_benchmark(args.repetitions),
        "template_tracker": template_benchmark(args.repetitions),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
