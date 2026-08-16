# 软件传感器目录

本页是仓库级入口。状态描述的是 **physics-software-sensors 中的实现**，不是来源项目的成熟度。

| Sensor | 中文名称 | 类型 | 主要来源 | 状态 | Demo | Python | TypeScript |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [`camera.capture`](../sensors/camera.capture/README.md) | 摄像头采集 | source | 声音—视觉稳定版等五仓 | experimental | [synthetic replay](../sensors/camera.capture/assets/captured-frame.png) | CameraSource + OpenCV/replay | browser contract planned |
| [`screen.capture`](../sensors/screen.capture/README.md) | 屏幕/窗口采集 | source | 多源实验桥、安培力教师端 | experimental | [synthetic replay](../sensors/screen.capture/assets/captured-screen-frame.png) | planned | browser + replay source |
| [`ocr.number`](../sensors/ocr.number/README.md) | 数字 OCR | processor | 多源实验桥、安培力教师端 | experimental | [synthetic pixel demo](../sensors/ocr.number/assets/overview.png) | planned | Tesseract/replay adapter |
| [`tracker.color-marker`](../sensors/tracker.color-marker/README.md) | 颜色标记追踪 | processor | 声音—视觉稳定版、多源实验桥 | experimental | [synthetic standalone demo](../sensors/tracker.color-marker/assets/overview.png) | adapter | planned |
| [`tracker.spot-centroid`](../sensors/tracker.spot-centroid/README.md) | 光斑重心识别 | processor | 光斑追踪系统、受迫振动系统 | experimental | [synthetic centroid replay](../sensors/tracker.spot-centroid/assets/overview.png) | adapter | planned |
| [`tracker.template`](../sensors/tracker.template/README.md) | 模板/单目标追踪 | processor | 声音—视觉稳定版 | experimental | [real OpenCV synthetic replay](../sensors/tracker.template/assets/overview.png) | adapter | planned |
| [`tracker.yolo`](../sensors/tracker.yolo/README.md) | YOLO 检测与追踪 | processor | 声音—视觉稳定版 | contract-only | pending | planned | planned |

## 状态含义

- `contract-only`：只有页面、manifest 和契约，没有本仓库实现；
- `experimental`：已有独立适配器和离线测试，但未完成真实设备/课堂验证；
- `validated`：完成规定的 L1/L2 基准和来源兼容验证；
- `stable`：公开 API、下游试点、版本兼容和回退均已验证。

完整成熟度流程见 [版本与升级流程](versioning-and-upgrades.md)。图片可用性与版权判断见 [资产盘点](asset-inventory.md)。

Phase 3B 完成后为 **6 / 7 experimental adapters**；`tracker.yolo` 因模型 artifact、权重许可和 inference/ByteTrack backend 尚未审查，继续保持 contract-only。
