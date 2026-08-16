# YOLO Tracker

## YOLO 检测与追踪软件传感器

> 用本地 YOLO 模型检测摄像头图像中的目标，并在支持时用 ByteTrack 给连续帧目标分配 track ID。

**状态：contract-only** · **Sensor ID：** `tracker.yolo` · **版本：** `0.1.0`

## 典型物理实验用途

声音—视觉稳定版用 YOLOv8 + ByteTrack 追踪人物中心，为视觉—声音同步轨迹提供图像位置；模型缺失或失败时可声明回退 OpenCV HOG。输出是图像检测/轨迹，不是三维位置或米制坐标。

## 来源项目

| 项目 | 仓库 | commit | 原实现文件 | 用途 |
| --- | --- | --- | --- | --- |
| 声音—视觉稳定版 | [`audio-visual-soundfield-tracker-stable`](https://github.com/WUHAO19831214/audio-visual-soundfield-tracker-stable) | `85740d686c67452a057540edb564d713e01ccc51` | `src/detector.py`、`camera_processor.py`、对应 tests | YOLO/ByteTrack 人物检测追踪及 HOG 回退 |

## 工作原理

```text
图像帧 → 模型推理 → 类别/置信度过滤 → ByteTrack ID → bbox/center → SensorEvent
```

## 输入

图像帧、模型 artifact + SHA-256、类别/置信度、tracker 配置和后端策略。

## 输出

目标输出为类别、confidence、bbox、中心、track ID、backend 和回退质量标志。

## 使用效果

**demo asset pending**。见 [assets](assets/README.md)。

## 最小调用示例

目标 API（尚不可运行）：`YoloTracker(model_artifact=...).process(frame)`。

## 当前成熟度

contract-only；按 Phase 3 顺序最后处理，以便先完成权重许可证和后端解耦。

## 已知限制

模型权重不随库默认分发；Ultralytics、ByteTrack、HOG 结果不可混报；不同 backend 的 track ID 和精度不同；模型许可需单独审核。

## Benchmark

见 [benchmarks](benchmarks/README.md)。

## Provenance

[SOURCE.md](SOURCE.md) · [sensor.json](sensor.json)
