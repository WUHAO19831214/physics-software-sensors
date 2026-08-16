# Spot Centroid 独立示例

该示例读取六张明确标记为 synthetic 的录制帧，通过真实的：

```text
ImageSequenceCameraBackend → CameraSource → FramePacket → SpotCentroidSensor → SensorEvent
```

生成原图、候选像素、重心叠加图、移动序列和完整事件：

```bash
python -m pip install -e 'packages/python[classical-trackers]'
python examples/spot-centroid/run.py
python examples/spot-centroid/run.py --output sensors/tracker.spot-centroid/assets
```

输出坐标单位是 pixel。示例没有空间标定，不代表机械位移、振幅或真实实验计量精度。
