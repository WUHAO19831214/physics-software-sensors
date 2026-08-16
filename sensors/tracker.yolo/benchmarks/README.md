# YOLO Tracker Benchmark

当前证据分为两个互不混淆的层次。

## Deterministic adapter benchmark

固定结果：[Phase 3C report](../../../benchmarks/results/phase3c-yolo-adapter-2026-08-16.md) / [JSON](../../../benchmarks/results/phase3c-yolo-adapter-2026-08-16.json)。输入来自 [dataset card](../../../benchmarks/datasets/yolo-tracker-source-recorded-replay/dataset-card.md)。

它验证 event mapping latency、单/多目标 serialization、all/ID/name class filters、tracking/lost/reappear 状态和 source-output compatibility。它不执行神经网络，不能用于评价模型 FPS、检测 accuracy 或 ByteTrack quality。

## Real inference benchmark

Phase 3C：**not measured**。没有维护者批准的本地模型 artifact，开发环境没有 Ultralytics runtime，且项目禁止自动联网下载。model、SHA-256、device、input size、inference latency、FPS、memory、detection count 均明确为 `not measured`。

未来若执行，必须固定 runtime/model SHA/device/input、把 detector 与 tracking latency 分开，并使用正式标注集才可报告 precision/recall/mAP 或 HOTA/IDF1/ID switches。没有标注集时只能报告软件性能和 detection count，不能声称 accuracy。
