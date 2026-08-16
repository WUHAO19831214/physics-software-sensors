# Python package

目标发行名为 `physics-software-sensors`，import 名为 `physics_sensors`。公共 core 不依赖实验 UI；具体传感器通过可选依赖安装。

```bash
python -m pip install -e 'packages/python[color-marker,camera-opencv]'
```

当前 `0.3.0` 提供 `physics_sensors.capture.CameraSource`、`ImageSequenceCameraBackend`、可选 `OpenCVCameraBackend`，并保留 Phase 2 的 `ColorMarkerTracker` / `ColorMarkerSensor`。不安装 `camera-opencv` 时仍可导入 core 与 recorded backend；只有真实 OpenCV start 会要求可选依赖。Phase 1 的 `physics_software_sensors` import 暂作兼容 re-export。

所有序列化输出仍必须满足根目录 JSON Schema。实验性适配器不等于真实设备精度已验证。
