# Python package

目标发行名为 `physics-software-sensors`，import 名为 `physics_sensors`。公共 core 不依赖实验 UI；具体传感器通过可选依赖安装。

```bash
python -m pip install -e 'packages/python[color-marker,camera-opencv,classical-trackers]'
# Only for an explicitly reviewed local YOLO artifact:
python -m pip install -e 'packages/python[yolo-runtime]'
```

当前 `0.5.0` 提供 `physics_sensors.capture.CameraSource`、`ImageSequenceCameraBackend`、可选 `OpenCVCameraBackend`，以及 Color/Spot/Template/YOLO 四个 tracking sensor。`YoloTrackerSensor` 默认可通过 `RecordedDetectorBackend` 完全离线使用；真实 `YoloDetectorBackend` 需要显式本地 `ModelArtifact`，会校验 SHA，不自动下载权重。OpenCV extras 统一选择 `opencv-contrib-python-headless`；core 与 recorded backends 仍可独立 import。Phase 1 的 `physics_software_sensors` import 暂作兼容 re-export。

GitHub Release wheel 的安装方法见 [installation](../../docs/installation.md)。Recorded YOLO 使用 `yolo-recorded` extra（仅 NumPy）；`yolo-runtime` 不默认安装，Release 也不包含模型。

所有序列化输出仍必须满足根目录 JSON Schema。实验性适配器不等于真实设备精度已验证。
