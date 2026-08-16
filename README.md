# 物理实验软件传感器库

**Physics Software Sensors** (`physics-software-sensors`) 面向物理实验教学与研究，把摄像头、屏幕和算法产生的观测抽象成可复用、可升级、可测试的“软件传感器”。

本仓库当前完成 **Phase 2D：首批试点完成与可视化演示**。现有来源仓库仍是历史实现与实际使用场景的事实来源；新库通过可追溯 adapter 渐进抽取，不要求来源项目立即接入，也不替换其 UI 或实验流程。

```text
Camera / Screen → FramePacket → Software Sensor → Measurement / SensorEvent → Physics Experiment
```

## Sensor Catalog

| Sensor | 一句话说明 | 状态 | Docs | Example | Benchmark |
| --- | --- | --- | --- | --- | --- |
| Camera Capture | 产生带时间和媒体元数据的摄像头帧 | contract-only | [Page](sensors/camera.capture/README.md) | [pending](sensors/camera.capture/examples/README.md) | [plan](sensors/camera.capture/benchmarks/README.md) |
| Screen Capture | 经用户授权采集屏幕/窗口像素帧 | contract-only | [Page](sensors/screen.capture/README.md) | [pending](sensors/screen.capture/examples/README.md) | [plan](sensors/screen.capture/benchmarks/README.md) |
| Number OCR | 从屏幕 ROI 保留 OCR 原文并解析数字 | experimental | [Page](sensors/ocr.number/README.md) | [pixel OCR](examples/web-number-ocr/README.md) | [status](sensors/ocr.number/benchmarks/README.md) |
| Color Marker Tracker | 用 HSV/轮廓连续追踪颜色标记 | experimental | [Page](sensors/tracker.color-marker/README.md) | [Python](examples/python-color-marker/README.md) | [golden](sensors/tracker.color-marker/benchmarks/README.md) |
| Spot Centroid Tracker | 输出图像中光斑的颜色加权重心 | contract-only | [Page](sensors/tracker.spot-centroid/README.md) | [pending](sensors/tracker.spot-centroid/examples/README.md) | [plan](sensors/tracker.spot-centroid/benchmarks/README.md) |
| Template Tracker | 初始化 ROI 后追踪单个实验物体 | contract-only | [Page](sensors/tracker.template/README.md) | [pending](sensors/tracker.template/examples/README.md) | [plan](sensors/tracker.template/benchmarks/README.md) |
| YOLO Tracker | 用显式模型 artifact 检测并追踪目标 | contract-only | [Page](sensors/tracker.yolo/README.md) | [pending](sensors/tracker.yolo/examples/README.md) | [plan](sensors/tracker.yolo/benchmarks/README.md) |

完整语言/来源对照见 [软件传感器目录](docs/sensor-catalog.md)。页面完整不等于算法已验证；状态以 manifest 和页面成熟度为准。

## Working demonstrations

| Color Marker Tracker | Number OCR |
| --- | --- |
| [![Synthetic color marker standalone result](sensors/tracker.color-marker/assets/overview.png)](sensors/tracker.color-marker/README.md) | [![Synthetic screen pixel OCR result](sensors/ocr.number/assets/overview.png)](sensors/ocr.number/README.md) |
| BGR frame → HSV/contour → position/lost SensorEvent | RGBA screen frame → ROI/preprocess → Tesseract.js → numeric SensorEvent |

两张图均由本仓库 standalone example 实际运行生成，输入明确为 synthetic，不是来源项目截图、真实设备数据或实验精度证据。

## 核心原则

1. **不破坏来源项目**：采用适配器式渐进迁移，不直接搬走或重写原仓库功能。
2. **原始观测优先**：保存原始算法输出、时间信息和质量标志；平滑值、物理换算值必须可区分。
3. **不伪造能力**：mock、占位实现、真实实现、经基准验证实现必须明确标注。
4. **时间和坐标显式化**：墙钟、单调时钟、源时间戳、像素坐标、归一化坐标和物理坐标不得混用。
5. **升级可追溯**：实现来源必须锚定仓库、完整 commit SHA、文件和验证记录。

## 快速导航

- [总体架构](docs/architecture.md)
- [软件传感器目录](docs/sensor-catalog.md)
- [来源图片与演示资产盘点](docs/asset-inventory.md)
- [许可证与来源边界](docs/licensing-and-provenance.md)
- [统一传感器接口](docs/sensor-interface.md)
- [统一数据格式](docs/data-format.md)
- [基准测试方案](docs/benchmarking.md)
- [版本与升级流程](docs/versioning-and-upgrades.md)
- [第一阶段路线图](docs/roadmap.md)
- [机器可读契约](contracts/README.md)
- [贡献指南](CONTRIBUTING.md)

## 目录结构

```text
physics-software-sensors/
├── contracts/                  # JSON Schema 与有效示例
│   ├── examples/
│   └── schemas/
├── sensors/                    # Sensor Page、来源、清单、资产、示例与 benchmark
├── packages/
│   ├── python/                 # physics-software-sensors / physics_sensors
│   └── typescript/             # @physics-software-sensors/core
├── examples/                   # 脱离原实验项目的最小示例
├── benchmarks/                 # 数据集、协议与结果的边界
├── docs/                       # 架构、接口、数据、盘点与路线图
├── templates/                  # 升级、基准和数据集记录模板
├── tests/                      # 契约与仓库一致性测试
└── tools/                      # 本地校验工具
```

## 本地校验

安装实验性 Python 颜色追踪与测试依赖：

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e 'packages/python[color-marker,dev]'
```

运行仓库校验、Python 测试和 TypeScript OCR 回放测试：

```bash
python tools/validate_repo.py
pytest
npm --prefix packages/typescript install
npm --prefix packages/typescript test
```

## 当前非目标

- 不整体搬运现有实验应用、UI 或业务 store；
- 不承诺硬实时、硬件同步或计量精度；
- 不提交摄像头原始视频、屏幕录制、个人图像、模型权重或未脱敏数据；
- 不把屏幕 OCR 表述成对实验设备 SDK 或内部数据的直接读取；
- 不把 `0.2.0` 实验性 adapter 描述为稳定、计量验证或真实设备兼容。

## 许可

代码与文档采用 [MIT License](LICENSE)。来源项目的代码、模型、数据与第三方依赖仍受各自许可证约束；未来迁移前必须单独完成许可证核查。
