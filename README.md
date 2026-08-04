# 物理实验软件传感器库

**Physics Software Sensors** (`physics-software-sensors`) 面向物理实验教学与研究，把摄像头、屏幕和算法产生的观测抽象成可复用、可升级、可测试的“软件传感器”。

本仓库当前处于 **Phase 1：文档与契约骨架**。它不会复制、重构或替换现有项目的实现；现有仓库仍是当前功能的运行载体和事实来源。本阶段只建立后续迁移所需的边界、数据契约、测试基线和升级记录方式。

## 首批传感器范围

| 传感器 ID | 能力 | 第一阶段状态 |
| --- | --- | --- |
| `camera.capture` | 浏览器或本机摄像头帧采集 | 契约骨架 |
| `screen.capture` | 经用户授权的屏幕/窗口帧采集 | 契约骨架 |
| `ocr.number` | ROI 数字 OCR 与解析 | 契约骨架 |
| `tracker.color-marker` | HSV/颜色标记追踪 | 契约骨架 |
| `tracker.yolo` | YOLO 检测与多目标追踪 | 契约骨架 |
| `tracker.template` | 初始化 ROI 后的模板/单目标追踪 | 契约骨架 |
| `tracker.spot-centroid` | 光斑颜色加权重心识别 | 契约骨架 |

“契约骨架”不等于新仓库已经实现算法。每项能力的来源、证据等级和已知边界见 [已有项目盘点](docs/source-inventory.md)。

## 核心原则

1. **不破坏来源项目**：采用适配器式渐进迁移，不直接搬走或重写原仓库功能。
2. **原始观测优先**：保存原始算法输出、时间信息和质量标志；平滑值、物理换算值必须可区分。
3. **不伪造能力**：mock、占位实现、真实实现、经基准验证实现必须明确标注。
4. **时间和坐标显式化**：墙钟、单调时钟、源时间戳、像素坐标、归一化坐标和物理坐标不得混用。
5. **升级可追溯**：实现来源必须锚定仓库、完整 commit SHA、文件和验证记录。

## 快速导航

- [总体架构](docs/architecture.md)
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
├── sensors/                    # 每类传感器的机器可读清单
├── packages/
│   ├── python/                 # Python Protocol 类型骨架
│   └── typescript/             # TypeScript 接口类型骨架
├── benchmarks/                 # 数据集、协议与结果的边界
├── docs/                       # 架构、接口、数据、盘点与路线图
├── templates/                  # 升级、基准和数据集记录模板
├── tests/                      # 契约与仓库一致性测试
└── tools/                      # 本地校验工具
```

## 本地校验

仅检查 JSON、清单、来源锚点与文档链接，不运行任何传感器算法：

```bash
python3 tools/validate_repo.py
```

完整 JSON Schema 校验需要开发依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
pytest
```

## 当前非目标

- 不从现有仓库复制算法实现；
- 不承诺硬实时、硬件同步或计量精度；
- 不提交摄像头原始视频、屏幕录制、个人图像、模型权重或未脱敏数据；
- 不把屏幕 OCR 表述成对实验设备 SDK 或内部数据的直接读取；
- 不发布可安装的稳定算法包。

## 许可

代码与文档采用 [MIT License](LICENSE)。来源项目的代码、模型、数据与第三方依赖仍受各自许可证约束；未来迁移前必须单独完成许可证核查。
