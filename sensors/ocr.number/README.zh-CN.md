# 数字 OCR 软件传感器

[English](README.md) | **简体中文** | [日本語](README.ja.md)

Sensor ID: `ocr.number` · Implementation version: `0.2.0` · Maturity: `experimental` · Evidence: `E3` · Release: `v0.6.0`

<!-- section:name -->
## 名称
数字 OCR 软件传感器
<!-- section:description -->
## 一句话介绍
从帧的 ROI 读取数字显示，同时保留 raw text、解析值、置信度、耗时、warning 和明确失败。
<!-- section:physics-use -->
## 典型物理实验用途
当没有直接 SDK 数据时，读取现有仪器软件显示值，用于教学可视化或同步分析。
<!-- section:measurement -->
## 它实际测到什么
路径是“软件显示 → 屏幕像素 → OCR 文本 → 数字解析”，不是直接读取设备内部数据；单位和物理范围检查来自配置/下游逻辑。
<!-- section:sources -->
## 来源项目
| 仓库 | Commit | 原文件/用途 |
| --- | --- | --- |
| [physics-experiment-bridge-mvp](https://github.com/WUHAO19831214/physics-experiment-bridge-mvp) | `8bba87df6475cae1e595fc925551db8bea83fb68` | `TesseractRecognizer.ts`、`extractNumber.ts`、预处理工具、`OCR_VALIDATION.md`；真实 Tesseract.js 路径 |
| [ampere-force-visualizer-teacher-yanan](https://github.com/WUHAO19831214/ampere-force-visualizer-teacher-yanan) | `cb073e89d6d87129287030f1df08bd540504eb39` | 相同 recognizer/utilities；教师端 Fy/Fz 显示读取 |
<!-- section:how-it-works -->
## 工作原理
RGBA frame → normalized ROI → 预处理 → Tesseract.js/recorded recognizer → raw text 规范化 → 数字解析/验证 → `SensorEvent`。OCR/解析失败不会生成 mock measurement。
<!-- section:input -->
## 输入
含 RGBA 像素的 screen/image `FramePacket`、ROI、whitelist/预处理选项、数值名称和单位。
<!-- section:output -->
## 输出
`SensorEvent` 保留 `raw_text`、成功时的 measurement、置信度、耗时、warning/artifact，以及明确的 `OCR_RECOGNITION_FAILED`/`OCR_PARSE_FAILED`。
<!-- section:demo -->
## Demo
[![Synthetic pixel OCR](assets/overview.png)](assets/README.md) 展示真实 Tesseract.js 在 synthetic pixels 上运行，不是真实仪器显示。
<!-- section:example -->
## 最小示例
运行 [web-number-ocr](../../examples/web-number-ocr/README.md) 或 [screen-to-ocr](../../examples/web-screen-to-ocr/README.md)。
<!-- section:distribution -->
## 分发 / 下载
TypeScript package `0.3.0`；[ocr.number-0.2.0.zip](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/ocr.number-0.2.0.zip)。真实 OCR 可能在运行时获取语言数据。
<!-- section:evidence -->
## 证据等级
`E3`：真实 Tesseract.js 已在受控 synthetic pixels 上执行并覆盖失败路径。
<!-- section:maturity -->
## 成熟度
`experimental`；manifest 为 `incubating/adapter-present`。
<!-- section:limitations -->
## 已知限制
默认数字解析不支持科学计数法；字符规范化可能混淆字母/数字。置信度不是准确率；真实显示、字体、缩放、眩光和浏览器兼容性没有 E4 证据。
<!-- section:benchmark -->
## Benchmark
见 [OCR benchmark](benchmarks/README.md)；指标包括 exact match、解析成功/误差、延迟和失败率。
<!-- section:provenance -->
## 来源追溯
两个固定来源 commit 的核心 OCR/预处理文件一致；hash 与变更见 [SOURCE.md](SOURCE.md)，事实见 [sensor.json](sensor.json)。
