# 一维信号特征

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

`signal.profile-features` · `0.1.0` · experimental · unreleased

<!-- section:name -->
## Name

一维信号特征

<!-- section:purpose -->
## Purpose

一维信号特征；处理已有观测，不生成新的直接观测。

<!-- section:boundary -->
## Boundary

一维信号特征；处理已有观测，不生成新的直接观测。

<!-- section:source -->
## Source

https://github.com/WUHAO19831214/webcam-laser-fringelab · `37a8b3996791790a22980b0d562996a65a3a65ef` · lib/signal.ts

<!-- section:input -->
## Input

finite signal array + axis/sample semantics + processing options

<!-- section:output -->
## Output

processed profile, peak/trough centers, widths and periods

<!-- section:example -->
## Example

```ts
import { Signal } from '@physics-software-sensors/fringelab';
const samples = Float64Array.from([0, 1, 3, 8, 13, 8, 3, 1, 0]);
const smoothed = Signal.gaussianSmooth(samples, 0.8);
const peaks = Signal.detectPeaks(smoothed, { minProminence: 2, minDistance: 3 });
const period = Signal.estimatePeriodAutocorrelation(smoothed);
// A short signal need not contain a measurable period. Widths are in samples;
// convert using the original pixel axis and confirmed scale, not display size.
```

[Runnable example](../../examples/web-fringelab-toolkit/README.md)

<!-- section:quality -->
## Quality

保留过曝、确认状态、来源版本与输入误差；失效数据不能冒充当前测量。

<!-- section:coordinates -->
## Coordinates

原图像素、毫米标定与以米为单位的光学模型；不隐含二维透视校正。

<!-- section:demo -->
## Demo

独立浏览器运行，图像本地处理。 [Demo](../../examples/web-fringelab-toolkit/README.md)

<!-- section:status -->
## Status

experimental；证据等级不等于测量准确度认证。 Version 0.1.0, unreleased; v0.6.0 unchanged.

<!-- section:limitations -->
## Limitations

不输出 lux/W/m²；保留通道、饱和与有效样本覆盖。 毫米刻线模型存在周期歧义；OCR 和尺度需人工确认。一维标定不是二维透视校正。

<!-- section:provenance -->
## Provenance

[SOURCE.md](SOURCE.md)
