# 基准目录

```text
benchmarks/
├── datasets/   # 只存数据集卡和允许公开的小样本；大型数据用 URI + SHA-256
├── protocols/  # 预注册的传感器专项协议
└── results/    # 机器摘要 JSON + 人类可读报告
```

当前不提交真实摄像头/屏幕数据，也没有任何算法精度结果。`contracts/examples/benchmark-result.json` 只是格式示例，不是性能证据。

新增数据集前复制 `templates/DATASET_CARD.md`；新增结果前复制 `templates/BENCHMARK_REPORT.md`，并确保机器摘要满足 `benchmark-result.schema.json`。
