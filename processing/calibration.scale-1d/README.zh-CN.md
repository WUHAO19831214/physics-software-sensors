# 确认两点与多点局部标定

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

`calibration.scale-1d` · `0.1.0` · experimental · unreleased

<!-- section:name -->
## Name

确认两点与多点局部标定

<!-- section:purpose -->
## Purpose

确认两点与多点局部标定；处理已有观测，不生成新的直接观测。

<!-- section:boundary -->
## Boundary

确认两点与多点局部标定；处理已有观测，不生成新的直接观测。

<!-- section:source -->
## Source

https://github.com/WUHAO19831214/webcam-laser-fringelab · `37a8b3996791790a22980b0d562996a65a3a65ef` · lib/ruler.ts, lib/spatial.ts

<!-- section:input -->
## Input

pixel points + known mm readings + source/calibration IDs

<!-- section:output -->
## Output

position mm, extrapolation and stale status

<!-- section:example -->
## Example

```ts
import { confirmTwoPointCalibration, calibratedPosition,
  confirmMultiPointCalibration } from '@physics-software-sensors/fringelab';
const scale = confirmTwoPointCalibration({ start: { x: 20, y: 40 },
  end: { x: 120, y: 40 }, knownLengthMm: 10 }, 'photo:1', 'scale:1');
const position = calibratedPosition({ x: 70, y: 40 }, scale, 'photo:1');
// position.valueMm === 5; a different source key returns stale/null.
const localScale = confirmMultiPointCalibration([
  { x: 0, y: 0, mm: 0 }, { x: 100, y: 0, mm: 10 },
  { x: 220, y: 0, mm: 20 }
], 'photo:1', 'scale:2');
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
