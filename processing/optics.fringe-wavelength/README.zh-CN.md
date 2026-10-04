# 光学条纹波长反演

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

`optics.fringe-wavelength` · `0.1.0` · experimental · unreleased

<!-- section:name -->
## Name

光学条纹波长反演

<!-- section:purpose -->
## Purpose

光学条纹波长反演；处理已有观测，不生成新的直接观测。

<!-- section:boundary -->
## Boundary

光学条纹波长反演；处理已有观测，不生成新的直接观测。

<!-- section:source -->
## Source

https://github.com/WUHAO19831214/webcam-laser-fringelab · `37a8b3996791790a22980b0d562996a65a3a65ef` · lib/physics.ts, lib/analysis.ts

<!-- section:input -->
## Input

calibrated positions, confirmed orders and a/d/L/errors

<!-- section:output -->
## Output

wavelength, regression, method/quality and uncertainty

<!-- section:example -->
## Example

```ts
import { Optics } from '@physics-software-sensors/fringelab';
const fit = Optics.fitDoubleSlitOrders({
  observations: [-2, -1, 0, 1, 2].map(order => ({
    order, screenPositionM: order * 0.0039
  })),
  screenDistanceM: 1.5,
  slitSeparationM: 0.00025,
  centerPositionM: 0
});
// Orders and metre positions must come from an explicitly confirmed workflow.
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
