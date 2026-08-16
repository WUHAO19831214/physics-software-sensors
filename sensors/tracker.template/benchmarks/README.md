# Template / Single-object Tracker Benchmark

当前完成两层 replay：

- 固定来源类的七个 scripted golden 快照覆盖 fallback、move、lost、exception、reinitialize 和 unavailable；stable numeric/status fields 容差 1e-9 px；
- OpenCV 4.14.0 contrib CSRT synthetic sequence：3/3 moving frames tracking，blank frame lost，已知 target 最大 center error 1.0 px；
- 同机 200 次 same-frame update：median 7.722 ms、p95 9.577 ms；
- fallback 测试确认 CSRT unavailable + KCF init false 后选择 MIL，并输出 flag。

完整环境与限制见 [Phase 3B report](../../../benchmarks/results/phase3b-classical-trackers-2026-08-16.md)。仍待真实相机、遮挡/尺度/旋转分层、CPU/memory、跨 OpenCV/platform 矩阵；不声称真实实验精度。
