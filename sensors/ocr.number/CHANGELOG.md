# Changelog — ocr.number

## 0.2.0 — 2026-08-16

- 状态从 contract-only/planned 进入 experimental/incubating；
- 增加 TypeScript NumberOCRSensor、来源兼容 parser 和 recorded-result replay recognizer；
- 保留 rawText、value、confidence、duration、warning/error；
- 明确失败事件不返回 mock 或上一次数值；
- 真实 Tesseract.js、像素预处理和浏览器 UI 尚未迁移。

## 0.1.0 — 2026-08-04

- 建立 manifest 与契约骨架，无本仓库实现。
