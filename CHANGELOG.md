# Changelog

本项目遵循 SemVer；传感器实现、契约和模型资产分别记录版本。

## 0.5.0 — 2026-08-16

- Phase 3C 新增 Python `YoloTrackerSensor`、`ModelArtifact`、recorded/Yolo/HOG backends 和 multi-target SensorEvent；
- 保留来源 predict/ByteTrack/HOG/centroid 边界，并显式记录 requested/actual/attempted backend、native ID 和 fallback；
- 增加来源执行型 golden、zero/single/multiple/lost/reappear/class-filter tests、CameraSource composition 和 deterministic adapter benchmark；
- 新增 offline standalone example 与明确标注的 recorded replay assets；
- 完成 runtime/weight/ByteTrack/HOG 许可证审查，不提交权重、不自动下载，真实 inference 明确为未执行；
- catalog 达到 7/7 experimental adapters；FramePacket `1.0.0` 与 SensorEvent 主 Schema 保持不变。

## 0.4.0 — 2026-08-16

- Phase 3B 新增 Python `SpotCentroidSensor` 与 `TemplateTrackerSensor`，直接消费 Phase 3A RuntimeFrame；
- 光斑重心保持固定来源 red threshold/brightness weighting，明确只输出 image centroid pixel；
- 单目标 tracker 保留 CSRT→KCF→MIL fallback，并区分 initialization ROI 与 template asset；
- 增加两个来源执行型 golden、CameraSource composition、synthetic standalone assets 和 microbenchmark；
- catalog 达到 6/7 experimental，YOLO 仍为 contract-only；FramePacket Schema 保持 `1.0.0`。

## 0.3.0 — 2026-08-16

- Phase 3A 建立统一 capture source 层，FramePacket Schema 保持 `1.0.0` 不变；
- Python 增加 backend-neutral `CameraSource`、image-sequence replay 与可选 OpenCV backend；
- TypeScript 增加 user-authorized browser `ScreenCaptureSource`、recorded replay 与 serializer；
- 增加 Camera、Screen 和 Screen→真实 Tesseract OCR 三个独立 example；
- requested/nominal/measured rate、权限拒绝、stream ended 与 dropped frame 显式化；
- 两个 manifest 提升为 `incubating/adapter-present/replay-benchmarked`，不声称硬件/浏览器验证。

## 0.2.0 — 2026-08-16

- 建立七个统一 Sensor Page 目录、仓库级 catalog、SOURCE/asset 模板和来源资产盘点；
- 完整建设 `tracker.color-marker` 与 `ocr.number` 公开页面；
- 增加实验性 Python `physics_sensors` core、ColorMarkerTracker/Sensor 和来源 golden-master 对照；
- 增加实验性 TypeScript NumberOCRSensor、来源兼容 parser 和 recorded-result replay；
- 完成 Phase 2D：Color Marker standalone visualization 与实际生成的 synthetic demo assets；
- 增加 RGBA ROI/preprocess、真实 Tesseract.js backend、synthetic pixel integration 与 OCR demo assets；
- 增加 package clean-install 门禁和 repository/source/adapter/fixture 许可证边界文档；
- 两个试点进入 `incubating/adapter-present`，其余五项仍为 contract-only；
- 未修改来源仓库，未复制授权不明图片，未声称真实设备或计量验证。

## 0.1.0 — 2026-08-04

- 创建“物理实验软件传感器库”第一阶段文档与骨架；
- 盘点五个优先公开仓库并以完整 commit 锚定来源；
- 定义统一生命周期、SensorEvent、FramePacket、传感器清单和基准结果 Schema；
- 建立摄像头、屏幕、OCR、颜色、YOLO、模板与光斑重心七类清单；
- 增加 Python/TypeScript 类型骨架、基准方案、升级模板、契约校验和待启用 CI 模板；
- 本版本不包含从现有项目迁移的算法实现。
