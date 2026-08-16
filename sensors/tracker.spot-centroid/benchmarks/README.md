# Spot Centroid Benchmark

当前完成 synthetic/replay L1：

- 六个固定 PNG 同时输入来源 JavaScript harness 和 Python extraction；
- detection/lost 6/6 一致；centroid 最大误差 0.0 px，容差 1e-9 px；
- 160×120 mixed fixture 200 次处理：median 0.793 ms、p95 0.875 ms（本机微基准）；
- CameraSource composition 和 SensorEvent Schema 通过。

完整环境与限制见 [Phase 3B report](../../../benchmarks/results/phase3b-classical-trackers-2026-08-16.md)。仍待真实摄像头数据上的 exposure、ROI、missing rate、CPU/memory 和长期稳定性；当前结果不代表物理计量精度。
