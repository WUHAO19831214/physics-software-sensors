# 相对图像响应剖面

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

`image.strip-profile` · `0.1.0` · experimental · E2 · unreleased

<!-- section:name -->
## Name

相对图像响应剖面

<!-- section:description -->
## Description

从旋转 RGBA 带状选区采样相对相机响应。

<!-- section:physics-use -->
## Physics Use

适用于衍射、图像剖面与光学测量。

<!-- section:measurement -->
## Measurement

Relative DN, sample coverage and pixel axis; not calibrated intensity.

<!-- section:sources -->
## Sources

https://github.com/WUHAO19831214/webcam-laser-fringelab · `37a8b3996791790a22980b0d562996a65a3a65ef` · lib/signal.ts

<!-- section:how-it-works -->
## How It Works

固定源码提交，算法只调整相对导入。

<!-- section:input -->
## Input

原图 RGBA FramePacket、显式 ROI 与选项。

<!-- section:output -->
## Output

SensorEvent with profile/channel/coverage payload.

<!-- section:demo -->
## Demo

独立浏览器运行，图像本地处理。 [Demo](../../examples/web-fringelab-toolkit/README.md)

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

TypeScript 包与源码可用，不包含在 v0.6.0 中。 [Package](../../packages/fringelab/README.md)

<!-- section:evidence -->
## Evidence

固定来源对照 E2；真实设备 E4 与下游 E5 尚未测量。

<!-- section:maturity -->
## Maturity

experimental；证据等级不等于测量准确度认证。

<!-- section:limitations -->
## Limitations

不输出 lux/W/m²；保留通道、饱和与有效样本覆盖。

<!-- section:benchmark -->
## Benchmark

[Benchmark record](../../benchmarks/results/fringelab-extraction-2026-10-05.md)

<!-- section:provenance -->
## Provenance

[SOURCE.md](SOURCE.md)
