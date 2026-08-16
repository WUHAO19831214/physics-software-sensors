# Changelog — tracker.template

## 0.4.0 — 2026-08-16

- 新增 Python ROI-initialized OpenCV single-object tracker 与 SensorEvent adapter；
- 保留 CSRT→KCF→MIL fallback、lost/reinitialize 和 source-native output projection；
- 增加专用 `initialize_target`，不修改统一 ProcessorSensor contract；
- 新增来源执行型 golden、真实 contrib synthetic replay、Camera composition 和 demo assets；
- 明确 initialization ROI 不等于 template asset，confidence 保持 null。

## 0.1.0 — 2026-08-04

- 契约和来源清单；无本仓库实现。
