# 数据集卡：ocr-number-recorded-result-fixture@0.1.0

## 用途与范围

验证 `ocr.number` 的来源 parser 兼容、recognizer result 保留、SensorEvent 映射和失败语义。它是**合成 recorded-result fixture**，不是 recorded image dataset，也不能用于 OCR 准确率结论。

## 内容

- `packages/typescript/tests/fixtures/ocr-number/recorded-results.json`；
- 4 个 parser 行为样例；
- 识别成功、带 warning、无法解析和 worker failure 四类结果；
- 不包含像素、屏幕截图、人物或设备软件内容。

## 来源真值

parser 语义锚定两个来源 commit 中 SHA-256 相同的 `src/utils/extractNumber.ts`；result 字段锚定同版本 `TesseractRecognizer.ts`。固定 commit 见 `sensors/ocr.number/SOURCE.md`。

## 文件完整性

`packages/typescript/tests/fixtures/ocr-number/recorded-results.json`
SHA-256: `ab0805d1a17c1468da328bc12e6aa858cf9da95e39ea1d9b5877d94076f92260`

## 许可与隐私

本仓库新建的合成 JSON，无个人信息；没有复制来源图片/UI。来源仓库许可证仍为 `NOASSERTION`。

## 限制

recorded result 绕过真实 ROI 像素、预处理和 Tesseract 推理。它只能验证 adapter 行为，不能计算 exact match rate、absolute numeric error 或真实 latency。
