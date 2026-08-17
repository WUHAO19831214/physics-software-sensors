# Validation matrix

This matrix is an evidence index, not a product score. Detailed values and limitations live in the [machine-readable benchmark registry](../benchmarks/results/index.json).

| Sensor | Adapter | Golden | Real runtime | Real device | Accuracy dataset | Benchmark | Clean install | Downstream | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `camera.capture` | synthetic image sequence | not measured | deterministic backend only | physical camera not tested | none | timing replay | wheel tested | not measured | E1 |
| `screen.capture` | recorded RGBA + browser seam | not measured | browser driver mocked | `getDisplayMedia` not executed | none | timing replay | tgz tested | not measured | E1 |
| `ocr.number` | ROI/parse/SensorEvent | source parser behavior | Tesseract.js 7 on synthetic pixels | experiment UI not tested | 3 synthetic numbers only | sample durations; no p50/p95 | tgz tested | not measured | E3 |
| `tracker.color-marker` | OpenCV HSV/contour | source match 4/4, `1e-6` | OpenCV on synthetic frames | camera not tested | none | latency/error not measured | wheel tested | not measured | E2 |
| `tracker.spot-centroid` | weighted centroid | source match 6/6, max `0 px` | OpenCV/NumPy synthetic | optical spot not tested | six source fixtures + seven downstream synthetic cases | median/p95 + downstream delta | v0.6.0 wheel SHA pinned | [Merged PR #1](https://github.com/WUHAO19831214/spot-vibration-tracking-system-20260508-171952/pull/1): legacy/library/compare + rollback | E5 |
| `tracker.template` | ROI-initialized tracker | seven source lifecycle cases | actual OpenCV contrib CSRT synthetic | moving object not tested | three synthetic moves + lost | median/p95 measured | wheel tested | not measured | E3 |
| `tracker.yolo` | recorded/backend seam | detector 3 + tracking 6 source cases | Ultralytics/ByteTrack not run | camera/model not tested | none | adapter mapping only | default wheel tested | not measured | E2 |

## Cross-sensor compositions

Only meaningful source-to-processor paths are tested; this is intentionally not a Cartesian product.

| Path | Fixture | Result |
| --- | --- | --- |
| Camera → Color | synthetic BGR yellow marker | passed |
| Camera → Spot | synthetic BGR red spot | passed |
| Camera → Template | synthetic textured ROI, actual OpenCV contrib backend | passed |
| Camera → YOLO | synthetic camera frame plus source-recorded detection | passed |
| Screen → OCR | recorded synthetic RGBA frame plus real Tesseract.js | passed |

The authoritative declarations are [`tests/composition/matrix.json`](../tests/composition/matrix.json); executable tests live beside it and in the TypeScript test package.
