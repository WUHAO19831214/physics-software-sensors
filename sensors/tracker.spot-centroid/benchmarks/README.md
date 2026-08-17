# Spot Centroid Benchmark

当前完成 source replay 和 E5 downstream reuse：

- 六个固定 PNG 同时输入来源 JavaScript harness 和 Python extraction；
- detection/lost 6/6 一致；centroid 最大误差 0.0 px，容差 1e-9 px；
- 160×120 mixed fixture 200 次处理：median 0.793 ms、p95 0.875 ms（本机微基准）；
- CameraSource composition 和 SensorEvent Schema 通过。
- 光斑振动下游项目通过 SHA-256 固定的公开 `v0.6.0` wheel 运行 `legacy/library/compare`；七个同帧 case 全部通过，最大 delta `7.105427357601002e-15`（容差 `1e-9 px`）；
- 下游三帧序列的 `y_max-y_min` 两条路径均为 `28 px / 0.56 cm`，且 rollback 已测试。

完整环境与限制见 [Phase 3B report](../../../benchmarks/results/phase3b-classical-trackers-2026-08-16.md)和 [downstream comparison](../../../integrations/spot-vibration/comparison-summary.md)。下游 fixture 仍是 synthetic offline replay；真实摄像头 exposure、ROI、missing rate、CPU/memory、长期稳定性和 E4 光学/设备验证仍待完成，当前结果不代表物理计量精度。
