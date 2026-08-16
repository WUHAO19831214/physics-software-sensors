# 来源与抽取记录：tracker.spot-centroid

## 固定来源

| Repository | Commit | Path | Symbol / responsibility | Actual use |
| --- | --- | --- | --- | --- |
| `WUHAO19831214/spot-vibration-tracking-system-20260508-171952` | `7f0d91cc73afafaecc54acc46b2b9d69375d994a` | `app.js` | `rgbToHsv`；`trackRedSpot`；`getAmplitudeFrom` | 从 browser canvas 像素识别红色光斑，以重心序列形成轨迹；后续窗口函数计算图像范围 |
| `WUHAO19831214/spot-vibration-tracking-system-20260508-171952` | 同上 | `docs/DATA_DICTIONARY.md`、`docs/VALIDATION_PROTOCOL.md` | 数据字段和验证边界 | 区分像素观测、校准与拟议验证 |
| `WUHAO19831214/forced-vibration-af-analyzer-20260502-122715` | `c3f58175a09ff29cacdfb976a5055758c4eff619` | `app.js` | `rgbToHsv`；`trackRedSpot`；`getAmplitudeFrom` | 相同红色重心核心；下游关联扫频窗口和设定频率 |
| `WUHAO19831214/forced-vibration-af-analyzer-20260502-122715` | 同上 | `docs/SIGNAL_PROCESSING.md`、`docs/VALIDATION_REPORT.md` | 信号处理和验证说明 | 提供 derived quantity 的边界上下文 |

核对结果：两个固定 `app.js` 中的 `rgbToHsv` 和 `trackRedSpot` 核心实现一致；本轮只抽取重心算法，不抽取 UI、canvas lifecycle、扫频状态、`getAmplitudeFrom` 或物理分析。

## 来源行为基线

`trackRedSpot` 的固定行为：

- `width > 1000` 时 `step=2`，否则 `step=1`；
- 红 hue：`h <= 18 || h >= 340`；
- `s > 0.38 && v > 0.35`；
- 强红：`r > 135 && r-g > 35 && r-b > 20`；
- 权重：`(s*v*255 + max(0, r-max(g,b))) / 2`；
- `weightSum > 900` 才 locked；
- 重心是候选像素坐标的 weight average；
- radius 为 `max(7, hypot(maxX-minX,maxY-minY)/2)`。

## 本仓库实现映射

| New file / symbol | Extraction method | Algorithm change |
| --- | --- | --- |
| `packages/python/src/physics_sensors/tracking/spot_centroid.py::SpotCentroidTracker` | 将浏览器 pixel loop 抽离为 NumPy BGR processor；默认配置保留上述来源判定和公式 | 核心阈值、权重、step、strict `>900` 与 radius 未改；增加可配置 normalized ROI 和计算型诊断字段 |
| 同文件 `SpotCentroidConfig` | 把来源常量变为显式配置 | 0.4.0 仍只允许 red；增加 minimum candidate、过曝 warning 参数，不改变默认 locked 真值 |
| 同文件 `SpotCentroidSensor` | FramePacket adapter | 新增统一 lifecycle、SensorEvent、image-pixel coordinate frame、lost/quality flags；不加入 displacement/amplitude/frequency |

新增 `spot_area`、bbox、candidate count、peak、overexposed fraction 与 ROI-edge 都由本帧候选像素直接计算。它们不是来源 confidence，也不改变 `source_projection`。`quality.confidence` 因无来源证据而保持 `null`。

## 来源对照与容差

1. `examples/spot-centroid/generate_fixtures.py` 生成六张 synthetic PNG：亮斑、水平移动、垂直移动、变暗、空白、ROI 边缘。
2. `tools/source_spot_centroid_harness.mjs` 用逐句对应固定 `app.js` 的 JavaScript 函数读取这些 PNG，生成 `tests/fixtures/spot_centroid/golden.json`；golden 不是手写预期。
3. `tests/test_spot_centroid.py` 对同一像素运行新 Python tracker，比对 locked、x、y、radius、weight sum。
4. 定义容差为 `1e-9`；六帧 detection/lost 6/6 一致，最大 centroid error 为 0.0 px。

完整性能环境和结果见 [Phase 3B benchmark](../../benchmarks/results/phase3b-classical-trackers-2026-08-16.md)。

## 演示资产

`assets/overview.png`、`processing.png`、`movement.png` 和 `events.json` 由 `examples/spot-centroid/run.py` 在本仓库 synthetic recorded frames 上实际运行 `CameraSource → SpotCentroidSensor` 生成。它们不是来源仓库资产；详细 SHA-256 见 [assets/README.md](assets/README.md)。

## 许可证边界

两个来源固定 commit 没有 `LICENSE*`，GitHub metadata 为 `NOASSERTION`，所以仍标为 `license_review: pending`。本轮没有复制来源图片或整文件；实现为边界化的 source-compatible extraction，并保留精确 provenance。在进入 stable、发布包或接入下游前，仍须由维护者确认来源代码许可。
