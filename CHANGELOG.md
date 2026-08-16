# Changelog

本项目遵循 SemVer；传感器实现、契约和模型资产分别记录版本。

## 0.2.0 — 2026-08-16

- 建立七个统一 Sensor Page 目录、仓库级 catalog、SOURCE/asset 模板和来源资产盘点；
- 完整建设 `tracker.color-marker` 与 `ocr.number` 公开页面；
- 增加实验性 Python `physics_sensors` core、ColorMarkerTracker/Sensor 和来源 golden-master 对照；
- 增加实验性 TypeScript NumberOCRSensor、来源兼容 parser 和 recorded-result replay；
- 两个试点进入 `incubating/adapter-present`，其余五项仍为 contract-only；
- 未修改来源仓库，未复制授权不明图片，未声称真实设备或计量验证。

## 0.1.0 — 2026-08-04

- 创建“物理实验软件传感器库”第一阶段文档与骨架；
- 盘点五个优先公开仓库并以完整 commit 锚定来源；
- 定义统一生命周期、SensorEvent、FramePacket、传感器清单和基准结果 Schema；
- 建立摄像头、屏幕、OCR、颜色、YOLO、模板与光斑重心七类清单；
- 增加 Python/TypeScript 类型骨架、基准方案、升级模板、契约校验和待启用 CI 模板；
- 本版本不包含从现有项目迁移的算法实现。
