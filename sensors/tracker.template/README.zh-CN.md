# 模板 / 单目标视觉追踪软件传感器

[English](README.md) | **简体中文** | [日本語](README.ja.md)

Sensor ID: `tracker.template` · Implementation version: `0.4.0` · Maturity: `experimental` · Evidence: `E3` · Release: `v0.6.0`

<!-- section:name -->
## 名称
模板 / 单目标视觉追踪软件传感器
<!-- section:description -->
## 一句话介绍
从 ROI 初始化一个目标，使用 OpenCV CSRT/KCF/MIL fallback 追踪其图像边界框。
<!-- section:physics-use -->
## 典型物理实验用途
当颜色分割不适合时，在运动或振动实验中连续追踪一个可见目标。
<!-- section:measurement -->
## 它实际测到什么
直接输出图像 bbox/中心以及 tracking/lost/backend 状态。当前实现不是静态模板匹配，像素运动也不是未标定的物理位移。
<!-- section:sources -->
## 来源项目
| 仓库 | Commit | 原文件/用途 |
| --- | --- | --- |
| [audio-visual-soundfield-tracker-stable](https://github.com/WUHAO19831214/audio-visual-soundfield-tracker-stable) | `85740d686c67452a057540edb564d713e01ccc51` | `object_template_tracker.py::initialize/update/reset/create_opencv_tracker/validate_bbox` 与 tests；本轮抽取 ROI tracker |
| [physics-experiment-bridge-mvp](https://github.com/WUHAO19831214/physics-experiment-bridge-mvp) | `8bba87df6475cae1e595fc925551db8bea83fb68` | `TemplateMatchingAnalyzer.ts`；相关静态 matching profile，本轮未抽取 |
<!-- section:how-it-works -->
## 工作原理
初始化帧 + ROI 校验 → 选择 CSRT→KCF→MIL backend → 逐帧 `update` → bbox/center 或 lost → 可选重新初始化 → `SensorEvent`。
<!-- section:input -->
## 输入
Camera/image `FramePacket`、初始化 ROI 和可选 backend preference。当前实现不要求 template asset。
<!-- section:output -->
## 输出
Tracking `SensorEvent`：bbox、center、requested/actual backend、fallback 尝试、初始化/重初始化和 lost 状态。OpenCV 不提供已标定置信度。
<!-- section:demo -->
## Demo
[![ROI tracker replay](assets/overview.png)](assets/README.md) 真实 OpenCV runtime 在 synthetic targets 上运行，不是真实实验精度。
<!-- section:example -->
## 最小示例
运行 [python-template-tracker](../../examples/python-template-tracker/README.md)，调用 `TemplateTrackerSensor`。
<!-- section:distribution -->
## 分发 / 下载
Python package `0.5.0` + `classical-trackers`；[tracker.template-0.4.0.zip](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.template-0.4.0.zip)。
<!-- section:evidence -->
## 证据等级
`E3`：真实 OpenCV contrib tracker 已在受控 synthetic/scripted sequence 上执行。
<!-- section:maturity -->
## 成熟度
`experimental`；manifest 为 `incubating/adapter-present`。
<!-- section:limitations -->
## 已知限制
Fallback 会改变行为/性能；遮挡、缩放、模糊和无效 ROI 可能导致 lost。没有已标定置信度、物理尺度或 E4 真实设备证据。
<!-- section:benchmark -->
## Benchmark
见 [benchmark](benchmarks/README.md)：初始化/update 成功、bbox/center error、lost/reinitialize、backend 和 latency。
<!-- section:provenance -->
## 来源追溯
算法家族边界、来源符号和比较见 [SOURCE.md](SOURCE.md)，事实见 [sensor.json](sensor.json)。
