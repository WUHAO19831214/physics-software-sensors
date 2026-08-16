# Camera Capture Sensor

## 摄像头采集软件传感器

> 把浏览器或本机摄像头产生的图像帧封装为带时间、尺寸、颜色空间和丢帧信息的 FramePacket。

**状态：contract-only** · **Sensor ID：** `camera.capture` · **版本：** `0.1.0`

## 典型物理实验用途

来源项目用摄像头拍摄人物、颜色标记和红色光斑，为轨迹、振动和视觉—声音同步实验提供图像。直接产物是图像帧，不是位置、速度或物理位移；这些由下游分析和标定得到。

## 来源项目

| 项目 | 仓库 | commit | 原实现文件 | 用途 |
| --- | --- | --- | --- | --- |
| 声音—视觉稳定版 | [`audio-visual-soundfield-tracker-stable`](https://github.com/WUHAO19831214/audio-visual-soundfield-tracker-stable) | `85740d686c67452a057540edb564d713e01ccc51` | `src/browser_capture.py`、`camera_devices.py`、`local_capture.py` | WebRTC/OpenCV 摄像头采集 |
| 光斑追踪系统 | [`spot-vibration-tracking-system-20260508-171952`](https://github.com/WUHAO19831214/spot-vibration-tracking-system-20260508-171952) | `7f0d91cc73afafaecc54acc46b2b9d69375d994a` | `app.js` | `getUserMedia` 实时光斑输入 |

## 工作原理

```text
设备选择/授权 → 视频帧 → 时间与媒体元数据 → artifact 引用 → FramePacket
```

## 输入

设备 ID、请求分辨率/FPS、权限和后端配置。

## 输出

目标输出为 `frame-packet.camera-frame`，包含 frame ID、时间、尺寸、颜色空间、镜像状态、artifact SHA-256 与丢帧质量信息。

## 使用效果

**demo asset pending**。来源固定 commit 没有可复用截图；见 [assets/README.md](assets/README.md)。

## 最小调用示例

目标 API（尚不可运行）：`async for frame in CameraCaptureSensor(...).read(): ...`。见 [examples](examples/README.md)。

## 当前成熟度

contract-only；计划在 Phase 3 首先抽取 OpenCV 文件/摄像头后端，再处理浏览器授权后端。

## 已知限制

请求 FPS/分辨率不等于实际值；权限、黑帧、设备中断和硬件时间戳必须分别验证；HTTP 可访问不证明相机工作。

## Benchmark

见 [benchmarks](benchmarks/README.md)。

## Provenance

[SOURCE.md](SOURCE.md) · [sensor.json](sensor.json)
