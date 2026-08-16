# Python Template / Single-object Tracker 独立示例

此处的“template”保留既有 Sensor ID；实际算法是首帧 ROI 初始化的 OpenCV 单目标 tracker，不是静态模板匹配。示例使用真实 `CSRT → KCF → MIL` backend factory：

```text
ImageSequenceCameraBackend → CameraSource → FramePacket
initial frame + ROI → TemplateTrackerSensor.initialize_target
later FramePacket → TemplateTrackerSensor.process → SensorEvent
```

运行：

```bash
python -m pip install -e 'packages/python[classical-trackers]'
python examples/python-template-tracker/run.py
python examples/python-template-tracker/run.py --output sensors/tracker.template/assets
```

素材是合成回放，事件由真实 OpenCV tracker 产生。它证明独立调用、backend 记录和 lost 状态，不代表真实实验追踪精度。
