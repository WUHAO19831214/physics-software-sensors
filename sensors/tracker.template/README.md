# Template / Single-Object Tracker

## 模板/单目标追踪软件传感器

> 由用户在首帧指定一个实验物体区域，并在后续图像中持续输出它的边界框、中心和丢失状态。

**状态：contract-only** · **Sensor ID：** `tracker.template` · **版本：** `0.1.0`

## 典型物理实验用途

声音—视觉稳定版允许选择自定义物体 ROI 后用 OpenCV CSRT/KCF/MIL 追踪，得到图像轨迹；多源实验桥另有浏览器 template-matching 策略。两者不是同一个算法，后续必须分 profile 验证。像素轨迹需标定后才能解释为物理位移。

## 来源项目

| 项目 | 仓库 | commit | 原实现文件 | 用途 |
| --- | --- | --- | --- | --- |
| 声音—视觉稳定版 | [`audio-visual-soundfield-tracker-stable`](https://github.com/WUHAO19831214/audio-visual-soundfield-tracker-stable) | `85740d686c67452a057540edb564d713e01ccc51` | `src/object_template_tracker.py`、对应 tests | CSRT→KCF→MIL 单目标追踪 |
| 多源实验桥 | [`physics-experiment-bridge-mvp`](https://github.com/WUHAO19831214/physics-experiment-bridge-mvp) | `8bba87df6475cae1e595fc925551db8bea83fb68` | `src/vision/TemplateMatchingAnalyzer.ts` | 浏览器模板匹配策略 |

## 工作原理

```text
首帧 + ROI → tracker 初始化 → 后续帧 update → bbox/center 或 lost → SensorEvent
```

## 输入

图像帧、初始化 ROI、tracker backend/模板配置。

## 输出

目标输出为 bbox、中心、backend、track ID、lost count 和回退标志。

## 使用效果

**demo asset pending**。见 [assets](assets/README.md)。

## 最小调用示例

目标 API（尚不可运行）：`TemplateTracker.initialize(frame, roi)` / `process(frame)`。

## 当前成熟度

contract-only；Phase 3 在 spot-centroid 后实现。

## 已知限制

遮挡、尺度/旋转变化、运动模糊和出画会导致丢失；CSRT/KCF/MIL 回退改变性能；ROI tracker 不等于静态模板匹配。

## Benchmark

见 [benchmarks](benchmarks/README.md)。

## Provenance

[SOURCE.md](SOURCE.md) · [sensor.json](sensor.json)
