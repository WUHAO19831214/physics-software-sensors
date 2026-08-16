# Screen Capture Sensor

## 屏幕/窗口采集软件传感器

> 在用户主动授权后，把选定屏幕、窗口或浏览器标签页的像素帧封装成 FramePacket，供 OCR 等传感器使用。

**状态：contract-only** · **Sensor ID：** `screen.capture` · **版本：** `0.1.0`

## 典型物理实验用途

多源实验桥和安培力教师端读取原实验软件屏幕上显示的传感器数值。它直接采集的是屏幕像素，不是设备 SDK、串口或数据库数据。

## 来源项目

| 项目 | 仓库 | commit | 原实现文件 | 用途 |
| --- | --- | --- | --- | --- |
| 多源实验桥 | [`physics-experiment-bridge-mvp`](https://github.com/WUHAO19831214/physics-experiment-bridge-mvp) | `8bba87df6475cae1e595fc925551db8bea83fb68` | `src/screen/ScreenCapturePanel.tsx`、`screenCaptureRuntime.ts` | `getDisplayMedia`、流状态和 OCR 输入 |
| 安培力教师端 | [`ampere-force-visualizer-teacher-yanan`](https://github.com/WUHAO19831214/ampere-force-visualizer-teacher-yanan) | `cb073e89d6d87129287030f1df08bd540504eb39` | 同名 screen 文件、`docs/SENSOR_INTEGRATION.md` | Fy/Fz 屏幕读数链路 |

## 工作原理

```text
用户操作 → getDisplayMedia 授权 → 视频帧 → 时间/尺寸/结束状态 → FramePacket
```

## 输入

用户选择的共享源、请求帧率、显示/裁剪配置。

## 输出

目标输出为 `frame-packet.screen-frame`，包含 frame ID、时间、媒体元数据、artifact 与质量信息。

## 使用效果

**demo asset pending**；来源没有可复用屏幕截图。见 [assets](assets/README.md)。

## 最小调用示例

目标 API（尚不可运行）：`for await (const frame of screenSensor.read()) { ... }`。见 [examples](examples/README.md)。

## 当前成熟度

contract-only；Phase 3 在 camera 后实现浏览器后端。

## 已知限制

每次由用户授权；页面不能静默读取桌面；刷新后需重新授权；窗口遮挡/缩放和浏览器调度会影响输出。

## Benchmark

见 [benchmarks](benchmarks/README.md)。

## Provenance

[SOURCE.md](SOURCE.md) · [sensor.json](sensor.json)
