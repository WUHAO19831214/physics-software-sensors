# 摄像头采集软件传感器

[English](README.md) | **简体中文** | [日本語](README.ja.md)

Sensor ID: `camera.capture` · Implementation version: `0.3.0` · Maturity: `experimental` · Evidence: `E1` · Release: `v0.6.0`

<!-- section:name -->
## 名称
摄像头采集软件传感器

<!-- section:description -->
## 一句话介绍
输出带明确时间戳、后端信息和采集质量元数据的摄像头或图像序列帧。

<!-- section:physics-use -->
## 典型物理实验用途
为运动、振动、轨迹、光斑和声音—视觉同步实验提供视觉输入，不耦合原项目 UI 或物理业务逻辑。

<!-- section:measurement -->
## 它实际测到什么
直接观测图像像素与采集时间/状态。位置、位移、速度、振幅需要后续 Sensor；转换为物理单位还必须标定。

<!-- section:sources -->
## 来源项目
| 仓库 | Commit | 原文件/用途 |
| --- | --- | --- |
| [audio-visual-soundfield-tracker-stable](https://github.com/WUHAO19831214/audio-visual-soundfield-tracker-stable) | `85740d686c67452a057540edb564d713e01ccc51` | `src/browser_capture.py`、`camera_devices.py`、`local_capture.py`、`camera_processor.py`；OpenCV/WebRTC 帧 |
| [spot-vibration-tracking-system-20260508-171952](https://github.com/WUHAO19831214/spot-vibration-tracking-system-20260508-171952) | `7f0d91cc73afafaecc54acc46b2b9d69375d994a` | `app.js`；camera→canvas 光斑处理 |
| [forced-vibration-af-analyzer-20260502-122715](https://github.com/WUHAO19831214/forced-vibration-af-analyzer-20260502-122715) | `c3f58175a09ff29cacdfb976a5055758c4eff619` | `app.js`；摄像头选择与振动输入 |
| [physics-experiment-bridge-mvp](https://github.com/WUHAO19831214/physics-experiment-bridge-mvp) | `8bba87df6475cae1e595fc925551db8bea83fb68` | `src/camera/CameraCapturePanel.tsx`、`cameraUtils.ts` |
| [ampere-force-visualizer-teacher-yanan](https://github.com/WUHAO19831214/ampere-force-visualizer-teacher-yanan) | `cb073e89d6d87129287030f1df08bd540504eb39` | 教师端相同 camera 边界 |

<!-- section:how-it-works -->
## 工作原理
后端 → 读取帧 → 墙钟/单调时钟 → 像素与媒体元数据 → 请求值/实测速率和状态 → `FramePacket`。当前 Python 后端是 OpenCV 与确定性图像序列回放。

<!-- section:input -->
## 输入
摄像头设备/后端配置、请求宽高/FPS，以及可选图像序列。浏览器 camera 仍是跨语言契约，不是当前 Python 实现。

<!-- section:output -->
## 输出
camera `FramePacket`：frame/run/sequence ID、尺寸、颜色/媒体类型、observed/monotonic time、后端状态和质量 flags。

<!-- section:demo -->
## Demo
[![Synthetic 回放帧](assets/captured-frame.png)](assets/README.md) Synthetic replay 只证明 adapter 路径，不证明真实摄像头兼容性或计时精度。

<!-- section:example -->
## 最小示例
运行 [python-camera-capture](../../examples/python-camera-capture/README.md)，使用 `CameraSource` 和 `ImageSequenceCameraBackend`。

<!-- section:distribution -->
## 分发 / 下载
Python package `0.5.0`；[camera.capture-0.3.0.zip](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/camera.capture-0.3.0.zip)。Bundle 不复制 package core。

<!-- section:evidence -->
## 证据等级
`E1`：只有确定性 synthetic 图像序列回放。

<!-- section:maturity -->
## 成熟度
`experimental`；manifest 仍为 `incubating/adapter-present`。页面完整不会自动升级。

<!-- section:limitations -->
## 已知限制
请求 FPS/分辨率可能不同于后端 nominal/measured 值。真实摄像头、驱动、丢帧和计时精度没有 E4 证据。

<!-- section:benchmark -->
## Benchmark
见[采集回放 benchmark](benchmarks/README.md)和仓库[汇总](../../docs/benchmark-summary.md)。

<!-- section:provenance -->
## 来源追溯
文件/符号级抽取与验证见 [SOURCE.md](SOURCE.md)，机器事实见 [sensor.json](sensor.json)。
