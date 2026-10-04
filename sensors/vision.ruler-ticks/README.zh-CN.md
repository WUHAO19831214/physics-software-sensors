# 实物尺刻线候选

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

`vision.ruler-ticks` · `0.1.0` · experimental · E2 · unreleased

<!-- section:name -->
## Name

实物尺刻线候选

<!-- section:description -->
## Description

定位实物尺刻线并输出待确认候选。

<!-- section:physics-use -->
## Physics Use

适用于辅助图像标定，保留手动和多点回退。

<!-- section:measurement -->
## Measurement

Tick pixel position; fitted mm-per-pixel is an unconfirmed model-dependent inference.

<!-- section:sources -->
## Sources

https://github.com/WUHAO19831214/webcam-laser-fringelab · `37a8b3996791790a22980b0d562996a65a3a65ef` · lib/ruler-detection.ts, lib/ruler.worker.ts, lib/ruler-ocr.ts

<!-- section:how-it-works -->
## How It Works

固定源码提交，算法只调整相对导入。

<!-- section:input -->
## Input

原图 RGBA FramePacket、显式 ROI 与选项。

<!-- section:output -->
## Output

SensorEvent with candidate/ticks/residuals and calibration_applied=false.

<!-- section:demo -->
## Demo

独立浏览器运行，图像本地处理。 [Demo](../../examples/web-fringelab-toolkit/README.md)

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

TypeScript 包与源码可用，不包含在 v0.6.0 中。 [Package](../../packages/fringelab/README.md)

<!-- section:evidence -->
## Evidence

固定来源对照 E2；真实设备 E4 与下游 E5 尚未测量。

<!-- section:maturity -->
## Maturity

experimental；证据等级不等于测量准确度认证。

<!-- section:limitations -->
## Limitations

毫米刻线模型存在周期歧义；OCR 和尺度需人工确认。一维标定不是二维透视校正。

<!-- section:benchmark -->
## Benchmark

[Benchmark record](../../benchmarks/results/fringelab-extraction-2026-10-05.md)

<!-- section:provenance -->
## Provenance

[SOURCE.md](SOURCE.md)
