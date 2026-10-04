[English](fringelab-toolkit.md) | [简体中文](fringelab-toolkit.zh-CN.md) | [日本語](fringelab-toolkit.ja.md)

<!-- section:overview -->
## FringeLab 可复用组件套件

两批组件均收录在 `@physics-software-sensors/fringelab` 0.1.0。固定来源版本为 `webcam-laser-fringelab@37a8b3996791790a22980b0d562996a65a3a65ef`，原应用保持原样。计算器、叠加控件和图像/相机工具可以单独引用，无须依赖 Next.js。

<!-- section:catalog -->
## 可以复用的组件

计算器：纯算式解析器与可移动 React 浮窗。ROI：原图像素坐标、旋转/缩放和显示坐标映射。虚拟尺：端点/整体拖动、角度吸附、磁性对齐和毫米刻度。人工标定：确认后的两点及分段多点映射。剖面：通道选择、相对 DN、背景扣除、饱和质量、平滑、峰谷、亚像素中心、FWHM 和自相关周期。自动尺：保留已有水平/旋转/透视识别以及限定区域方式，人工模式可随时补充。浏览器工具：本地图像/HEIC 输入、按需尺标 OCR、相机采集/参数锁定及导出。光学：干涉/衍射反演、多级回归、不确定度和确定性模拟。

<!-- section:run -->
## 运行和引入其他项目

在仓库根目录执行下面的命令。另一个项目可以安装本地构建的 core 和 FringeLab 两个 tgz。纯算法、标准 Sensor、浏览器辅助工具和可选 React UI 分别提供入口；完整示例展示如何组合使用。

```sh
npm --prefix packages/typescript ci
npm --prefix packages/typescript run build
npm --prefix packages/fringelab ci
npm --prefix packages/fringelab test
npm --prefix examples/web-fringelab-toolkit ci
npm --prefix examples/web-fringelab-toolkit run dev
# Local artifacts + clean-install smoke test:
python3 tools/build_fringelab_artifacts.py
```

<!-- section:measurement -->
## 测量工作流

载入预设 650 nm 示例，确认虚拟尺的 30 mm 长度，再计算。多点模式允许在原图添加尺标并编辑读数。自动识别/OCR 填入候选，核对单位和长度后再应用。相机先冻结图像再标定；更换图像清除旧标定，ROI/参数修改使旧计算失效。强度是 DN/相机相对响应，不能直接称作 lux 或 W/m²。多点映射是一维分段尺度，不是透视单应变换。饱和截断的峰值不能恢复丢失幅度或可靠峰宽。

<!-- section:verification -->
## 验证和复用证据

18 个提取文件固定了来源哈希；计算器、ROI、人工/自动尺、剖面、模拟和反演结果在数组/时间归一化后与原版本完全一致。原测试及适配器测试覆盖时间、错误、取消和标定失效。浏览器生产构建验证双计算器、焦点恢复、两点/多点标定、自动识别、反演及 390 px 布局。这些证据来自合成图像和离线路径，实机、真实照片误差分布和光学计量精度尚未测量。

<!-- section:provenance -->
## 来源和打包

来源所有者已明确授权将这些组件收录到本 MIT 仓库；提取的自有代码使用目标仓库 MIT，OCR/HEIC 等第三方许可证独立保留。HEIC 可选且按需加载，OCR 可能获取引擎/语言资源。未发布到 npm registry。既有 v0.6.0 七个 Sensor Bundle 保持原样，新套件 tgz 和两个新 Sensor Bundle 可本地打包使用。

[Package API](../packages/fringelab/README.md) · [example](../examples/web-fringelab-toolkit/README.md) · [source](../packages/fringelab/SOURCE.md) · [evidence](../benchmarks/results/fringelab-extraction-2026-10-05.md)

![FringeLab production example, synthetic fixture](assets/fringelab-toolkit.png)
