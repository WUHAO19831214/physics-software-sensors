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

## Phase 2C — Number OCR Adapter（本轮开始）

- [x] 建立 TypeScript parser、recognizer seam 和 recorded-result replay；
- [x] 保留 rawText/value/confidence/duration/warning/error，失败无 mock；
- [ ] 加入脱敏 recorded image frames；
- [ ] 抽取 Canvas ROI/preprocess 和真实 Tesseract.js backend；
- [ ] 运行 exact match、numeric error、failure rate 和 latency benchmark。

Phase 2 仍只选择两个实现试点：

1. Python `tracker.color-marker`：来源稳定版已有单元测试且依赖边界清楚；
2. TypeScript `ocr.number`：可直接服务实验桥/教师端，优先做录制回放，不先改 UI。

## Phase 3 — 采集与其余分析器

- 按 `camera → screen → spot centroid → template → YOLO` 顺序适配；
- camera/screen 产生 FramePacket；其余产生 SensorEvent；
- 跨语言事件一致性测试；
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
