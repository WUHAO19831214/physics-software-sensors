# YOLO Tracker 示例入口

可运行的 Python 示例位于 [`examples/python-yolo-tracker`](../../../examples/python-yolo-tracker/README.md)。默认 `--backend recorded` 完全离线，证明该传感器离开来源实验应用后仍可完成：

```text
ImageSequenceCameraBackend → CameraSource → FramePacket
  → RecordedDetectorBackend → YoloTrackerSensor → SensorEvent
```

真实模式只接受 `--model /absolute/path`、显式 `--model-license-state` 和至少一个 `--input`，不自动打开 camera 或联网下载。若 runtime/model 没有真正进入 Ultralytics backend 而是回退，脚本拒绝生成“real inference”资产。
