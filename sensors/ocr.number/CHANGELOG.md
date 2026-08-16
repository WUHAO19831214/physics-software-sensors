# Changelog — ocr.number

## 0.2.0 — 2026-08-16

- 状态从 contract-only/planned 进入 experimental/incubating；
- 增加 TypeScript NumberOCRSensor、来源兼容 parser 和 recorded-result replay recognizer；
- 保留 rawText、value、confidence、duration、warning/error；
- 明确失败事件不返回 mock 或上一次数值；
- 增加纯 RGBA ROI crop、来源兼容预处理和真实 `TesseractJsRecognizer`；
- 增加 synthetic pixel integration、standalone runner 和实际生成的 demo assets；
- React/屏幕授权 UI 与真实设备验证仍未迁移。

## 0.1.0 — 2026-08-04

- 建立 manifest 与契约骨架，无本仓库实现。
