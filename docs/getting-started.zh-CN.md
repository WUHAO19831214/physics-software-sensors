# 快速开始

[English](getting-started.md) | **简体中文** | [日本語](getting-started.ja.md)

<!-- section:choose -->
## 1. 先确定直接观测

需要像素时选择 camera/screen capture，需要读取显示文字时选择 OCR，需要图像位置/边界框时选择 tracker。如果目标是位移、力、频率或角度，应另外记录后续标定/推导链。

<!-- section:download -->
## 2. 下载并校验

从 [`v0.6.0` Experimental Release](https://github.com/WUHAO19831214/physics-software-sensors/releases/tag/v0.6.0) 下载，验证 `SHA256SUMS`，再按[安装说明](installation.zh-CN.md)操作。本项目没有 registry 包。

<!-- section:run -->
## 3. 运行独立示例

打开对应 [Sensor Page](sensor-catalog.zh-CN.md)，只安装它声明的依赖并运行小型示例。Recorded/synthetic 示例证明它能离开来源应用运行，但不证明真实设备精度。

### 感知之后：处理测量值

实验需要派生表示时，再进入独立的[配套工具目录](tool-catalog.zh-CN.md)。例如，`screen.capture → ocr.number → vector.compose-3d` 把屏幕显示的标量分量重建为可追溯三维合矢量。该工具不产生新的观测，而且当前未发布的工具源码不属于 `v0.6.0`。

<!-- section:interpret -->
## 4. 保守解释结果

接入前阅读证据、成熟度、已知限制、benchmark 和 provenance。在下游比较成功前，保留来源项目旧路径和 rollback 机制。
