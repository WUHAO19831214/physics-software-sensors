# 来源与抽取记录：tracker.yolo

## 固定来源

| Repository | Commit | Path | Symbol / responsibility | Actual use |
| --- | --- | --- | --- | --- |
| `WUHAO19831214/audio-visual-soundfield-tracker-stable` | `85740d686c67452a057540edb564d713e01ccc51` | `src/detector.py` | `Detection`；`Detector.__init__/detect/track/_parse_yolo_results/_detect_hog` | 本地 YOLO detection、`persist=True` ByteTrack、缺失 ID 标记、HOG fallback |
| 同上 | 同上 | `src/camera_processor.py` | `CentroidTracker`；`CameraProcessor._update_tracks` | HOG 或 native ID 不完整时的最近重心 association；`max_missed=12`、`max_distance_ratio=0.18` |
| 同上 | 同上 | `requirements.txt` | `ultralytics>=8.2,<9`、`lap>=0.5.12,<1`、OpenCV | 运行时依赖范围 |
| 同上 | 同上 | `config.yaml` | `person_only`、confidence、tracker | 应用默认 `person_only=true`、threshold `0.25`、`bytetrack.yaml` |
| 同上 | 同上 | `scripts/setup_yolo.sh`、`models/README.md`、`.gitignore` | 显式模型准备、路径、忽略权重 | 确认应用可显式下载，但正常 adapter/test 不应下载或提交权重 |
| 同上 | 同上 | `tests/test_detector.py`、`tests/test_tracking.py` | weight missing/load failure、selector 等已有测试 | 来源基线；未覆盖多目标和完整 ByteTrack lifecycle，因此本仓库补充离线 replay |

固定来源 checkout 在抽取前后均为该完整 SHA 且 `git status --short` 空。Phase 3C 未修改来源仓库。

## 来源行为基线

- 初始化时依次查找 `models/yolov8n.pt` 与仓库根 `yolov8n.pt`；不存在、加载失败或推理失败时使用 OpenCV HOG；
- detection 调用 `model.predict(source=frame, classes=[0] when person_only, conf=threshold, verbose=False)`；
- tracking 调用 `model.track(..., persist=True, tracker="bytetrack.yaml")`；
- 解析每个 box 的 `xyxy/conf/cls/id`；native ID 缺失时使用当前帧 index+1 并发 warning；
- HOG 将最长宽缩至 720、使用 `detectMultiScale`、threshold 及 IoU 0.45 suppression，只输出 person；
- `CameraProcessor` 在 native IDs 不完整或 HOG 模式使用最近重心 tracker；stop/reset 后 ID 从 1 重新开始。

## 本仓库实现映射

| New file / symbol | Extraction method | Algorithm change |
| --- | --- | --- |
| `core/model_artifact.py::ModelArtifact` | 新增模型/runtime/provenance 边界 | 来源只按路径找权重；新实现强制显式 URI、SHA、runtime 和 license state，并拒绝远程 URI。这是安全/可追溯增强，不修改 detection 数值 |
| `tracking/yolo.py::YoloDetection/DetectorFrameResult` | 来源 `Detection` 的结构化投影 | `xyxy` 改为 JSON 友好的 `x/y/width/height`，同时输出 center；保留 detector confidence、class、track ID 和 native-ID availability |
| `tracking/yolo.py::RecordedDetectorBackend` | 来源执行输出的 deterministic replay seam | 不运行模型；只用于 golden/test/example，页面与事件明确标注 recorded |
| `tracking/yolo.py::YoloDetectorBackend` | 抽离来源 YOLO/HOG 控制流，注入 backend/artifact | 保留 predict/track 参数和 HOG fallback；不再扫描项目目录或自动准备模型；ByteTrack exception 先保留 YOLO detection，再用 centroid association |
| `tracking/yolo.py::OpenCVHogDetectorBackend` | 来源 HOG 最小依赖边界 | 保留 person-only、resize、threshold、IoU suppression；事件显式区分 actual backend |
| `tracking/yolo.py::CentroidAssociator` | 来源 `CentroidTracker` | 保留 nearest-centroid、missed lifecycle、distance ratio 与 reset semantics；增加 `tracking_id_available=false` |
| `tracking/yolo.py::YoloTrackerSensor` | FramePacket → SensorEvent adapter | 新增 lifecycle、multi-target payload、class filter、backend attempts、model artifact 和质量 flags；没有修改全局 SensorEvent Schema |

来源应用的 `person_only` 语义仍可通过 class ID/name filter 表达；独立库增加 all/ID/name 三种模式以支持复用。detector score 保存在 detection 内，顶层 confidence 不从它推导。

## 来源执行型 golden

`tools/generate_yolo_source_golden.py` 要求来源 checkout 精确处于固定 SHA，然后直接 import `src/detector.py` 和 `src/camera_processor.py`。它向真实来源类注入 scripted model result，执行 zero/single/move/two/lost/reappear/missing-ID detection，以及 CentroidTracker single/move/double/lost/reappear/reset，并记录 HOG fallback metadata。

生成结果为 `tests/fixtures/yolo_tracker/source-golden.json`，记录来源 commit、Python、OpenCV 和平台。测试比较来源输出的 bbox/class/confidence/ID、调用参数与 centroid lifecycle；fake `.pt` 只存在于临时目录，用于验证 path/SHA/runtime injection，绝不提交或执行真实模型。

## 验证边界

- `RecordedDetectorBackend` 覆盖 zero/single/multiple/filter/ID/lost/reappear/fallback；
- injected fake YOLO 验证 `persist=True`、`bytetrack.yaml`、classes、threshold 和 failure path；
- 真实 OpenCV HOG 在 blank frame 完成 offline smoke；
- `ImageSequenceCameraBackend → CameraSource → YoloTrackerSensor` 验证独立 composition；
- 真实 Ultralytics inference未执行，原因和 `not measured` 字段见 benchmark/license review。

## 演示资产

`examples/python-yolo-tracker/run.py --backend recorded` 读取来源 golden，生成 synthetic 背景和绘制结果：`overview.png`、`multi-target.png`、`tracking.png`、`fallback.png`、`events.json`。这些是 recorded replay，不是来源项目截图或真实 inference。

## 许可证边界

来源固定 commit 没有 `LICENSE*`，GitHub metadata 为 `NOASSERTION`，所以来源代码许可仍为 pending。抽取采用行为重实现和来源输出测试，没有复制模型、来源图片或整个模块。Ultralytics runtime、YOLO weight、ByteTrack 集成和 OpenCV fallback 分开记录于 [许可证审查](../../docs/yolo-model-and-license-review.md)。
