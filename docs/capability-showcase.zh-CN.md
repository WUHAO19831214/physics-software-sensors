# 能力展示详情

[English](capability-showcase.md) | **简体中文** | [日本語](capability-showcase.ja.md)

<!-- section:overview -->
## 概览

仓库首页只加载一张聚合预览图，以减少独立的 GitHub Raw/CDN 请求。用户主动进入本页后，仍可查看八项能力各自的详细演示。

[![Physics Software Sensors 能力总览](assets/capability-showcase.png)](../README.zh-CN.md)

聚合图由 `python3 tools/build_capability_showcase.py` 从下面八张图片可重复生成；脚本不访问网络，也不使用外部图床。

<!-- section:software-sensors -->
## 软件传感器

### 摄像头采集

[![合成录制摄像头帧](../sensors/camera.capture/assets/captured-frame.png)](../sensors/camera.capture/README.zh-CN.md)

把录制或实时摄像头图像组织为带时间信息的 `FramePacket`。图片是确定性的合成摄像头回放，不代表真实硬件测试。

### 屏幕采集

[![合成共享窗口像素](../sensors/screen.capture/assets/captured-screen-frame.png)](../sensors/screen.capture/README.zh-CN.md)

把用户授权的屏幕或窗口像素组织为 `FramePacket`。图片使用合成的共享窗口像素。

### 数字 OCR

[![数字 OCR 回放](../sensors/ocr.number/assets/overview.png)](../sensors/ocr.number/README.zh-CN.md)

识别屏幕图像 ROI 中的文本并解析数字观测；它读取的是屏幕像素，不是设备 SDK 数值。

### 颜色标记追踪

[![颜色标记回放](../sensors/tracker.color-marker/assets/overview.png)](../sensors/tracker.color-marker/README.zh-CN.md)

寻找 HSV 颜色标记并报告图像坐标中心。像素位置不等于经过标定的物理位移。

### 光斑重心

[![光斑重心回放](../sensors/tracker.spot-centroid/assets/overview.png)](../sensors/tracker.spot-centroid/README.zh-CN.md)

报告图像 ROI 中光斑的亮度加权重心，并不直接测量机械位移。

### 模板 / 单目标追踪

[![单目标追踪回放](../sensors/tracker.template/assets/overview.png)](../sensors/tracker.template/README.zh-CN.md)

使用 OpenCV 单目标 backend 追踪初始化 ROI，输出 bbox/lost 状态；它不是静态模板匹配。

### YOLO 追踪

[![Recorded detector replay](../sensors/tracker.yolo/assets/overview.png)](../sensors/tracker.yolo/README.zh-CN.md)

通过 **recorded detector replay** 展示检测结果与 track ID。这张公开图片不是真实 YOLO 模型推理证据。

<!-- section:companion-tools -->
## 配套处理工具

### 三维矢量合成

[![录制 OCR 分量合成为三维合矢量](../processing/vector.compose-3d/assets/overview.png)](../processing/vector.compose-3d/README.zh-CN.md)

把可追溯的 x/y/z 标量分量合成为合矢量及与渲染器无关的模型。它派生已有观测，不会冒充新的 Sensor 直接观测。参阅[独立 Web 示例](../examples/web-vector-compose-3d/README.md)。

<!-- section:evidence -->
## 证据边界

这些是代表性的 standalone、synthetic、recorded 或 replay 演示。不同能力的证据等级不同；任何单张图片都不能单独证明真实设备精度、标定、重复性或计量性能。规范 demo 资产继续保存在本仓库并纳入版本控制。
