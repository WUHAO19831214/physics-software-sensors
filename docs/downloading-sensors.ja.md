# Sensor のダウンロード

[English](downloading-sensors.md) | [简体中文](downloading-sensors.zh-CN.md) | **日本語**

<!-- section:release -->
## Release

[`v0.6.0` Experimental](https://github.com/WUHAO19831214/physics-software-sensors/releases/tag/v0.6.0) から取得します。experimental/pre-stable であり、実機検証や計量検証を意味しません。

<!-- section:packages -->
## Package 全体

- Python: [`physics_software_sensors-0.5.0-py3-none-any.whl`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/physics_software_sensors-0.5.0-py3-none-any.whl)
- TypeScript: [`physics-software-sensors-core-0.3.0.tgz`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/physics-software-sensors-core-0.3.0.tgz)

<!-- section:bundles -->
## 個別 Sensor Bundle

| Sensor | Bundle |
| --- | --- |
| `camera.capture` | [`camera.capture-0.3.0.zip`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/camera.capture-0.3.0.zip) |
| `screen.capture` | [`screen.capture-0.3.0.zip`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/screen.capture-0.3.0.zip) |
| `ocr.number` | [`ocr.number-0.2.0.zip`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/ocr.number-0.2.0.zip) |
| `tracker.color-marker` | [`tracker.color-marker-0.2.0.zip`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.color-marker-0.2.0.zip) |
| `tracker.spot-centroid` | [`tracker.spot-centroid-0.4.0.zip`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.spot-centroid-0.4.0.zip) |
| `tracker.template` | [`tracker.template-0.4.0.zip`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.template-0.4.0.zip) |
| `tracker.yolo` | [`tracker.yolo-0.5.0.zip`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.yolo-0.5.0.zip) |

Sensor Bundle は Sensor Page、来歴、asset、example、依存情報を含みますが、共通実装 core は複製しません。参照先の wheel/tgz をインストールしてください。

<!-- section:integrity -->
## 完全性確認

[`SHA256SUMS`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/SHA256SUMS) を同じ directory に置いて実行します。

```bash
shasum -a 256 -c SHA256SUMS
```

[`release-manifest.json`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/release-manifest.json) には size、hash、source SHA、build environment が記録されています。完全性確認は Sensor の精度・互換性を証明しません。
