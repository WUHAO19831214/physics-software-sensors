# Number OCR Benchmark

## 当前证据

- 来源 parser fixture：rawText→normalizedText→number；
- recorded-result replay：ROI、confidence、duration、warning/error 保留；
- 失败路径：parse failure 和 recognizer failure 均无 measurement；
- Node/TypeScript 构建与离线测试。

记录：[Phase 2 adapter verification](../../../benchmarks/results/phase2-adapter-verification-2026-08-16.md) · [fixture card](../../../benchmarks/datasets/ocr-number-recorded-result-fixture/dataset-card.md)

## 尚未完成

- 真实 recorded image frames 和 Tesseract.js backend；
- exact match rate、numeric parse success、absolute numeric error；
- 小数点/符号错误率、拒绝率和误接受率；
- 真实 p50/p95 latency、CPU/内存；
- 屏幕缩放、字体、背景、亮度、ROI 敏感性。

进入 validated 前必须提供脱敏数据集卡和真实识别报告；parser 测试不能替代 OCR 精度测试。
