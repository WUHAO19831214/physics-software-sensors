# 软件传感器目录

[English](sensor-catalog.md) | **简体中文** | [日本語](sensor-catalog.ja.md)

<!-- section:catalog -->
## 可用传感器

状态描述本仓库中的实现，不代表历史来源项目的成熟度。

| Sensor | 用途 | 语言 | 成熟度 | 证据 | 示例 | 下载 |
| --- | --- | --- | --- | --- | --- | --- |
| [`camera.capture`](../sensors/camera.capture/README.zh-CN.md) | 摄像头帧和采集元数据 | Python | experimental | E1 | [运行](../examples/python-camera-capture/README.md) | [0.3.0](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/camera.capture-0.3.0.zip) |
| [`screen.capture`](../sensors/screen.capture/README.zh-CN.md) | 用户授权的屏幕/窗口像素 | TypeScript | experimental | E1 | [运行](../examples/web-screen-capture/README.md) | [0.3.0](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/screen.capture-0.3.0.zip) |
| [`ocr.number`](../sensors/ocr.number/README.zh-CN.md) | 从 ROI 读取数字 | TypeScript | experimental | E3 | [运行](../examples/web-number-ocr/README.md) | [0.2.0](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/ocr.number-0.2.0.zip) |
| [`tracker.color-marker`](../sensors/tracker.color-marker/README.zh-CN.md) | 颜色标记位置/丢失状态 | Python | experimental | E2 | [运行](../examples/python-color-marker/README.md) | [0.2.0](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.color-marker-0.2.0.zip) |
| [`tracker.spot-centroid`](../sensors/tracker.spot-centroid/README.zh-CN.md) | 光斑亮度加权重心 | Python | experimental | E2 | [运行](../examples/spot-centroid/README.md) | [0.4.0](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.spot-centroid-0.4.0.zip) |
| [`tracker.template`](../sensors/tracker.template/README.zh-CN.md) | ROI 初始化单目标追踪 | Python | experimental | E3 | [运行](../examples/python-template-tracker/README.md) | [0.4.0](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.template-0.4.0.zip) |
| [`tracker.yolo`](../sensors/tracker.yolo/README.zh-CN.md) | 多目标检测/追踪 adapter | Python | experimental | E2 | [运行](../examples/python-yolo-tracker/README.md) | [0.5.0](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.yolo-0.5.0.zip) |

<!-- section:status -->
## 状态含义

- `contract-only`：只有契约和文档，没有本仓库实现。
- `experimental`：已有独立 adapter 和离线证据，但可能缺少真实设备/下游验证。
- `validated`：适用的真实 runtime/device、指标和许可证门禁已通过。
- `stable`：validated API 已完成下游固定版本复用与回退验证。

证据等级不等于成熟度，参阅[证据与成熟度](evidence-and-maturity.zh-CN.md)。七项 Sensor 仍全部为 experimental，均无 E4/E5。真实 YOLO inference 仍是 not measured，且不分发模型权重。
