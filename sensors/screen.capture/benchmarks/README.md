# Screen Capture benchmark

## Phase 3A L1 protocol

- 固定 2 个 2×1 RGBA recorded frames；
- requested sampling interval 100 ms；fixed monotonic interval 250 ms；
- 断言 measured interval 250 ms / 4 Hz、1 个显式 dropped frame、artifact hash 和 stop；
- 另用 800×300 synthetic shared-window frame 完成 Schema serialization 和真实 Tesseract composition。

## 当前结果

2/2 replay frames 交付；measured interval 250 ms；measured rate 4 Hz；dropped count 1（fixture 注入并保留）。组合样本得到 OCR rawText `-2.33`、parsed value `-2.33`。单帧 standalone 输出的 measured interval 合理为 `null`。CPU、内存、browser capture latency、真实 refresh/scheduling 与平台行为未测，不以 Node replay 代替。

完整报告：[Phase 3A capture replay](../../../benchmarks/results/phase3a-capture-replay-2026-08-16.md)。
