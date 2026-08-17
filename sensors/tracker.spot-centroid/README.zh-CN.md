# 光斑重心识别软件传感器

[English](README.md) | **简体中文** | [日本語](README.ja.md)

Sensor ID: `tracker.spot-centroid` · Implementation version: `0.4.0` · Maturity: `experimental` · Evidence: `E2` · Release: `v0.6.0`

<!-- section:name -->
## 名称
光斑重心识别软件传感器
<!-- section:description -->
## 一句话介绍
寻找红色光斑，输出图像中的亮度加权重心以及质量/丢失证据。
<!-- section:physics-use -->
## 典型物理实验用途
在振动、共振和轨迹实验中观测投射/附着的红色光斑，再由下游分析振幅或频率。
<!-- section:measurement -->
## 它实际测到什么
红色候选像素、加权重心、bbox、权重和、过曝/ROI 边缘证据和 lost 状态；它**不直接测量**机械位移或振幅。
<!-- section:sources -->
## 来源项目
| 仓库 | Commit | 原文件/用途 |
| --- | --- | --- |
| [spot-vibration-tracking-system-20260508-171952](https://github.com/WUHAO19831214/spot-vibration-tracking-system-20260508-171952) | `7f0d91cc73afafaecc54acc46b2b9d69375d994a` | `app.js::rgbToHsv/trackRedSpot/getAmplitudeFrom`；红色加权重心与扫频窗口 |
| [forced-vibration-af-analyzer-20260502-122715](https://github.com/WUHAO19831214/forced-vibration-af-analyzer-20260502-122715) | `c3f58175a09ff29cacdfb976a5055758c4eff619` | 相同核心阈值/权重公式；受迫振动图像范围 |
<!-- section:how-it-works -->
## 工作原理
Frame/ROI → 来源兼容红通道阈值 → 逐像素亮度权重 → 加权和 → centroid/bbox/quality flags 或明确 lost → `SensorEvent`。
<!-- section:input -->
## 输入
Camera/image `FramePacket`、normalized ROI 和来源兼容红色阈值/质量配置。
<!-- section:output -->
## 输出
Centroid/tracking `SensorEvent`：像素/归一化重心、bbox、候选/权重证据，以及 `spot-lost`、`low-signal`、`overexposed`、`roi-edge` 等 flags。
<!-- section:demo -->
## Demo
[![光斑重心回放](assets/overview.png)](assets/README.md) Synthetic adapter 输出，不是真实实验标定证据。
<!-- section:example -->
## 最小示例
运行 [spot-centroid](../../examples/spot-centroid/README.md)，调用 `SpotCentroidSensor`。
<!-- section:distribution -->
## 分发 / 下载
Python package `0.5.0` + `classical-trackers`；[tracker.spot-centroid-0.4.0.zip](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.spot-centroid-0.4.0.zip)。
<!-- section:evidence -->
## 证据等级
`E2`：来源公式比较与 centroid/lost/quality 路径 golden replay。
<!-- section:maturity -->
## 成熟度
`experimental`；manifest 为 `incubating/adapter-present`。
<!-- section:limitations -->
## 已知限制
0.4.0 只实现来源 red-channel profile。曝光、弱光斑和 ROI 边缘会影响结果；重复性、不确定度和物理标定都没有 E4 证据。
<!-- section:benchmark -->
## Benchmark
见 [benchmark](benchmarks/README.md)：centroid pixel error、missing rate、曝光/ROI 敏感性和延迟。
<!-- section:provenance -->
## 来源追溯
固定来源函数/公式与比较结果见 [SOURCE.md](SOURCE.md)，事实见 [sensor.json](sensor.json)。
