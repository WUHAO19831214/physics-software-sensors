# Python YOLO Tracker 独立示例

默认模式完全离线：读取固定来源生成的 detector fixture，经真实 `CameraSource → FramePacket → YoloTrackerSensor → SensorEvent` 生成多目标、ID、lost/reappear 和 fallback 资产。

```bash
python -m pip install -e 'packages/python[classical-trackers]'
python examples/python-yolo-tracker/run.py --backend recorded
python examples/python-yolo-tracker/run.py --backend recorded --output sensors/tracker.yolo/assets
```

Recorded 输出是 **Recorded detector replay / Synthetic fixture**，不是实时 YOLO 推理或 accuracy 证据。

真实 backend 只接受显式本地模型和输入，不自动联网：

```bash
python -m pip install -e 'packages/python[yolo-runtime]'
python examples/python-yolo-tracker/run.py \
  --backend yolo \
  --model /absolute/path/to/yolov8n.pt \
  --model-family YOLOv8 \
  --model-license-state agpl-3.0-reviewed \
  --input /absolute/path/to/input.png
```

脚本会计算模型 SHA-256 并写入事件。使用者必须自行确认 runtime、权重和使用方式的许可证；本仓库不提供、下载或重新分发权重。
