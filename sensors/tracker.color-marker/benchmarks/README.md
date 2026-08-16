# Color Marker Tracker Benchmark

## 当前证据

- L0：SensorEvent Schema、生命周期、invalid/lost 状态；
- L1：确定性合成 BGR 帧；固定来源 golden 输出；可选动态加载来源实现进行同帧比较；
- 比较容差：source-native 浮点字段绝对误差 `1e-6`。
- standalone demo：实际 adapter 产生 `ok → lost → ok`、HSV mask 和 annotated output。

记录：[Phase 2 adapter verification](../../../benchmarks/results/phase2-adapter-verification-2026-08-16.md) · [Phase 2D result](../../../benchmarks/results/phase2d-demonstration-2026-08-16.md) · [dataset card](../../../benchmarks/datasets/color-marker-synthetic-golden/dataset-card.md)

## 尚未完成

- 真实标记静态中心 bias/RMSE；
- 不同光照、曝光、背景和 ROI 的 detection/lost rate；
- p50/p95 延迟、FPS、CPU 和峰值内存；
- 像素到物理长度的独立标定误差；
- 公开数据集卡和 L2 受控实验。

进入 validated 前必须按仓库级 [benchmark 方案](../../../docs/benchmarking.md) 预注册阈值并报告失败样本。
