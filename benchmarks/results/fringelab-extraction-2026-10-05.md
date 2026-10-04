# FringeLab extraction evidence — 2026-10-05

Fixed source: `WUHAO19831214/webcam-laser-fringelab@37a8b3996791790a22980b0d562996a65a3a65ef`. Source owner authorized collection into this MIT repository. The source application was not modified.

## Both batches delivered

- Batch 1: calculator parser/floating panel, rotated ROI and native viewport mapping, virtual ruler, confirmed manual two-point/multi-point calibration, relative profile and signal features.
- Batch 2: original automatic ruler modes and selected-region path, ruler-number OCR candidate helper, browser camera backend for existing `camera.capture`, optical inversion/regression/uncertainty and simulation.
- Catalog: two Processor Sensors (`image.strip-profile`, `vision.ruler-ticks`) and three Companion Tools. Browser camera/OCR add toolkit backends; calculator/ROI/ruler UI remain separately importable React components.

## Source equivalence

`tools/compare_fringelab_source.py --source /path/to/source` reads fixed files with `git show`, verifies 18 recorded source SHA-256 hashes, then executes the same harness on original TS and compiled extraction. Golden output matches exactly after typed-array serialization and removing generated ruler timestamps. Inputs cover five calculator expressions, rotated ROI resizing, manual ruler ticks, multi-point mapping, deterministic double-slit pixels, complete channel/profile arrays, peaks/troughs/FWHM/period, optical regression/analysis and four automatic-ruler scenes (light/dark ruler, rotated and perspective/missing ticks).

The 55 original tests are retained with import changes only. Seven new checks include adapter lifecycle/errors/metadata, no-sample lost state, candidate ruler output, calibration invalidation/extrapolation, native coordinate mapping, controlled camera backend cancellation, ruler job cancellation and the source golden. Total: **62/62** (six adapter tests plus one golden test).

Five emitted events (valid, clipping, lost and error paths) were validated with `sensor-event.schema.json`, JSON Schema Draft 2020-12 and format checking: **5/5**. Pixel arrays stay in runtime FramePackets; serializable events retain parent-frame identity and observed time.

## Browser evidence

Production Vite build; headless Chrome via agent-browser. [Recorded checks](fringelab-browser-verification.json): seven flows passed, including independent calculator IDs/arithmetic/Esc focus, manual scale with synthetic wavelength near 650 nm, parameter/source invalidation, ROI angle, editable multi-point anchors, automatic detection Worker/candidate state and 390 px layout. [Verified screenshot](../../docs/assets/fringelab-toolkit.png).

The real Tesseract.js 6 browser worker also completed the demo ruler OCR: **0 usable anchors** in the automatically selected synthetic ruler region, and no calibration was applied. This proves the execution path and empty-result handling, not numeric OCR accuracy. The existing core's real Tesseract.js 7 tests remain **30/30** overall. No physical camera was activated; camera lifecycle evidence uses an explicitly controlled injected backend. Optional HEIC runtime with device photos is not measured.

## Local synthetic latency

[Machine-readable measurements](fringelab-latency.json). Node v24.13.0, macOS arm64, Apple M2; five warm-ups and 30 samples per algorithm. Timings exclude Worker transfer and capture.

| Path | Input | Median ms | p95 ms |
| --- | --- | --- | --- |
| Strip extraction | 960×540 RGBA, 768×64 ROI | 5.478 | 7.315 |
| Automatic ruler | 720×280 synthetic ruler | 70.906 | 74.082 |

## Reproduce

```sh
npm --prefix packages/typescript ci
npm --prefix packages/typescript test
npm --prefix packages/fringelab ci
npm --prefix packages/fringelab test
python3 tools/compare_fringelab_source.py --source /path/to/webcam-laser-fringelab
node tools/benchmark_fringelab.mjs
npm --prefix examples/web-fringelab-toolkit ci
npm --prefix examples/web-fringelab-toolkit run build
npm --prefix examples/web-fringelab-toolkit run preview -- --port 4173
# In another terminal, with agent-browser installed:
AGENT_BROWSER_BIN=/path/to/agent-browser node tools/verify_fringelab_browser.mjs
python3 tools/build_fringelab_artifacts.py
```

## Limits and preservation

Automatic tick periods assume the physical minor tick represents 1 mm; a candidate can misidentify that period. Keep existing manual, multi-point and selected-region modes, check units/known length, then confirm. These useful tools are collected now; a benchmark dataset is a future quality improvement, not a collection blocker. Real-photo error, actual camera exposure/negotiated rate, physical movement, optical uncertainty validation and radiometric conversion remain **not measured**. DN is not lux or W/m². Perspective mapping is one-dimensional, not homography.

Local artifacts and clean-install results are recorded in `build/fringelab/manifest.json`; they are not registry/Release publications. Existing immutable v0.6.0 artifacts remain unchanged.
