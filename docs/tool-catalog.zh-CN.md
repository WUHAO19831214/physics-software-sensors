# 配套工具目录

[English](tool-catalog.md) | **简体中文** | [日本語](tool-catalog.ja.md)

<!-- section:catalog -->
## 目录

Companion Tool（配套工具）处理已有观测或测量值；它不产生新的直接观测，也不计入 Sensor 数量。

| Tool | 用途 | 语言 | 状态 | 来源 | Example | 文档 |
| --- | --- | --- | --- | --- | --- | --- |
| [`vector.compose-3d`](../processing/vector.compose-3d/README.zh-CN.md) | 把带来源语义的 x/y/z 标量分量合成为三维矢量和可选渲染模型 | TypeScript | `experimental` `0.1.0` | 延安安培力教师端 | [Web demo](../examples/web-vector-compose-3d/README.md) | [来源记录](../processing/vector.compose-3d/SOURCE.md) |
| [`calibration.scale-1d`](../processing/calibration.scale-1d/README.zh-CN.md) | 人工确认的两点及分段多点一维标定 | TypeScript | experimental 0.1.0 | FringeLab | [Web demo](../examples/web-fringelab-toolkit/README.md) | [Source](../processing/calibration.scale-1d/SOURCE.md) |
| [`signal.profile-features`](../processing/signal.profile-features/README.zh-CN.md) | 平滑、背景扣除、峰谷、峰宽与周期分析 | TypeScript | experimental 0.1.0 | FringeLab | [Web demo](../examples/web-fringelab-toolkit/README.md) | [Source](../processing/signal.profile-features/SOURCE.md) |
| [`optics.fringe-wavelength`](../processing/optics.fringe-wavelength/README.zh-CN.md) | 干涉/衍射波长反演、回归与不确定度 | TypeScript | experimental 0.1.0 | FringeLab | [Web demo](../examples/web-fringelab-toolkit/README.md) | [Source](../processing/optics.fringe-wavelength/SOURCE.md) |

<!-- section:status -->
## 状态边界

仓库清单：**9 个 Sensor · 4 个 Companion Tool**。该工具属于不可变 `v0.6.0` 之后的未发布开发，不在该 Release 中，也不改变任何 Sensor 的成熟度或证据等级。
