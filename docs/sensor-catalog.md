# 软件传感器目录

本页是仓库级入口。状态描述的是 **physics-software-sensors 中的实现**，不是来源项目的成熟度。

| Sensor | 中文名称 | 类型 | 主要来源 | 状态 | Demo | Python | TypeScript |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [`camera.capture`](../sensors/camera.capture/README.md) | 摄像头采集 | source | 声音—视觉稳定版、光斑追踪系统 | contract-only | pending | planned | planned |
| [`screen.capture`](../sensors/screen.capture/README.md) | 屏幕/窗口采集 | source | 多源实验桥、安培力教师端 | contract-only | pending | planned | planned |
| [`ocr.number`](../sensors/ocr.number/README.md) | 数字 OCR | processor | 多源实验桥、安培力教师端 | experimental | pending | planned | replay adapter |
| [`tracker.color-marker`](../sensors/tracker.color-marker/README.md) | 颜色标记追踪 | processor | 声音—视觉稳定版、多源实验桥 | experimental | pending | adapter | planned |
| [`tracker.spot-centroid`](../sensors/tracker.spot-centroid/README.md) | 光斑重心识别 | processor | 光斑追踪系统、受迫振动系统 | contract-only | pending | planned | planned |
| [`tracker.template`](../sensors/tracker.template/README.md) | 模板/单目标追踪 | processor | 声音—视觉稳定版、多源实验桥 | contract-only | pending | Python planned | TypeScript planned |
| [`tracker.yolo`](../sensors/tracker.yolo/README.md) | YOLO 检测与追踪 | processor | 声音—视觉稳定版 | contract-only | pending | planned | planned |

## 状态含义

- `contract-only`：只有页面、manifest 和契约，没有本仓库实现；
- `experimental`：已有独立适配器和离线测试，但未完成真实设备/课堂验证；
- `validated`：完成规定的 L1/L2 基准和来源兼容验证；
- `stable`：公开 API、下游试点、版本兼容和回退均已验证。

完整成熟度流程见 [版本与升级流程](versioning-and-upgrades.md)。图片可用性与版权判断见 [资产盘点](asset-inventory.md)。
