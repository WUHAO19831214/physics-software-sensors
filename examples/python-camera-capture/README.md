# Python camera capture

这个最小程序证明 `CameraSource` 离开原实验应用后仍能输出统一 `RuntimeFrame` / FramePacket。

确定性证据（默认，不访问摄像头）：

```bash
python examples/python-camera-capture/run.py --publish-assets
```

人工真实设备 smoke test（显式指定才打开设备）：

```bash
python examples/python-camera-capture/run.py --device 0
```

默认回放只能证明契约、时间字段、丢帧和 backend seam，不能证明真实硬件兼容。真实设备结果保存在 `output/hardware-smoke.json`，需记录 OS、OpenCV backend 和实际分辨率/FPS。
