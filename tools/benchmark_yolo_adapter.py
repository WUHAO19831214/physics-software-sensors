#!/usr/bin/env python3
"""Offline microbenchmark for YOLO event mapping and replay semantics."""

from __future__ import annotations

import argparse
import asyncio
import json
import platform
import statistics
import sys
import time
import tracemalloc
from pathlib import Path
from typing import Any

import numpy as np

from physics_sensors.core import RuntimeFrame, SensorContext
from physics_sensors.tracking import RecordedDetectorBackend, YoloTrackerSensor


ROOT = Path(__file__).resolve().parents[1]
GOLDEN_PATH = ROOT / "tests/fixtures/yolo_tracker/source-golden.json"


def packet(pixels: np.ndarray, sequence: int) -> RuntimeFrame:
    return RuntimeFrame(
        metadata={
            "schema_version": "1.0.0",
            "frame_id": f"94000000-0000-4000-8000-{sequence:012d}",
            "run_id": "yolo-adapter-benchmark",
            "source_sensor_id": "camera.capture",
            "sequence": sequence,
            "observed_at": "2026-08-16T20:00:00.000Z",
            "monotonic_ns": 12_000_000_000 + sequence,
            "source_timestamp": float(sequence),
            "media": {
                "kind": "camera-frame",
                "media_type": "application/x-raw-bgr",
                "width": pixels.shape[1],
                "height": pixels.shape[0],
                "color_space": "BGR",
                "orientation": "0",
                "mirrored": False,
            },
            "artifact": {
                "uri": f"recorded://benchmark/{sequence}",
                "media_type": "image/png",
                "sha256": "8" * 64,
                "bytes": int(pixels.nbytes),
            },
            "quality": {"dropped_since_last": 0, "flags": ["synthetic-fixture"]},
        },
        pixels=pixels,
    )


def percentile(values: list[float], fraction: float) -> float:
    return sorted(values)[min(len(values) - 1, int(len(values) * fraction))]


async def map_case(frame: dict[str, Any], iterations: int) -> dict[str, Any]:
    pixels = np.zeros((260, 360, 3), dtype=np.uint8)
    sensor = YoloTrackerSensor(RecordedDetectorBackend([frame] * iterations))
    await sensor.start(SensorContext.minimal("yolo-adapter-benchmark"))
    latencies: list[float] = []
    last_event: dict[str, Any] = {}
    tracemalloc.start()
    for index in range(iterations):
        started = time.perf_counter_ns()
        last_event = sensor.process_frame(packet(pixels, index))
        latencies.append((time.perf_counter_ns() - started) / 1_000_000.0)
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    await sensor.stop()
    return {
        "iterations": iterations,
        "median_ms": statistics.median(latencies),
        "p95_ms": percentile(latencies, 0.95),
        "peak_tracemalloc_bytes": peak_bytes,
        "serialized_detection_count": len(last_event["payload"]["detections"]),
    }


async def verify_filters(frame: dict[str, Any]) -> dict[str, Any]:
    pixels = np.zeros((260, 360, 3), dtype=np.uint8)
    cases = [
        ({"mode": "all", "values": []}, ["person", "sports ball"]),
        ({"mode": "ids", "values": [1]}, ["sports ball"]),
        ({"mode": "names", "values": ["person"]}, ["person"]),
    ]
    passed = 0
    for index, (class_filter, expected) in enumerate(cases):
        sensor = YoloTrackerSensor(RecordedDetectorBackend([frame]))
        sensor.configure({"class_filter": class_filter})
        await sensor.start(SensorContext.minimal("yolo-adapter-benchmark"))
        event = sensor.process_frame(packet(pixels, index))
        await sensor.stop()
        actual = [item["class_name"] for item in event["payload"]["detections"]]
        passed += actual == expected
    return {"passed": passed, "total": len(cases)}


async def verify_tracking(frames: list[dict[str, Any]]) -> dict[str, Any]:
    pixels = np.zeros((260, 360, 3), dtype=np.uint8)
    sensor = YoloTrackerSensor(RecordedDetectorBackend(frames))
    await sensor.start(SensorContext.minimal("yolo-adapter-benchmark"))
    events = [sensor.process_frame(packet(pixels, index)) for index in range(len(frames))]
    await sensor.stop()
    expected_status = ["ok", "ok", "ok", "lost", "ok"]
    actual_status = [event["status"] for event in events]
    expected_ids = [[7], [7], [7, 12], [], [7]]
    actual_ids = [[item["track_id"] for item in event["payload"]["detections"]] for event in events]
    passed = sum(actual == expected for actual, expected in zip(actual_status, expected_status, strict=True))
    passed += sum(actual == expected for actual, expected in zip(actual_ids, expected_ids, strict=True))
    return {
        "passed": passed,
        "total": len(expected_status) * 2,
        "statuses": actual_status,
        "track_ids": actual_ids,
    }


async def run(iterations: int) -> dict[str, Any]:
    golden = json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    recorded = golden["recorded_frames"]
    return {
        "schema_version": "1.0.0",
        "generated_at": "2026-08-16",
        "evidence_level": "deterministic-adapter-replay",
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "input_size": [360, 260],
        },
        "fixture": str(GOLDEN_PATH.relative_to(ROOT)),
        "single_target_mapping": await map_case(recorded[1], iterations),
        "multi_target_serialization": await map_case(recorded[3], iterations),
        "class_filter": await verify_filters(recorded[3]),
        "tracking_state": await verify_tracking(recorded[1:6]),
        "real_inference": {
            "executed": False,
            "reason": "No maintainer-approved local model artifact was supplied; online download is prohibited.",
            "model": "not measured",
            "model_sha256": "not measured",
            "device": "not measured",
            "input_size": "not measured",
            "latency_ms": "not measured",
            "fps": "not measured",
            "memory": "not measured",
            "detection_count": "not measured",
            "accuracy": "not measured; no labelled evaluation set",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=500)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.iterations <= 0:
        parser.error("--iterations must be positive")
    result = asyncio.run(run(args.iterations))
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
