# Physical Ruler Tick Candidates

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

`vision.ruler-ticks` · `0.1.0` · experimental · E2 · unreleased

<!-- section:name -->
## Name

Physical Ruler Tick Candidates

<!-- section:description -->
## Description

Locate physical ruler ticks and return unconfirmed candidates.

<!-- section:physics-use -->
## Physics Use

Useful for assisted image-scale measurement with manual and multi-point fallback.

<!-- section:measurement -->
## Measurement

Tick pixel position; fitted mm-per-pixel is an unconfirmed model-dependent inference.

<!-- section:sources -->
## Sources

https://github.com/WUHAO19831214/webcam-laser-fringelab · `37a8b3996791790a22980b0d562996a65a3a65ef` · lib/ruler-detection.ts, lib/ruler.worker.ts, lib/ruler-ocr.ts

<!-- section:how-it-works -->
## How It Works

Source is pinned; relative import changes only.

<!-- section:input -->
## Input

Original-image RGBA FramePacket, explicit ROI and options.

<!-- section:output -->
## Output

SensorEvent with candidate/ticks/residuals and calibration_applied=false.

<!-- section:demo -->
## Demo

Standalone browser runtime; all images stay local. [Demo](../../examples/web-fringelab-toolkit/README.md)

<!-- section:example -->
## Example

```ts
import { RulerTicksSensor } from '@physics-software-sensors/fringelab/sensors';
// frame: RuntimeFramePacket containing native RGBA pixels from any source.
const sensor = new RulerTicksSensor();
const configured = sensor.configure({ region: { x: 80, y: 390, width: 750, height: 110 } });
if (!configured.accepted) throw new Error(configured.warnings.join('; '));
await sensor.start({ runId: frame.runId });
for await (const event of sensor.process(frame)) console.log(event);
await sensor.stop();
```

[Runnable example](../../examples/web-fringelab-toolkit/README.md)

<!-- section:distribution -->
## Distribution

Core and TypeScript package; not included in v0.6.0. [Package](../../packages/fringelab/README.md)

<!-- section:evidence -->
## Evidence

Source-compatible golden E2; real-device E4 and downstream E5 not measured.

<!-- section:maturity -->
## Maturity

experimental; evidence does not imply metrological validation.

<!-- section:limitations -->
## Limitations

Millimetre tick model; possible period ambiguity; OCR/scale require human confirmation. One-dimensional calibration is not homography.

<!-- section:benchmark -->
## Benchmark

[Benchmark record](../../benchmarks/results/fringelab-extraction-2026-10-05.md)

<!-- section:provenance -->
## Provenance

[SOURCE.md](SOURCE.md)
