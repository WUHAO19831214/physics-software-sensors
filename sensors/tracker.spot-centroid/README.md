# Spot Centroid Tracker

## 光斑重心识别软件传感器

> 在摄像头图像中按颜色权重寻找光斑，并输出光斑二维重心与锁定质量。

**状态：contract-only** · **Sensor ID：** `tracker.spot-centroid` · **版本：** `0.1.0`

## 典型物理实验用途

光斑追踪与受迫振动项目用红色光斑重心 `y` 形成轨迹，并在频率窗口内计算 `max(y)-min(y)`。直接观测是图像光斑重心；它不是振动物体机械位移。物理长度需要同平面标尺和光路/相机标定。

## 来源项目

| 项目 | 仓库 | commit | 原实现文件 | 用途 |
| --- | --- | --- | --- | --- |
| 光斑追踪系统 | [`spot-vibration-tracking-system-20260508-171952`](https://github.com/WUHAO19831214/spot-vibration-tracking-system-20260508-171952) | `7f0d91cc73afafaecc54acc46b2b9d69375d994a` | `app.js`、`docs/DATA_DICTIONARY.md` | 红色加权重心、轨迹和扫频窗口 |
| 受迫振动系统 | [`forced-vibration-af-analyzer-20260502-122715`](https://github.com/WUHAO19831214/forced-vibration-af-analyzer-20260502-122715) | `c3f58175a09ff29cacdfb976a5055758c4eff619` | `app.js`、`docs/SIGNAL_PROCESSING.md` | 光斑范围与设定频率关联 |

## 工作原理

```text
RGB 帧 → 红色 HSV/RGB 条件 → 候选像素加权和 → (x,y) 重心 → 锁定阈值 → SensorEvent
```

## 输入

摄像头/ImageData 帧、ROI、颜色阈值、权重与锁定阈值。

## 输出

目标输出为 `centroid_x/y`、颜色权重和 lost 状态；窗口峰—峰范围属于后续聚合层。

## 使用效果

**demo asset pending**；来源没有提交截图。见 [assets](assets/README.md)。

## 最小调用示例

目标 API（尚不可运行）：`SpotCentroidSensor.process(frame)`。见 [examples](examples/README.md)。

## 当前成熟度

contract-only；按路线图在 camera/screen 后进入 Phase 3。

## 已知限制

曝光、散斑、拖影、中心发白和背景红色会偏移重心；设定频率不是实测频率；峰—峰光斑范围不是机械单边振幅。

## Benchmark

见 [benchmarks](benchmarks/README.md)。

## Provenance

[SOURCE.md](SOURCE.md) · [sensor.json](sensor.json)
