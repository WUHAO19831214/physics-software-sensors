# 基准目录

```text
benchmarks/
├── datasets/   # 只存数据集卡和允许公开的小样本；大型数据用 URI + SHA-256
├── protocols/  # 预注册的传感器专项协议
└── results/    # 机器摘要 JSON + 人类可读报告
```

当前不提交真实摄像头/设备屏幕数据，也没有真实实验精度结果。Phase 2D 增加 synthetic pixel OCR 与 standalone visualization；它们验证软件路径和固定 fixture，不可外推为真实设备准确率。`contracts/examples/benchmark-result.json` 仍只是格式示例。

新增数据集前复制 `templates/DATASET_CARD.md`；新增结果前复制 `templates/BENCHMARK_REPORT.md`，并确保机器摘要满足 `benchmark-result.schema.json`。

当前记录：[`Phase 2 adapter verification`](results/phase2-adapter-verification-2026-08-16.md) · [`Phase 2D demonstration`](results/phase2d-demonstration-2026-08-16.md) · [`Phase 3A capture`](results/phase3a-capture-replay-2026-08-16.md) · [`Phase 3B classical trackers`](results/phase3b-classical-trackers-2026-08-16.md) · [`Phase 3C YOLO adapter`](results/phase3c-yolo-adapter-2026-08-16.md)。
