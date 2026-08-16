# YOLO Tracker 演示资产

全部资产由本仓库 `examples/python-yolo-tracker/run.py --backend recorded` 在 2026-08-16 生成。输入是 synthetic BGR frame；detection/track/fallback 记录来自固定来源执行型 fixture `tests/fixtures/yolo_tracker/source-golden.json`。图片显式标注 **Recorded detector replay**，不是来源项目截图、真实人物图像、真实 Ultralytics inference 或 accuracy 证据。

| Asset | Purpose | SHA-256 |
| --- | --- | --- |
| `overview.png` | zero、single、multiple target 总览 | `5a1fa8a44545041c0f55ea6f11e6693bc60c233b3d3a052ea53f44996567639b` |
| `multi-target.png` | 两个 detection 的数组输出 | `668c5487fa08abd40c088fc92cea11a736916dab3437d4b0076cd0eb5e639a7e` |
| `tracking.png` | track 7 的移动、lost、reappear recorded lifecycle | `cd0df4f1da735e979202f3787302d34ff8f0e2b3a3a4b46461f103cd5d5988d3` |
| `fallback.png` | requested YOLO / actual HOG metadata | `338f3ad62b672d3fcdb97c19f7508fde1fdc9adf0183505e141f2ba8ae4d47f2` |
| `events.json` | 7 个完整 CameraSource → YoloTrackerSensor 事件 | `a97f5c393512f2ffb53779368a9a1bfb5854fbeb33a1c25dfb8ea66caf7d3ec7` |

Fixture SHA-256：`641e0311c66f5c4508e6bc5990f071ec36627236e63efad18858e1a1bdbf0abd`。其来源、生成脚本与固定 commit 见 [SOURCE.md](../SOURCE.md)。

如以后运行真实 inference，必须使用经审查的显式本地 artifact，并把输出命名/标注为 **Real YOLO inference smoke test**，同时记录 runtime、model SHA、device、input size 和许可状态；不得覆盖这些 recorded 证据而混淆类型。
