# YOLO Detection and Tracking Sensor

## YOLO 检测与追踪软件传感器

> 从摄像头或图像帧中检测多个目标，并在追踪模式下输出跨帧 track ID；模型、运行时和权重始终作为独立、可审计的 artifact 管理。

**状态：experimental** · **Sensor ID：** `tracker.yolo` · **实现版本：** `0.5.0`

## 典型物理实验用途

声音—视觉同步采集稳定版使用 YOLOv8 + ByteTrack 追踪人物中心，为声音与视觉轨迹对齐提供图像位置。该传感器直接测到的是每一帧中的类别、检测框、中心像素和可用的轨迹 ID，可供运动轨迹、活动范围或多目标时序分析使用。

它不直接输出三维位置、米制位移、速度、声场强度或实验精度。`center.x/y` 是图像 pixel；只有通过另外记录的空间标定、镜头模型和时间处理，应用才能推导物理量。

## 来源项目

| 项目 | 仓库 | commit | 原实现文件 | 原始类/函数 | 实际用途 |
| --- | --- | --- | --- | --- | --- |
| 声音—视觉同步采集稳定版 | [`audio-visual-soundfield-tracker-stable`](https://github.com/WUHAO19831214/audio-visual-soundfield-tracker-stable) | `85740d686c67452a057540edb564d713e01ccc51` | `src/detector.py` | `Detection`；`Detector.__init__/detect/track/_detect_hog` | 本地 YOLO 人物检测、ByteTrack ID、模型失败时 HOG 人物检测 |
| 同上 | 同上 | 同上 | `src/camera_processor.py` | `CentroidTracker.update/reset`；`CameraProcessor._update_tracks` | native ID 不完整或 HOG 模式下的最近重心关联 |
| 同上 | 同上 | 同上 | `requirements.txt`、`config.yaml`、`scripts/setup_yolo.sh`、`models/README.md`、来源 tests | 依赖范围、`bytetrack.yaml`、person-only 默认、显式模型准备和已有覆盖 | 确认模型路径、下载边界与配置 |

完整文件级映射见 [SOURCE.md](SOURCE.md)，模型与第三方许可审查见 [YOLO model and license review](../../docs/yolo-model-and-license-review.md)。

## 工作原理

```text
CameraSource / recorded image
  ↓
FramePacket (BGR pixels + time/provenance)
  ↓
YoloTrackerSensor
  ↓
DetectorBackend
  ├─ RecordedDetectorBackend (offline golden/replay)
  ├─ YoloDetectorBackend + explicit local ModelArtifact
  │    ├─ detect: Ultralytics YOLO predict
  │    └─ track: Ultralytics YOLO + bytetrack.yaml
  └─ OpenCVHogDetectorBackend (declared person-only fallback)
  ↓
class/confidence filter → detections[] → SensorEvent
```

## Detection 与 Tracking

- **Detection** 是单帧识别，输出当前帧的类别、bbox、中心和 detector score；不承诺跨帧身份。
- **Tracking** 是跨帧身份关联。来源通过 `model.track(..., persist=True, tracker="bytetrack.yaml")` 请求 ByteTrack ID。
- `detector_confidence` 只是 detector 对当前 detection 的 backend score；它不是 tracking confidence、物理测量 uncertainty、实验精度或标定后的概率。因此顶层 `quality.confidence` 保持 `null`。

来源没有自定义 ByteTrack YAML 参数，而是引用运行时自带 `bytetrack.yaml`。Phase 3C 测试覆盖 recorded 的单目标、移动、双目标、短暂消失、重现和 ID reset/生命周期，同时覆盖 ByteTrack 异常后的 deterministic centroid association；**没有把 recorded ID 序列描述成真实 ByteTrack 性能验证**。真实运行时参数和版本必须在将来的 inference report 中锁定。

## ModelArtifact

模型权重不是 Sensor 本身。`ModelArtifact` 记录：`model_id`、`model_family`、本地 `uri`、精确 `sha256`、`runtime`、`runtime_version`、`class_names` 和 `license_state`。

`YoloDetectorBackend` 只接受显式本地 artifact，拒绝 HTTP(S) URI，并在加载前核对 SHA-256；不会因 import、start、example 或 test 自动下载模型。Phase 3C 不含任何 `.pt`/`.onnx`/`.engine`。

## 输入

- 已启动的 `RuntimeFrame` / FramePacket，pixel payload 为 BGR image；
- `tracking`（默认 true）；
- `confidence_threshold`（来源兼容默认 `0.25`）；
- class filter：`all`、class ID 数组或 class name 数组；
- 可选真实 backend 的本地 `ModelArtifact` 与 tracker 名称；
- recorded backend 的固定 detection fixture，供离线测试/示例使用。

来源应用默认 `person_only=true`；独立 adapter 为复用性提供三种 filter，并把实际 filter 写进每个事件。name filter 在 backend 输出后执行；ID filter 可同时传给支持它的 YOLO runtime。

## 多目标输出

一个事件只使用一个 `payload.detections` 数组，不创建 `center_x_1` 等动态字段。bbox 和 center 均位于事件声明的 `image-pixel` 坐标系。

```json
{
  "sensor": {"id": "tracker.yolo", "version": "0.5.0", "category": "processor"},
  "status": "ok",
  "measurements": [
    {"name": "detection_count", "value": 2, "value_type": "number", "unit": "1", "role": "raw", "uncertainty": null},
    {"name": "tracked_count", "value": 2, "value_type": "number", "unit": "1", "role": "derived", "uncertainty": null}
  ],
  "quality": {"confidence": null, "flags": [], "dropped_since_last": 0},
  "payload": {
    "tracking_mode": "bytetrack",
    "requested_backend": "ultralytics-yolo-bytetrack",
    "actual_backend": "ultralytics-yolo-bytetrack",
    "attempted_backends": ["ultralytics-yolo-bytetrack"],
    "class_filter": {"mode": "all", "values": []},
    "detections": [
      {"track_id": 7, "tracking_id_available": true, "class_id": 0, "class_name": "person", "bbox": {"x": 20.0, "y": 20.0, "width": 100.0, "height": 200.0}, "center": {"x": 70.0, "y": 120.0}, "detector_confidence": 0.9},
      {"track_id": 12, "tracking_id_available": true, "class_id": 1, "class_name": "sports ball", "bbox": {"x": 220.0, "y": 100.0, "width": 50.0, "height": 50.0}, "center": {"x": 245.0, "y": 125.0}, "detector_confidence": 0.82}
    ]
  }
}
```

零目标返回 `status: "lost"`、空数组和 `no-target`，绝不制造 detection。backend 失败返回显式 error/fallback 信息。

## Fallback 边界

固定来源真实存在 `YOLO → OpenCV HOG` 回退。事件始终记录 `requested_backend`、`actual_backend`、`attempted_backends` 和 `fallback_reason`，并在变化时产生 `detector-backend-fallback`。

HOG 使用 OpenCV 默认 people detector，只能提供 person-like detection，不识别通用 YOLO 类别，也不原生提供 ByteTrack ID。追踪模式下 adapter 可使用来源兼容的最近重心关联，并用 `tracking-id-not-native` 标记。ByteTrack 失败但 YOLO detection 可用时也使用该关联。两者不能混报为等价能力或精度。

## 使用效果

![Recorded detector replay: zero, single and multiple targets](assets/overview.png)

[multiple targets](assets/multi-target.png) · [tracking/lost/reappear](assets/tracking.png) · [declared HOG fallback](assets/fallback.png) · [recorded SensorEvents](assets/events.json)

这些图片来自本仓库 synthetic frame + 固定来源执行型 detection fixture 的 offline replay，均标记 **Recorded detector replay**。它们不是实际 YOLO inference 截图、人物数据或 accuracy 证据。生成方法和 SHA-256 见 [assets/README.md](assets/README.md)。

## 最小调用示例

离线、确定性 example：

```bash
python examples/python-yolo-tracker/run.py --backend recorded
```

公共 API：

```python
from physics_sensors.core import ModelArtifact, SensorContext
from physics_sensors.tracking import YoloDetectorBackend, YoloTrackerSensor

artifact = ModelArtifact(
    model_id="maintainer-reviewed-model", model_family="YOLOv8",
    uri="/absolute/path/to/model.pt", sha256="<exact sha256>",
    runtime="ultralytics", runtime_version="<installed exact version>",
    class_names=("person",), license_state="<artifact-specific review>",
)
sensor = YoloTrackerSensor(YoloDetectorBackend(artifact))
sensor.configure({"tracking": True, "class_filter": {"mode": "names", "values": ["person"]}})
await sensor.start(SensorContext.minimal("experiment-001"))
event = sensor.process_frame(camera_frame)
await sensor.stop()
```

真实 backend 命令、依赖和不联网边界见 [standalone example](../../examples/python-yolo-tracker/README.md)。

## 当前成熟度

`experimental` / manifest `incubating` / `adapter-present`：已有独立 Python API、ModelArtifact 边界、recorded backend、来源执行型 golden、HOG offline smoke、CameraSource composition、fallback/lifecycle tests、demo 和微基准。真实 Ultralytics inference **未执行**：没有提供经维护者批准的本地模型 artifact，且当前开发环境未安装 runtime；项目禁止用联网下载绕过此边界。

## 已知限制

- 当前证据是 synthetic/replay 和 fake runtime seam，不是模型 accuracy、ByteTrack 指标或真实实验验证；
- 没有正式标注集，因此 precision、recall、mAP、HOTA、IDF1、ID switches 均为 `not measured`；
- 模型/类别/训练数据会改变检测范围；权重许可证必须逐 artifact 审查；
- track ID 只在同一次已启动的 sensor session 内有意义，reset 或 backend 变化可能重新编号；
- 遮挡、快速运动、光照、图像缩放和人物外观会影响检测/追踪；
- HOG 仅 person detector，不等价于 YOLO；
- bbox/center 是图像像素，不是物理位移或不确定度。

## Benchmark 与 Provenance

[本传感器 benchmark](benchmarks/README.md) · [Phase 3C 结果](../../benchmarks/results/phase3c-yolo-adapter-2026-08-16.md) · [SOURCE.md](SOURCE.md) · [sensor.json](sensor.json) · [license review](../../docs/yolo-model-and-license-review.md)

## Distribution

- Maturity/evidence: `experimental / E2`; real Ultralytics inference is not part of current evidence.
- Implementation: `physics_sensors.tracking.YoloTrackerSensor` in Python package `0.5.0`.
- Proposed bundle: `tracker.yolo-0.5.0.zip`; offline replay requires `yolo-recorded`, while real inference separately requires `yolo-runtime` and an approved local `ModelArtifact`.
- No `.pt`, `.onnx`, `.engine` or third-party weight is distributed or automatically downloaded.
- Install/download: [installation](../../docs/installation.md) · [downloading sensors](../../docs/downloading-sensors.md).
- Minimal runnable example: [python-yolo-tracker](../../examples/python-yolo-tracker/README.md).
