# Camera Capture benchmark

## Phase 3A L1 protocol

- 固定 3 帧、640×360 BGR synthetic image sequence；
- requested 1280×720 @ 30 FPS；backend nominal 20 FPS；固定 monotonic interval 50 ms；
- 断言 measured 20 FPS、inter-frame jitter 0 ms、1 个显式 dropped frame、Schema 合法和 stop 幂等；
- 记录 artifact SHA-256、分辨率、wall/monotonic/source timestamp。

## 当前结果

3/3 帧交付；measured 20.0 FPS；帧间隔 50.0 ms；jitter 0.0 ms；dropped count 1（fixture 注入并完整保留）。这是 deterministic replay，不是性能上限。CPU、内存、真实 delivery latency、首帧延迟和硬件掉帧尚未形成可比较的 L2 结果，禁止填猜测值。

完整报告：[Phase 3A capture replay](../../../benchmarks/results/phase3a-capture-replay-2026-08-16.md)。
