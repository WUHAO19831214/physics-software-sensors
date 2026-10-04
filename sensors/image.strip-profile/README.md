# Relative Image Strip Profile

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

`image.strip-profile` · `0.1.0` · experimental · E2 · unreleased

<!-- section:name -->
## Name

Relative Image Strip Profile

<!-- section:description -->
## Description

Observe a rotated RGBA strip as relative camera response.

<!-- section:physics-use -->
## Physics Use

Useful in diffraction, image profiles and optical measurement.

<!-- section:measurement -->
## Measurement

Relative DN, sample coverage and pixel axis; not calibrated intensity.

<!-- section:sources -->
## Sources

https://github.com/WUHAO19831214/webcam-laser-fringelab · `37a8b3996791790a22980b0d562996a65a3a65ef` · lib/signal.ts

<!-- section:how-it-works -->
## How It Works

Source is pinned; relative import changes only.

<!-- section:input -->
## Input

Original-image RGBA FramePacket, explicit ROI and options.

<!-- section:output -->
## Output

SensorEvent with profile/channel/coverage payload.

<!-- section:demo -->
## Demo

Standalone browser runtime; all images stay local. [Demo](../../examples/web-fringelab-toolkit/README.md)

<!-- section:example -->
## Example

```ts
import { StripProfileSensor } from '@physics-software-sensors/fringelab/sensors';
// frame: RuntimeFramePacket containing native RGBA pixels from any source.
const sensor = new StripProfileSensor();
const configured = sensor.configure({ channel: 'r', roi: { centerX: 480, centerY: 270, width: 700, height: 50, angleDeg: 0 } });
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

No lux/W/m². Keep channel, source clipping and sample coverage.

<!-- section:benchmark -->
## Benchmark

[Benchmark record](../../benchmarks/results/fringelab-extraction-2026-10-05.md)

<!-- section:provenance -->
## Provenance

[SOURCE.md](SOURCE.md)
