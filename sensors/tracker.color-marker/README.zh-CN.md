# 颜色标记视觉追踪软件传感器

[English](README.md) | **简体中文** | [日本語](README.ja.md)

Sensor ID: `tracker.color-marker` · Implementation version: `0.2.0` · Maturity: `experimental` · Evidence: `E2` · Release: `v0.6.0`

<!-- section:name -->
## 名称
颜色标记视觉追踪软件传感器
<!-- section:description -->
## 一句话介绍
在摄像头图像中寻找指定颜色标记，连续输出图像坐标位置与丢失状态。
<!-- section:physics-use -->
## 典型物理实验用途
追踪彩色球/标记，用于运动、振动、轨迹实验和声音—视觉对齐。
<!-- section:measurement -->
## 它实际测到什么
直接输出像素重心、轮廓/面积证据和检测状态。像素位置必须经过明确标定和时间推导后，才能得到位移、速度或振幅。
<!-- section:sources -->
## 来源项目
| 仓库 | Commit | 原文件/用途 |
| --- | --- | --- |
| [audio-visual-soundfield-tracker-stable](https://github.com/WUHAO19831214/audio-visual-soundfield-tracker-stable) | `85740d686c67452a057540edb564d713e01ccc51` | `tennis_ball_tracker.py::TennisBallTracker.update`、mask/candidate 函数和 tests；本轮抽取 profile |
| [physics-experiment-bridge-mvp](https://github.com/WUHAO19831214/physics-experiment-bridge-mvp) | `8bba87df6475cae1e595fc925551db8bea83fb68` | `ColorTrackingAnalyzer.ts`、`MarkerTrackingAnalyzer.ts`；相关浏览器 profile，本轮未抽取 |
<!-- section:how-it-works -->
## 工作原理
BGR frame → HSV → 阈值 mask → 形态学 → 轮廓候选 → 面积/圆度/连续性排序 → 重心平滑/丢失 → `SensorEvent`。
<!-- section:input -->
## 输入
Camera/image `FramePacket`、HSV 阈值、面积/圆度过滤、平滑和可选 ROI/连续性设置。
<!-- section:output -->
## 输出
Tracking `SensorEvent`：原始/平滑像素中心、归一化位置、bbox/面积/质量证据和明确 lost 状态。
<!-- section:demo -->
## Demo
[![颜色标记回放](assets/overview.png)](assets/README.md) Standalone synthetic 输出，不是真实实验精度声明。
<!-- section:example -->
## 最小示例
运行 [python-color-marker](../../examples/python-color-marker/README.md)，调用 `ColorMarkerSensor`。
<!-- section:distribution -->
## 分发 / 下载
Python package `0.5.0` + `color-marker`；[tracker.color-marker-0.2.0.zip](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.color-marker-0.2.0.zip)。
<!-- section:evidence -->
## 证据等级
`E2`：固定来源 commit 执行/golden 对比，以及确定性成功、丢失、重获测试。
<!-- section:maturity -->
## 成熟度
`experimental`；manifest 为 `incubating/adapter-present`。
<!-- section:limitations -->
## 已知限制
HSV 阈值依赖相机和光照；相似颜色、模糊、遮挡、曝光会导致误检/丢失。算法置信度不是物理不确定度。
<!-- section:benchmark -->
## Benchmark
见 [benchmark](benchmarks/README.md)：成功率、lost-frame rate、center error、latency/FPS 和来源输出兼容性。
<!-- section:provenance -->
## 来源追溯
抽取变更、来源符号、容差和 golden 方法见 [SOURCE.md](SOURCE.md)，事实见 [sensor.json](sensor.json)。
