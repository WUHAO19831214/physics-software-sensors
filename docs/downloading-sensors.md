# Downloading software sensors / 获取软件传感器

首个公开版本是 [`v0.6.0` Experimental Release](https://github.com/WUHAO19831214/physics-software-sensors/releases/tag/v0.6.0)。它是 GitHub-only 的 experimental/pre-stable 发布，不代表 stable、真实设备兼容或计量验证。所有版本见 [Releases](https://github.com/WUHAO19831214/physics-software-sensors/releases)。

## A. Python package

下载 [`physics_software_sensors-0.5.0-py3-none-any.whl`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/physics_software_sensors-0.5.0-py3-none-any.whl)，然后按 [installation](installation.md) 选择所需 extra。一个 wheel 包含 Python core、Camera、Color、Spot、Template 和 YOLO adapter；默认不会安装 Ultralytics 或下载模型。

## B. TypeScript package

下载 [`physics-software-sensors-core-0.3.0.tgz`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/physics-software-sensors-core-0.3.0.tgz)，在 Node/web 项目中用本地路径安装。它包含 Screen Capture、Number OCR 和公共 TypeScript contract；没有发布到 npm registry。

## C. Single Sensor Bundle

若只想先理解或评估一个传感器，可下载对应 zip：

| Sensor | Bundle | Requires |
| --- | --- | --- |
| Camera Capture | [`camera.capture-0.3.0.zip`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/camera.capture-0.3.0.zip) | Python wheel + `camera-opencv`（真实相机） |
| Screen Capture | [`screen.capture-0.3.0.zip`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/screen.capture-0.3.0.zip) | TypeScript tgz |
| Number OCR | [`ocr.number-0.2.0.zip`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/ocr.number-0.2.0.zip) | TypeScript tgz；真实 OCR 可能获取语言数据 |
| Color Marker | [`tracker.color-marker-0.2.0.zip`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.color-marker-0.2.0.zip) | Python wheel + `color-marker` |
| Spot Centroid | [`tracker.spot-centroid-0.4.0.zip`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.spot-centroid-0.4.0.zip) | Python wheel + `classical-trackers` |
| Template Tracker | [`tracker.template-0.4.0.zip`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.template-0.4.0.zip) | Python wheel + `classical-trackers` |
| YOLO Tracker | [`tracker.yolo-0.5.0.zip`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.yolo-0.5.0.zip) | Python wheel + `yolo-recorded`；真实 inference 另需审核过的本地 artifact |

Sensor Bundle 是 **root README + Sensor Page + manifest + provenance + demo assets + minimal example + dependency/install/evidence metadata**。它不是一份脱离公共 core 的重复实现，也不鼓励复制单文件形成分叉。每个 zip 的 root `README.md` 只链接 bundle 内存在的入口；保存的完整 Sensor Page 若含仓库级链接，则明确指向 `BUNDLE.json` 中固定 SHA 的 canonical page。

## Integrity verification

把下载文件与 [`SHA256SUMS`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/SHA256SUMS) 放在同一目录：

```bash
shasum -a 256 -c SHA256SUMS
```

Linux 也可使用 `sha256sum -c SHA256SUMS`。[`release-manifest.json`](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/release-manifest.json) 另行记录文件大小、SHA-256、构建环境和 source Git SHA。发布后已重新下载全部 11 个附件并完成 11/11 校验；校验通过只证明文件完整性，不证明传感器精度或真实设备兼容性。
