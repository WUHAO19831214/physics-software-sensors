# Screen Capture Changelog

## 0.3.0 — 2026-08-16

- 增加 TypeScript `ScreenCaptureSource`、真实 browser driver 与 deterministic recorded backend；
- `start()` 成为显式权限边界，拒绝与 stream ended 使用稳定错误码；
- 输出 runtime RGBA FramePacket，并提供 Schema JSON serializer；
- 增加 replay/browser/composition/real-Tesseract tests、最小网页与 synthetic assets；
- maturity 从 `planned/contract-only` 提升到 `incubating/adapter-present`；无浏览器矩阵验证。

## 0.1.0 — 2026-08-04

- 建立 contract-only 页面与 manifest。
