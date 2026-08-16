# 传感器升级记录：ocr.number 0.1.0 → 0.2.0

## 基本信息

- 负责人：WUHAO19831214；
- 日期：2026-08-16；
- 变更类型：parser/recognizer seam/recorded replay 首次适配；
- 目标成熟度：incubating / experimental；
- 契约版本：SensorEvent `1.0.0`（未改变）。

## 来源锚点

- `WUHAO19831214/physics-experiment-bridge-mvp@8bba87df6475cae1e595fc925551db8bea83fb68`；
- `WUHAO19831214/ampere-force-visualizer-teacher-yanan@cb073e89d6d87129287030f1df08bd540504eb39`；
- 文件/函数：`TesseractRecognizer.ts::TesseractRecognizer.recognize`、`extractNumber.ts::normalizeOcrText/extractNumberFromText`、`imagePreprocess.ts`、`ocrPreprocess.ts`、`numberPostprocess.ts`、`ScreenCapturePanel.tsx`；
- 两个来源中的五个核心文件 SHA-256 相同，清单见 sensor `SOURCE.md`；
- 来源许可证：均为 `NOASSERTION`，审核 pending。

## 行为变化

- 来源 parser 行为进入独立 Node 可测试 utility；
- 新增 injected `NumberRecognizer` 和 `RecordedNumberRecognizer`；
- 新增 `NumberOCRSensor`，输出 rawText、normalizedText、parsed measurement、confidence、duration、warning/error；
- parse/recognizer failure 使用明确 error SensorEvent，measurements 为空；
- 真实 Tesseract.js、Canvas ROI/preprocess、React UI 和物理过滤本轮未迁移。

## 验证证据

- 7 个 TypeScript/Node 测试：parser、成功、warning、parse failure、recognizer failure、missing replay、invalid ROI；
- fixture：`ocr-number-recorded-result-fixture@0.1.0`；
- 失败测试明确证明不会产生 mock/stale value；
- 报告：[`benchmarks/results/phase2-adapter-verification-2026-08-16.md`](../../benchmarks/results/phase2-adapter-verification-2026-08-16.md)。

## 兼容与迁移

- 没有修改来源 React/浏览器应用；
- 新 package 暂为单一 `@physics-software-sensors/core`；
- recorded replay API 是实验性边界，真实 Tesseract backend 可能增加可选依赖，但不能改变失败语义。

## 回退

- 回退到 manifest `0.1.0` 即只保留契约；
- 来源项目完全未修改；
- 没有下游数据迁移。

## 未完成门禁

- [ ] source 许可证明确
- [ ] 脱敏 recorded image frames
- [ ] Canvas/preprocess/Tesseract.js backend
- [ ] exact match、numeric error、failure rate 和真实 latency
- [ ] 浏览器与下游试点
