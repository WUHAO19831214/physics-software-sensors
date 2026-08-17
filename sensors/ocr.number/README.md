# Number OCR Sensor

**English** | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

Sensor ID: `ocr.number` · Implementation version: `0.2.0` · Maturity: `experimental` · Evidence: `E3` · Release: `v0.6.0`

<!-- section:name -->
## Name
Number OCR Sensor
<!-- section:description -->
## One-line description
Reads a numeric display from a frame ROI while preserving raw text, parsed value, confidence, duration, warnings and explicit failure.
<!-- section:physics-use -->
## Typical physics experiment use
Reads values shown by existing instrument software for teaching visualization or synchronized analysis when direct SDK data is unavailable.
<!-- section:measurement -->
## What it actually measures
The chain is software display → screen pixels → OCR text → numeric parse. It does not directly read device internals; units and physical range checks come from configuration/downstream logic.
<!-- section:sources -->
## Source projects
| Repository | Commit | Source paths / use |
| --- | --- | --- |
| [physics-experiment-bridge-mvp](https://github.com/WUHAO19831214/physics-experiment-bridge-mvp) | `8bba87df6475cae1e595fc925551db8bea83fb68` | `TesseractRecognizer.ts`, `extractNumber.ts`, preprocess utilities, `OCR_VALIDATION.md`; real Tesseract.js path |
| [ampere-force-visualizer-teacher-yanan](https://github.com/WUHAO19831214/ampere-force-visualizer-teacher-yanan) | `cb073e89d6d87129287030f1df08bd540504eb39` | matching recognizer/utilities; Fy/Fz teacher display reading |
<!-- section:how-it-works -->
## How it works
RGBA frame → normalized ROI → preprocessing → Tesseract.js/recorded recognizer → raw text normalization → numeric parse/validation → `SensorEvent`. OCR/parse errors emit no mock measurement.
<!-- section:input -->
## Input
Screen/image `FramePacket` with RGBA pixels, ROI, whitelist/preprocess options, value name and unit.
<!-- section:output -->
## Output
`SensorEvent` with `raw_text`, parsed measurement when successful, confidence, duration, warnings/artifacts and explicit `OCR_RECOGNITION_FAILED` or `OCR_PARSE_FAILED` errors.
<!-- section:demo -->
## Demo
[![Synthetic pixel OCR](assets/overview.png)](assets/README.md) Shows real Tesseract.js on synthetic pixels, not a real instrument display.
<!-- section:example -->
## Minimal example
Run [web-number-ocr](../../examples/web-number-ocr/README.md) or [screen-to-ocr](../../examples/web-screen-to-ocr/README.md).
<!-- section:distribution -->
## Distribution / Download
TypeScript package `0.3.0`; [ocr.number-0.2.0.zip](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/ocr.number-0.2.0.zip). Real OCR may obtain language data at runtime.
<!-- section:evidence -->
## Evidence level
`E3`: actual Tesseract.js executed on controlled synthetic pixels, including failures.
<!-- section:maturity -->
## Maturity
`experimental`; manifest `incubating/adapter-present`.
<!-- section:limitations -->
## Known limitations
Default numeric parsing excludes scientific notation. Character normalization can confuse letters/digits. Confidence is not accuracy; real displays, fonts, scaling, glare and browser compatibility lack E4 evidence.
<!-- section:benchmark -->
## Benchmark
See [OCR benchmark](benchmarks/README.md); required metrics include exact match, numeric parse success/error, latency and failure rate.
<!-- section:provenance -->
## Provenance
The two fixed source commits share identical core OCR/preprocess files; hashes and changes are in [SOURCE.md](SOURCE.md), facts in [sensor.json](sensor.json).
