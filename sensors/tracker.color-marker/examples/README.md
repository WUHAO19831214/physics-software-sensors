# Color Marker Tracker 最小示例

当前可运行入口是 `physics_sensors.tracking.ColorMarkerSensor`。它只需要公共 core、NumPy 和 OpenCV，不依赖来源实验项目 UI。

```python
sensor = ColorMarkerSensor()
sensor.configure({"hsv_lower": [20, 100, 100], "hsv_upper": [40, 255, 255]})
await sensor.start(SensorContext.minimal("run-001"))
async for event in sensor.process(RuntimeFrame(metadata=packet, pixels=frame)):
    consume(event)
await sensor.stop()
```

调用方仍需构造有效 `FramePacket` metadata，并提供 BGR `uint8` NumPy 帧。后续 `examples/python-color-marker/` 将加入小型摄像头/文件示例；本轮不新建大型实验应用。
