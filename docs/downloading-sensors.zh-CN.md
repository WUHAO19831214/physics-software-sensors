# 下载软件传感器

[English](downloading-sensors.md) | **简体中文** | [日本語](downloading-sensors.ja.md)

<!-- section:release -->
## Release

从 [`v0.6.0` Experimental](https://github.com/WUHAO19831214/physics-software-sensors/releases/tag/v0.6.0) 下载。它是 experimental/pre-stable，不代表真实设备或计量验证。

<!-- section:packages -->
## 完整软件包

- Python：[`physics_software_sensors-0.5.0-py3-none-any.whl`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/physics_software_sensors-0.5.0-py3-none-any.whl)
- TypeScript：[`physics-software-sensors-core-0.3.0.tgz`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/physics-software-sensors-core-0.3.0.tgz)

<!-- section:bundles -->
## 单个 Sensor Bundle

| Sensor | Bundle |
| --- | --- |
| `camera.capture` | [`camera.capture-0.3.0.zip`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/camera.capture-0.3.0.zip) |
| `screen.capture` | [`screen.capture-0.3.0.zip`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/screen.capture-0.3.0.zip) |
| `ocr.number` | [`ocr.number-0.2.0.zip`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/ocr.number-0.2.0.zip) |
| `tracker.color-marker` | [`tracker.color-marker-0.2.0.zip`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.color-marker-0.2.0.zip) |
| `tracker.spot-centroid` | [`tracker.spot-centroid-0.4.0.zip`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.spot-centroid-0.4.0.zip) |
| `tracker.template` | [`tracker.template-0.4.0.zip`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.template-0.4.0.zip) |
| `tracker.yolo` | [`tracker.yolo-0.5.0.zip`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.yolo-0.5.0.zip) |

Sensor Bundle 包含 Sensor Page、来源追溯、资产、示例和依赖说明，但**不会**复制公共实现 core；仍需安装它引用的 wheel/tgz。

<!-- section:integrity -->
## 完整性校验

把 [`SHA256SUMS`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/SHA256SUMS) 与下载文件放在一起并运行：

```bash
shasum -a 256 -c SHA256SUMS
```

[`release-manifest.json`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/release-manifest.json) 记录大小、hash、来源 SHA 和构建环境。完整性一致不等于 Sensor 精度或兼容性已验证。
