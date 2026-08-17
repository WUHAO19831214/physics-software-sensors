# 屏幕采集软件传感器

[English](README.md) | **简体中文** | [日本語](README.ja.md)

Sensor ID: `screen.capture` · Implementation version: `0.3.0` · Maturity: `experimental` · Evidence: `E1` · Release: `v0.6.0`

<!-- section:name -->
## 名称
屏幕/窗口采集软件传感器
<!-- section:description -->
## 一句话介绍
采集用户选择的屏幕、窗口或标签页像素，输出带时间戳的 screen `FramePacket`。
<!-- section:physics-use -->
## 典型物理实验用途
当设备没有可用 SDK 时，把仪器软件显示桥接到后续 ROI/OCR 处理。
<!-- section:measurement -->
## 它实际测到什么
直接观测用户授权的屏幕像素与采集生命周期/时间，不是仪器内部数据、设备 SDK 数值或物理量。
<!-- section:sources -->
## 来源项目
| 仓库 | Commit | 原文件/用途 |
| --- | --- | --- |
| [physics-experiment-bridge-mvp](https://github.com/WUHAO19831214/physics-experiment-bridge-mvp) | `8bba87df6475cae1e595fc925551db8bea83fb68` | `ScreenCapturePanel.tsx`、`screenCaptureRuntime.ts`、`SCREEN_CAPTURE_PIPELINE.md`；授权屏幕→ROI/OCR |
| [ampere-force-visualizer-teacher-yanan](https://github.com/WUHAO19831214/ampere-force-visualizer-teacher-yanan) | `cb073e89d6d87129287030f1df08bd540504eb39` | `ScreenCapturePanel.tsx`、`SENSOR_INTEGRATION.md`；Fy/Fz 显示像素桥 |
<!-- section:how-it-works -->
## 工作原理
用户操作 → `getDisplayMedia` 授权 → 选定流 → video/canvas 像素 → 时间/状态 → screen `FramePacket`。Recorded backend 可脱离浏览器 UI 做确定性回放。
<!-- section:input -->
## 输入
浏览器授权/配置或 recorded RGBA 帧、请求采样间隔和 source ID。
<!-- section:output -->
## 输出
Screen `FramePacket`：ID、RGBA 尺寸/像素、artifact URI、时间戳和采集质量 flags。
<!-- section:demo -->
## Demo
[![屏幕回放](assets/captured-screen-frame.png)](assets/README.md) Synthetic replay 不证明浏览器/设备兼容性。
<!-- section:example -->
## 最小示例
运行 [web-screen-capture](../../examples/web-screen-capture/README.md)；与 OCR 组合见 [web-screen-to-ocr](../../examples/web-screen-to-ocr/README.md)。
<!-- section:distribution -->
## 分发 / 下载
TypeScript package `0.3.0`；[screen.capture-0.3.0.zip](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/screen.capture-0.3.0.zip)。Bundle 依赖公共 tgz。
<!-- section:evidence -->
## 证据等级
`E1`：确定性 recorded RGBA replay；不会自动执行浏览器采集。
<!-- section:maturity -->
## 成熟度
`experimental`；manifest 为 `incubating/adapter-present`。
<!-- section:limitations -->
## 已知限制
必须由用户操作触发授权，刷新后通常要重新授权。拒绝/结束属于采集生命周期错误。OCR 是下游处理，失败时不得返回 mock 数字。
<!-- section:benchmark -->
## Benchmark
见 [benchmark](benchmarks/README.md)和[兼容性矩阵](../../docs/compatibility-matrix.md)。
<!-- section:provenance -->
## 来源追溯
见 [SOURCE.md](SOURCE.md) 和 [sensor.json](sensor.json)。
