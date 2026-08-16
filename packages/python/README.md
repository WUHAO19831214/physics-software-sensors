# Python package

目标发行名为 `physics-software-sensors`，import 名为 `physics_sensors`。公共 core 不依赖实验 UI；具体传感器通过可选依赖安装。

```bash
python -m pip install -e 'packages/python[color-marker,camera-opencv,classical-trackers]'
```

当前 `0.4.0` 提供 `physics_sensors.capture.CameraSource`、`ImageSequenceCameraBackend`、可选 `OpenCVCameraBackend`，以及 `ColorMarkerSensor`、`SpotCentroidSensor` 和 `TemplateTrackerSensor`。三个 OpenCV extra 统一选择 `opencv-contrib-python-headless`，避免同一环境同时安装相互冲突的 regular/contrib wheel，并为 CSRT/KCF/MIL 提供完整 factory；core 与 recorded camera backend 仍可独立 import。Phase 1 的 `physics_software_sensors` import 暂作兼容 re-export。

所有序列化输出仍必须满足根目录 JSON Schema。实验性适配器不等于真实设备精度已验证。
