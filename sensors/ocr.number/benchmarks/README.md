# Number OCR Benchmark

## 当前证据

- 来源 parser fixture：rawText→normalizedText→number；
- recorded-result replay：ROI、confidence、duration、warning/error 保留；
- 失败路径：parse failure 和 recognizer failure 均无 measurement；
- pure RGBA crop/preprocess 单元测试；
- 真实 Tesseract.js synthetic pixel integration：三个数字 exact numeric match，两个 parse failure 和一个 controlled engine failure；
- Node/TypeScript 构建与独立 example。

记录：[Phase 2 adapter verification](../../../benchmarks/results/phase2-adapter-verification-2026-08-16.md) · [Phase 2D result](../../../benchmarks/results/phase2d-demonstration-2026-08-16.md) · [recorded-result card](../../../benchmarks/datasets/ocr-number-recorded-result-fixture/dataset-card.md) · [synthetic-pixel card](../../../benchmarks/datasets/ocr-number-synthetic-pixels/dataset-card.md)

## 尚未完成

- 真实设备 recorded image frames；
- 真实设备 exact match rate、numeric parse success、absolute numeric error；
- 小数点/符号错误率、拒绝率和误接受率；
- 真实 p50/p95 latency、CPU/内存；
- 屏幕缩放、字体、背景、亮度、ROI 敏感性。

进入 validated 前必须提供脱敏数据集卡和真实识别报告；parser 测试不能替代 OCR 精度测试。
