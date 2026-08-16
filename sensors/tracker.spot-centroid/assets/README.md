# Spot Centroid 演示资产

全部由 `examples/spot-centroid/run.py` 使用本仓库 synthetic PNG 运行真实 `CameraSource → SpotCentroidSensor` 生成；不是来源项目图片、真实实验数据或物理标定结果。

生成命令：

```bash
python examples/spot-centroid/run.py --output sensors/tracker.spot-centroid/assets
```

| Asset | Meaning | SHA-256 |
| --- | --- | --- |
| `overview.png` | 一个 bright fixture 的 centroid overlay | `0e287e84aef4a699e213b64657218e28080c4a84913546699ea2ce086f4016bc` |
| `processing.png` | original / accepted-pixel mask / adapter output | `7925a1806d9d81c38ee479801cea28e60c6a7910d0e6ab22ba415dda41b8f806` |
| `movement.png` | initial / horizontal / vertical synthetic movement | `7262723c1ebea87581e621338a6dd2412edd9bb2c2b2d31c4306568e2b07f410` |
| `events.json` | 六个完整 SensorEvent；包含运行时 latency，重跑时允许变化 | generated runtime evidence |

输入 fixture 由 `examples/spot-centroid/generate_fixtures.py` 生成，清单在 `examples/spot-centroid/sample/manifest.json`。许可证：本仓库 MIT；没有复制固定来源仓库资产。
