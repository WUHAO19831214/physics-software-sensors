# YOLO 检测与追踪软件传感器

[English](README.md) | **简体中文** | [日本語](README.ja.md)

Sensor ID: `tracker.yolo` · Implementation version: `0.5.0` · Maturity: `experimental` · Evidence: `E2` · Release: `v0.6.0`

<!-- section:name -->
## 名称
YOLO 检测与追踪软件传感器
<!-- section:description -->
## 一句话介绍
把多目标 detector/tracker 后端结果转换为可追溯的 detection、bbox 和 Track ID。
<!-- section:physics-use -->
## 典型物理实验用途
在适合使用已审核本地模型/runtime 时，观测多个可见物体或人员的图像轨迹。
<!-- section:measurement -->
## 它实际测到什么
直接输出 class label、detector confidence、bbox/center 和 backend Track ID。Confidence 不是准确率、tracking confidence 或物理不确定度；像素必须标定后才能得到物理量。
<!-- section:sources -->
## 来源项目
| 仓库 | Commit | 原文件/用途 |
| --- | --- | --- |
| [audio-visual-soundfield-tracker-stable](https://github.com/WUHAO19831214/audio-visual-soundfield-tracker-stable) | `85740d686c67452a057540edb564d713e01ccc51` | `detector.py::Detector.detect/track/_detect_hog`、`camera_processor.py`、config/setup/model docs/tests；YOLO/ByteTrack 与 HOG fallback 边界 |
<!-- section:how-it-works -->
## 工作原理
Frame → 选择 backend → 适用时校验 model artifact → detection → 可选 ByteTrack/recorded Track ID → adapter 标准结果/fallback 证据 → `SensorEvent`。
<!-- section:input -->
## 输入
Camera/image `FramePacket`、backend 配置、class filter；真实 YOLO 还必须提供已审核的本地 `ModelArtifact` 路径/SHA-256/许可证状态。
<!-- section:output -->
## 输出
Detection/tracking `SensorEvent`：每个目标的 class ID/name、bbox/center、detector confidence、可选 Track ID，以及 requested/actual/attempted backend 元数据。
<!-- section:demo -->
## Demo
[![Recorded detector replay](assets/overview.png)](assets/README.md) 这是来源兼容 recorded output，不是真实 YOLO inference 或模型准确率证据。
<!-- section:example -->
## 最小示例
运行 [python-yolo-tracker](../../examples/python-yolo-tracker/README.md)，使用不会下载模型的 `RecordedDetectorBackend`。
<!-- section:distribution -->
## 分发 / 下载
Python package `0.5.0`；offline `yolo-recorded`；[tracker.yolo-0.5.0.zip](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.yolo-0.5.0.zip)。真实 `yolo-runtime` 独立安装。
<!-- section:evidence -->
## 证据等级
`E2`：固定来源 recorded output 和 adapter/fallback/lifecycle tests。没有执行真实 Ultralytics/ByteTrack inference。
<!-- section:maturity -->
## 成熟度
`experimental`；manifest 为 `incubating/adapter-present`。
<!-- section:limitations -->
## 已知限制
不捆绑或自动下载 `.pt`/`.onnx`/`.engine`。HOG 仅限 person 且不等价于 YOLO。模型准确率、真实 ByteTrack 行为和实验室/设备性能均未测量。
<!-- section:benchmark -->
## Benchmark
见 [benchmark](benchmarks/README.md)：adapter/来源兼容性、多目标/lost/fallback 语义和延迟；模型准确率仍为 not measured。
<!-- section:provenance -->
## 来源追溯
来源符号、模型/许可证边界和 replay 构造见 [SOURCE.md](SOURCE.md)及 [YOLO 审查](../../docs/yolo-model-and-license-review.md)，事实见 [sensor.json](sensor.json)。
