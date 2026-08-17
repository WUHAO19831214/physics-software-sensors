# Evidence levels

Evidence level describes **what has actually been exercised**, not how complete a Sensor Page looks and not whether an API feels stable. The registry at [`benchmarks/results/index.json`](../benchmarks/results/index.json) assigns one current level to each sensor.

| Level | Required evidence | What it does not prove |
| --- | --- | --- |
| E0 — Contract | Manifest, Schema-valid examples and interface shape | An implementation exists or runs |
| E1 — Deterministic replay | Adapter runs on synthetic or recorded fixtures; success and failure paths are asserted | Compatibility with the historical source or a real engine/device |
| E2 — Source compatibility | Fixed source commit is executed or its recorded native output is compared through a documented golden-master method | A real production runtime, model or physical device was exercised |
| E3 — Real runtime | Actual OCR/CV/runtime backend executes on controlled synthetic or recorded pixels | Real laboratory conditions, broad accuracy or device compatibility |
| E4 — Real device/lab | Named hardware/software, OS, settings and a reproducible real-world dataset are tested | Safe adoption by a downstream experiment project |
| E5 — Downstream integration | A source project uses a pinned release behind a rollback path and passes its regression suite | Automatic `stable` status or metrological certification |

## Assignment rules

1. Record only the highest fully satisfied level; a sensor can retain lower-level evidence in its reports.
2. A mock or recorded backend never counts as the corresponding real runtime.
3. A runtime executing synthetic pixels may reach E3, but not E4.
4. Source compatibility must identify repository, complete commit SHA, source path/function and numeric or semantic tolerance.
5. Missing values are written as `not measured`; they are never replaced with zero.
6. Evidence level and maturity are separate. A sensor remains `experimental` until every applicable maturity gate passes.

## Current result

`camera.capture` and `screen.capture` are E1; `tracker.color-marker` and `tracker.yolo` are E2; `ocr.number` and `tracker.template` are E3. `tracker.spot-centroid` is E5 through the pinned offline-replay integration recorded in [`integrations/spot-vibration`](../integrations/spot-vibration/README.md). No Sensor has E4 real-device/lab evidence, and E5 does not change its `experimental` maturity.
