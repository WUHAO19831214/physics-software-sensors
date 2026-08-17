# Screen Capture Sensor

**English** | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

Sensor ID: `screen.capture` · Implementation version: `0.3.0` · Maturity: `experimental` · Evidence: `E1` · Release: `v0.6.0`

<!-- section:name -->
## Name
Screen Capture Sensor
<!-- section:description -->
## One-line description
Captures pixels from a user-selected screen, window or tab and emits timestamped screen `FramePacket` records.
<!-- section:physics-use -->
## Typical physics experiment use
Bridges instrument software displays to downstream ROI/OCR processing when no supported device SDK is available.
<!-- section:measurement -->
## What it actually measures
User-authorized screen pixels and capture lifecycle/timing—not instrument internals, device SDK values or physical quantities.
<!-- section:sources -->
## Source projects
| Repository | Commit | Source paths / use |
| --- | --- | --- |
| [physics-experiment-bridge-mvp](https://github.com/WUHAO19831214/physics-experiment-bridge-mvp) | `8bba87df6475cae1e595fc925551db8bea83fb68` | `src/screen/ScreenCapturePanel.tsx`, `screenCaptureRuntime.ts`, `docs/SCREEN_CAPTURE_PIPELINE.md`; authorized screen→ROI/OCR |
| [ampere-force-visualizer-teacher-yanan](https://github.com/WUHAO19831214/ampere-force-visualizer-teacher-yanan) | `cb073e89d6d87129287030f1df08bd540504eb39` | `ScreenCapturePanel.tsx`, `docs/SENSOR_INTEGRATION.md`; Fy/Fz display pixel bridge |
<!-- section:how-it-works -->
## How it works
User gesture → `getDisplayMedia` permission → selected stream → video/canvas pixels → timing/status → screen `FramePacket`. A recorded backend provides deterministic replay without browser UI.
<!-- section:input -->
## Input
Browser permission/configuration or recorded RGBA frames, requested sampling interval and source ID.
<!-- section:output -->
## Output
Screen `FramePacket` with IDs, RGBA dimensions/pixels, artifact URI, timestamps and capture quality flags.
<!-- section:demo -->
## Demo
[![Recorded screen replay](assets/captured-screen-frame.png)](assets/README.md) Synthetic replay is not browser/device compatibility evidence.
<!-- section:example -->
## Minimal example
Run [web-screen-capture](../../examples/web-screen-capture/README.md); compose with OCR via [web-screen-to-ocr](../../examples/web-screen-to-ocr/README.md).
<!-- section:distribution -->
## Distribution / Download
TypeScript package `0.3.0`; [screen.capture-0.3.0.zip](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/screen.capture-0.3.0.zip). Bundle requires the shared tgz.
<!-- section:evidence -->
## Evidence level
`E1`: deterministic recorded RGBA replay; browser capture is not automatically exercised.
<!-- section:maturity -->
## Maturity
`experimental`; manifest `incubating/adapter-present`.
<!-- section:limitations -->
## Known limitations
Permission must be user initiated and normally repeats after reload. Denial/end are capture lifecycle errors. OCR is downstream and must report failures without mock values.
<!-- section:benchmark -->
## Benchmark
See [benchmark](benchmarks/README.md) and [compatibility matrix](../../docs/compatibility-matrix.md).
<!-- section:provenance -->
## Provenance
See [SOURCE.md](SOURCE.md) and [sensor.json](sensor.json).
