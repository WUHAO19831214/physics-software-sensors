# Python package

目标发行名为 `physics-software-sensors`，import 名为 `physics_sensors`。公共 core 不依赖实验 UI；具体传感器通过可选依赖安装。

```bash
python -m pip install -e 'packages/python[color-marker]'
```

当前 `0.2.0` 提供实验性的 `physics_sensors.tracking.ColorMarkerTracker` / `ColorMarkerSensor`。Phase 1 的 `physics_software_sensors` import 暂时作为兼容 re-export 保留，新代码不应使用它。

所有序列化输出仍必须满足根目录 JSON Schema。实验性适配器不等于真实设备精度已验证。
