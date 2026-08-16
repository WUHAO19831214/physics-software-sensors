# Phase 3C YOLO Adapter Replay — 2026-08-16

Evidence level: **deterministic adapter replay**. Machine-readable output: [JSON](phase3c-yolo-adapter-2026-08-16.json). Dataset: [source-recorded replay](../datasets/yolo-tracker-source-recorded-replay/dataset-card.md).

Environment: macOS 26.3.1 arm64, Python 3.12.13, NumPy 2.5.2, 360×260 synthetic frames. The benchmark used 500 in-process FramePacket → SensorEvent mappings per serialization case with `tracemalloc` enabled.

| Deterministic metric | Result |
| --- | ---: |
| Single-target mapping median / p95 | 0.099937 / 0.123583 ms |
| Single-target peak traced Python allocation | 94,588 bytes |
| Multi-target mapping + serialization median / p95 | 0.110354 / 0.130291 ms |
| Multi-target peak traced Python allocation | 90,643 bytes |
| all / ID / name filter cases | 3 / 3 passed |
| status + ID lifecycle checks | 10 / 10 passed |

Lifecycle replay produced `ok, ok, ok, lost, ok` with track IDs `[7], [7], [7,12], [], [7]`. These IDs came from fixed source-executed scripted outputs; they verify adapter handling, not ByteTrack accuracy or persistence on real images.

Latency is an in-process mapping microbenchmark and excludes camera delivery, color conversion, YOLO/ByteTrack/HOG inference, disk I/O and UI. `tracemalloc` is Python allocation evidence, not total process/GPU memory.

## Real inference

| Metric | Result |
| --- | --- |
| Executed | no |
| Reason | no maintainer-approved local model artifact; online download prohibited |
| Model / SHA / runtime / device / input size | not measured |
| Inference latency / FPS / memory / detection count | not measured |
| Accuracy | not measured; no labelled evaluation set |

## Upgrade use

Future versions must rerun source golden generation, class filters, multi-target mapping and lifecycle/fallback tests. A real-backend report must be stored separately and must never replace this deterministic compatibility baseline.
