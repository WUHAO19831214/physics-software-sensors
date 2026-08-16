# Web Number OCR 示例

本轮真实浏览器 OCR **pending**。可运行的 recorded-result replay 位于 `packages/typescript/tests/number-ocr.test.ts`；它证明 adapter、parser 与失败语义，不证明 Tesseract 像素识别。

```bash
npm --prefix packages/typescript test
```

真实示例将在 Canvas ROI/preprocess 和 `TesseractJsRecognizer` 完成后加入，并保持页面足够小。
