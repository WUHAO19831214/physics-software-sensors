# Template / Single-object Tracker 演示资产

全部由 `examples/python-template-tracker/run.py` 在 synthetic textured-object replay 上运行真实 OpenCV contrib CSRT adapter 生成。它们不是来源项目截图或真实实验精度证据。

生成环境写入 `events.json`；本次为 Python 3.12.13、OpenCV 4.14.0、macOS arm64。生成命令：

```bash
python examples/python-template-tracker/run.py --output sensors/tracker.template/assets
```

| Asset | Meaning | SHA-256 |
| --- | --- | --- |
| `overview.png` | initialization ROI → tracking → lost | `c7f8b5e340ea399b2f67a6a509a23a8d52085edf970f492cd130e97a77d2b252` |
| `initialization.png` | 首帧 ROI；不是 template image asset | `155bfcc7cd22bd699dbc23d169716bdb82964fa6dd7ae78f96f46abdcd6d4a4e` |
| `tracking.png` | 真实 CSRT update 的 bbox/center | `a40cdf718980034e9cedd7351c35d48ebb0bfea15988c2d818d39ea53a9f74de` |
| `lost.png` | blank replay frame 的显式 lost | `9bddb171727a89cd4d787728942caf80fcef41145d3ecbc9a93870b9d172ff57` |
| `events.json` | 环境与四个完整 SensorEvent；latency 重跑时允许变化 | generated runtime evidence |

许可证：本仓库 MIT；没有复制固定来源仓库资产。OpenCV 二进制不随本仓库资产提交。
