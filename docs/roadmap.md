# 路线图

## Phase 1 — 文档与骨架（完成）

- [x] 盘点五个优先公开仓库并锚定 commit；
- [x] 定义统一生命周期、事件信封、时间和坐标语义；
- [x] 建立机器可读 Schema、传感器清单与示例；
- [x] 建立基准方案、升级模板、本地契约测试和待启用 CI 模板；
- [x] 提供 Python/TypeScript 类型骨架；
- [x] 由维护者确认首个第二阶段试点；来源许可证仍需在 stable 前明确。

退出标准：仓库校验通过；所有首批传感器有清单；文档不声称新实现已完成。

## Phase 2A — Public Sensor Catalog（本轮）

- [x] 七个独立 Sensor Page 目录；
- [x] 统一 README/SOURCE/asset 模板；
- [x] 仓库级 sensor catalog 与 asset inventory；
- [x] 两个试点的完整公开页面；
- [ ] 从真实来源运行状态补充获准发布的 demo 图片。

## Phase 2B — Color Marker Adapter（本轮 experimental）

- [x] 建立 `physics_sensors.core` 和独立 `tracking.color_marker`；
- [x] 保留 source-native 输出并映射 SensorEvent；
- [x] 固定 golden fixture，并对固定来源 commit 进行同帧比较；
- [ ] 建立真实摄像头 recorded dataset、性能基准和 L2 验证；
- [ ] 选择一个来源项目做可回退下游试点。

## Phase 2C — Number OCR Adapter（experimental）

- [x] 建立 TypeScript parser、recognizer seam 和 recorded-result replay；
- [x] 保留 rawText/value/confidence/duration/warning/error，失败无 mock；
- [x] 加入明确标记的 synthetic pixel frames；
- [x] 抽取纯 RGBA ROI/preprocess 和真实 Tesseract.js backend；
- [x] 对固定 synthetic pixels 运行 exact numeric match、parse failure 和 engine failure；
- [ ] 加入脱敏真实设备 recorded image frames，并运行完整 accuracy/latency benchmark。

Phase 2 仍只选择两个实现试点：

1. Python `tracker.color-marker`：来源稳定版已有单元测试且依赖边界清楚；
2. TypeScript `ocr.number`：可直接服务实验桥/教师端，优先做录制回放，不先改 UI。

## Phase 2D — Pilot Completion & Demonstration（完成）

- [x] Color Marker standalone runner、实际 mask/event/annotated assets；
- [x] OCR RGBA pixel → ROI → preprocessing → Tesseract.js → SensorEvent；
- [x] OCR synthetic fixture runner、成功/parse failure/engine failure；
- [x] 两个 Sensor Page 直接展示有明确证据标签的 demo；
- [x] Python wheel 与 npm tgz clean-install smoke test；
- [x] repository/source/adapter/fixture 许可证边界说明；
- [ ] 真实摄像头和真实设备屏幕 recorded datasets，留待后续 L2。

## Phase 3A — Capture Layer（本轮 experimental）

- [x] Python backend-neutral `CameraSource`、deterministic image-sequence backend 与可选 OpenCV backend；
- [x] TypeScript `ScreenCaptureSource`、用户授权 browser driver 与 recorded backend；
- [x] camera/screen 共用 FramePacket Schema `1.0.0`，不重设计 Phase 1 契约；
- [x] requested/nominal/measured rate、wall/monotonic/source time 和 dropped frames 分开记录；
- [x] Camera、Screen、Screen→真实 OCR 三个独立 example；
- [x] replay、browser permission/error、composition、contract 与 clean-install tests；
- [ ] 真实 camera 与 browser 人工 smoke 报告、设备/OS/browser 矩阵；
- [ ] L2 CPU、内存、capture latency、长时间稳定性与断流恢复基准。

退出标准（本轮达到 experimental）：两个 manifest 为 `incubating/adapter-present`，L0/L1 自动证据通过，来源仓库不变；真实设备证据仍是后续门禁，不把 replay 当成 hardware validation。

## Phase 3B — Classical Trackers（本轮 experimental）

- [x] `tracker.spot-centroid`：来源兼容 red weighted centroid、confidence null、六帧来源 golden；
- [x] `tracker.template`：ROI-initialized CSRT→KCF→MIL、实际 backend/fallback、lost/reinitialize；
- [x] 两项均直接消费 CameraSource RuntimeFrame，并输出 Schema-valid SensorEvent；
- [x] standalone synthetic assets、来源执行型 comparison、clean-install 与微基准；
- [ ] 真实摄像头/实验目标 L2 数据、CPU/memory、长期运行和跨平台矩阵；
- [ ] 来源许可确认和可回退下游试点。

退出标准（本轮达到 experimental）：两个 manifest 为 `incubating/adapter-present/replay-benchmarked`；不把 pixel 说成物理位移，不伪造 confidence，不修改来源仓库或 FramePacket `1.0.0`。

## Phase 3C — YOLO Tracker（本轮 experimental）

- [x] `tracker.yolo` 独立 Python adapter 和 multi-target SensorEvent；
- [x] `ModelArtifact` 与 library/runtime/weight 解耦，本地 SHA 验证且不自动下载；
- [x] `RecordedDetectorBackend`、可选 `YoloDetectorBackend` 与 person-only OpenCV HOG fallback；
- [x] detection/tracking/confidence 语义、all/ID/name class filter 和 actual backend 显式化；
- [x] 来源执行型 golden、ID lifecycle/fallback tests、CameraSource composition、offline example/assets 与 adapter benchmark；
- [x] runtime/weight/ByteTrack/HOG 专项许可证审查；不提交模型权重；
- [ ] 经维护者批准的本地 artifact 真实 inference smoke、标注数据集和模型/追踪性能；
- [ ] 来源许可确认、真实摄像头 L2 和可回退下游试点。

退出标准（本轮达到 experimental）：manifest 为 `incubating/adapter-present/replay-benchmarked`，catalog 达到 7/7 adapters；真实 inference 未执行时必须明确原因和全部 `not measured` 字段，不把 detector score 当物理 uncertainty。

## Phase 3D — Cross-sensor benchmark（只规划）

- 跨语言事件一致性测试；
- real/replay/synthetic dataset matrix；
- 真实设备兼容矩阵与 L2 基准。

## Phase 4 — 下游灰度接入

先选一个低风险下游仓库，以版本固定和 feature flag 接入。验证无回归后，再逐个接入其他项目；不同时修改五个来源仓库。

## Phase 5 — 稳定发布

- 契约 `1.0.0`；
- 可安装 Python/TypeScript 包；
- 至少一个 `stable` 传感器；
- 两个下游项目使用统一事件；
- 发布兼容矩阵、基准结果与升级/回退记录。

## 暂不承诺

硬件级同步、计量认证、统一训练平台、云端视频托管、自动下载受限模型权重、替代原实验应用，均不在当前路线图承诺范围内。
