# Camera Capture Changelog

## 0.3.0 — 2026-08-16

- 增加 backend-neutral Python `CameraSource`；
- 增加确定性 `ImageSequenceCameraBackend` 与可选 `OpenCVCameraBackend`；
- 输出 Schema `1.0.0` FramePacket，并分开记录 requested、nominal、measured FPS；
- 增加 replay/schema/drop/lifecycle tests、standalone example 和 synthetic assets；
- maturity 从 `planned/contract-only` 提升到 `incubating/adapter-present`；无真实设备验证。

## 0.1.0 — 2026-08-04

- 建立 contract-only 页面与 manifest。
