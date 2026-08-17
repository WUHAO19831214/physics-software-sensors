# 物理实验软件传感器库

[English Docs](https://wuhao19831214.github.io/physics-software-sensors/) | **简体中文** | [日本語 Docs](https://wuhao19831214.github.io/physics-software-sensors/ja/)

Markdown sources: [English](README.md) | **简体中文** | [日本語](README.ja.md)

<!-- section:introduction -->
## 它是什么？

**面向物理实验的可复用软件传感器基础层。** 它把摄像头帧、屏幕像素和图像算法观测统一为可追溯的 `FramePacket` 与 `SensorEvent`，供后续物理实验项目复用。

仓库也承载处理 Sensor 输出的可复用配套处理工具；这些工具不会假装产生新的直接观测。

这是长期维护的基础能力库，不是新的实验应用。来源项目保持原状，继续作为历史实现和实际使用情境的事实来源。

```text
物理实验项目
      ↓
可复用成熟能力
      ↓
物理实验软件传感器库
      ↓
未来物理实验项目
```

成熟能力通过 adapter 渐进抽取，对固定来源 commit 做测试、文档和 benchmark，再服务未来项目。像素位置、OCR 文本、置信度和边界框是软件直接观测，不会自动成为经标定的物理量。

```text
物理 / 软件来源
        ↓
采集 Sensor → FramePacket
        ↓
处理 Sensor → SensorEvent / 标量测量值
        ↓
配套处理工具
        ↓
物理实验应用
```

例如：`screen.capture → ocr.number → vector.compose-3d → 三维合矢量`。最后一步只重建已有标量测量值，不感知新的物理量。

<!-- section:language-access -->
## 语言访问

仓库三语内容完整性：**PASS**。英文、简体中文、日文 Markdown 都是完整的来源文档。如果某些地区的 GitHub 文件查看页暂时失败，仍可从仓库首页获得以下简要说明：

- **English quick summary:** A reusable software sensing layer for physics experiments with 7 Software Sensors, 1 Companion Processing Tool and 8 public capabilities. It separates direct image/screen/OCR/tracking observations from downstream physical quantities. The public `v0.6.0` contains seven Sensor Bundles; `vector.compose-3d` remains an unreleased experimental Tool. The trilingual documentation website is now served by GitHub Pages from `main /docs`.
- **日本語クイックガイド：**物理実験向けの再利用可能なソフトウェアセンサー基盤であり、7 個の Software Sensor、1 個の Companion Processing Tool、合計 8 項目の公開 capability を提供します。画像・画面・OCR・追跡の直接観測と下流の物理量は区別されます。公開 `v0.6.0` には 7 個の Sensor Bundle が含まれ、`vector.compose-3d` は未リリースの experimental Tool です。3 言語の static reader は GitHub Pages の `main /docs` から公開されています。

<!-- section:project-status -->
## 项目状态

**7 个软件传感器 · 1 个配套处理工具 · 共 8 项可复用公开能力** · 英文 / 简体中文 / 日文

7 个 adapter 和该工具目前均为 experimental。公开 `v0.6.0` Release 包含 7 个 Sensor Bundle；工具尚未发布。首次 E5 下游复用已经完成，但不能把任何 Sensor 描述为已经全面 validated。

<!-- section:catalog -->
## 传感器目录

| Sensor | 用途 | 语言 | 成熟度 | 证据 | 示例 | 下载 |
| --- | --- | --- | --- | --- | --- | --- |
| [`camera.capture`](sensors/camera.capture/README.zh-CN.md) | 带时间/后端信息的摄像头帧 | Python | experimental | E1 | [示例](examples/python-camera-capture/README.md) | [bundle](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/camera.capture-0.3.0.zip) |
| [`screen.capture`](sensors/screen.capture/README.zh-CN.md) | 用户授权的屏幕/窗口像素 | TypeScript | experimental | E1 | [示例](examples/web-screen-capture/README.md) | [bundle](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/screen.capture-0.3.0.zip) |
| [`ocr.number`](sensors/ocr.number/README.zh-CN.md) | 从图像 ROI 读取数字 | TypeScript | experimental | E3 | [示例](examples/web-number-ocr/README.md) | [bundle](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/ocr.number-0.2.0.zip) |
| [`tracker.color-marker`](sensors/tracker.color-marker/README.zh-CN.md) | HSV/轮廓颜色标记追踪 | Python | experimental | E2 | [示例](examples/python-color-marker/README.md) | [bundle](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.color-marker-0.2.0.zip) |
| [`tracker.spot-centroid`](sensors/tracker.spot-centroid/README.zh-CN.md) | 光斑亮度加权重心 | Python | experimental | E5 | [示例](examples/spot-centroid/README.md) | [bundle](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.spot-centroid-0.4.0.zip) |
| [`tracker.template`](sensors/tracker.template/README.zh-CN.md) | ROI 初始化的单目标追踪 | Python | experimental | E3 | [示例](examples/python-template-tracker/README.md) | [bundle](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.template-0.4.0.zip) |
| [`tracker.yolo`](sensors/tracker.yolo/README.zh-CN.md) | 多目标检测/追踪 adapter | Python | experimental | E2 | [示例](examples/python-yolo-tracker/README.md) | [bundle](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.yolo-0.5.0.zip) |

完整信息见[传感器目录](docs/sensor-catalog.zh-CN.md)。证据等级表示实际跑过的路径；成熟度是另一项发布决策。

<!-- section:companion-tools -->
### 配套处理工具

| Tool | 用途 | 语言 | 状态 | 示例 | 文档 |
| --- | --- | --- | --- | --- | --- |
| [`vector.compose-3d`](processing/vector.compose-3d/README.zh-CN.md) | 从标量分量进行三维矢量合成与重建 | TypeScript | experimental | [Web demo](examples/web-vector-compose-3d/README.md) | [Tool Page](processing/vector.compose-3d/README.zh-CN.md) |

完整信息见[配套工具目录](docs/tool-catalog.zh-CN.md)。配套工具构成可扩展的测量处理层，不计入 Sensor 数量。

<!-- section:quick-start -->
## 快速开始

先阅读[快速开始](docs/getting-started.zh-CN.md)，再从 [`v0.6.0` Experimental Release](https://github.com/WUHAO19831214/physics-software-sensors/releases/tag/v0.6.0) 选择 Python wheel 或 TypeScript tgz。本项目没有发布到 PyPI 或 npm registry。

```bash
python -m pip install './physics_software_sensors-0.5.0-py3-none-any.whl[classical-trackers]'
npm install ./physics-software-sensors-core-0.3.0.tgz
```

<!-- section:download -->
## 下载

Release 包含一个 Python wheel、一个 TypeScript tgz、七个 Sensor Bundle、`release-manifest.json` 和 `SHA256SUMS`。Sensor Bundle 是便于阅读的文档/示例包，不复制公共 core。参阅[下载传感器](docs/downloading-sensors.zh-CN.md)和[安装](docs/installation.zh-CN.md)。

<!-- section:capability-showcase -->
## 能力总览

[![Physics Software Sensors：7 个软件传感器和 1 个配套处理工具](docs/assets/capability-showcase.png)](docs/capability-showcase.zh-CN.md)

图中汇总了 standalone、synthetic 和 replay 演示，各能力的证据等级并不相同；YOLO tile 明确是 **recorded detector replay**，不是真实 YOLO inference。图片只是增强展示；即使图片服务不可用，下面的文字链接仍是可靠入口。

[摄像头采集](sensors/camera.capture/README.zh-CN.md) · [屏幕采集](sensors/screen.capture/README.zh-CN.md) · [数字 OCR](sensors/ocr.number/README.zh-CN.md) · [颜色标记追踪](sensors/tracker.color-marker/README.zh-CN.md) · [光斑重心](sensors/tracker.spot-centroid/README.zh-CN.md) · [模板 / 单目标追踪](sensors/tracker.template/README.zh-CN.md) · [YOLO 追踪](sensors/tracker.yolo/README.zh-CN.md) · [三维矢量合成](processing/vector.compose-3d/README.zh-CN.md)

覆盖：**7/7 个软件传感器 + 1/1 个配套处理工具 = 8/8 项可复用公开能力**。进入三语[能力展示详情页](docs/capability-showcase.zh-CN.md)可查看八张独立 demo 图及其证据边界。

<!-- section:principles -->
## 核心原则

1. 不破坏或静默改写来源项目。
2. 来源追溯固定到仓库、完整 commit SHA、路径和符号。
3. 保存原始观测，明确区分后续派生值。
4. 显式记录时间、坐标、单位、置信度和不确定度。
5. 保守说明证据、成熟度、许可证和模型边界。

<!-- section:long-term-workflow -->
## 长期工作流

```text
新的物理实验项目
      ↓
可复用的成熟能力
      ↓
Sensor Intake
      ↓
Physics Software Sensors
      ↓
Experimental / Validation / Release
      ↓
未来物理实验项目
```

今后的工作通过 [Sensor Intake](docs/sensor-intake.zh-CN.md)、[新增 Sensor 操作说明](docs/agent-recipes/add-new-sensor.md)或已有 Sensor 维护轨道进入，不再默认创建新 Phase。首次从抽取到复用的完整周期见[首次完整复用闭环](docs/first-reuse-loop.zh-CN.md)。

<!-- section:documentation -->
## 文档

- [三语文档网站](https://wuhao19831214.github.io/physics-software-sensors/zh-CN/)
- [传感器目录](docs/sensor-catalog.zh-CN.md)
- [配套工具目录](docs/tool-catalog.zh-CN.md)
- [能力展示详情](docs/capability-showcase.zh-CN.md)
- [快速开始](docs/getting-started.zh-CN.md)
- [证据与成熟度](docs/evidence-and-maturity.zh-CN.md)
- [Sensor 接入流程](docs/sensor-intake.zh-CN.md)
- [首次完整复用闭环](docs/first-reuse-loop.zh-CN.md)和[维护指南](docs/maintenance.md)
- [当前项目状态](docs/project-status.md)
- [术语](docs/i18n/terminology.md)和 [i18n 风格指南](docs/i18n/style-guide.md)
- [Demo 素材清单](docs/demo-asset-inventory.md)
- [架构](docs/architecture.md)、[数据格式](docs/data-format.md)、[benchmark](docs/benchmarking.md)
- [v0.6.0 Release](https://github.com/WUHAO19831214/physics-software-sensors/releases/tag/v0.6.0)

<!-- section:development -->
## 开发与校验

```bash
python3 tools/validate_repo.py
pytest
npm --prefix packages/typescript test
```

参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。新 Sensor 或重大能力必须走正式 intake；普通 bugfix 不需要。

<!-- section:non-goals -->
## 当前非目标

- 不声称 stable、production-ready、measurement-grade 或 metrology-ready。
- 不自动下载 YOLO 模型，也不捆绑模型权重。
- 不强制来源实验项目迁移。
- 不发布 PyPI/npm；首次已合并的 E5 接入是离线回放路径，不替换下游实时摄像头实现。

<!-- section:license -->
## 许可

本仓库自有代码和文档采用 MIT。来源代码、模型、数据和依赖继续遵守各自许可证边界；参阅 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

最新 handoff：[.agent-handoff/latest.md](.agent-handoff/latest.md) · [.agent-handoff/latest.json](.agent-handoff/latest.json)
