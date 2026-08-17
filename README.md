# Physics Software Sensors

**English** | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

<!-- section:introduction -->
## What is this?

**A reusable software sensing layer for physics experiments.** It turns camera frames, screen pixels and image-processing observations into traceable `FramePacket` and `SensorEvent` records that future physics projects can reuse.

The repository also hosts reusable Companion Processing Tools that operate on Sensor outputs without pretending to create new direct observations.

This is a long-lived capability library, not a new experiment application. Source projects remain unchanged and continue to be the historical source of truth.

```text
Physics Project
      ↓
Reusable Capability
      ↓
Physics Software Sensors
      ↓
Future Physics Projects
```

Mature capabilities are extracted through adapters, tested against fixed source commits, documented, benchmarked and then reused. Pixel position, OCR text, confidence and bounding boxes are direct software observations—not automatically calibrated physical quantities.

```text
Physical / Software Source
        ↓
Capture Sensors → FramePacket
        ↓
Processor Sensors → SensorEvent / scalar measurements
        ↓
Companion Processing Tools
        ↓
Physics Application
```

For example: `screen.capture → ocr.number → vector.compose-3d → 3D resultant vector`. The final step reconstructs existing scalar measurements; it does not sense a new quantity.

<!-- section:language-access -->
## Language access

Repository multilingual content integrity: **PASS**. English, Simplified Chinese and Japanese Markdown are maintained as complete source documents. If a regional GitHub file-view route fails, this repository still provides the following quick orientation from the root README:

- **简体中文快速说明：**这是面向物理实验的可复用软件传感器基础层，当前有 7 个软件传感器和 1 个配套处理工具，共 8 项公开能力。它记录图像/屏幕/OCR/追踪的直接观测，不把像素或 OCR 数值自动说成物理量。公开 `v0.6.0` 包含 7 个 Sensor Bundle；`vector.compose-3d` 仍是未发布的 experimental 工具。完整三语静态阅读页已准备在 `docs/`，待 GitHub Pages 从 `main /docs` 启用。
- **日本語クイックガイド：**これは物理実験向けの再利用可能なソフトウェアセンサー基盤です。7 個の Software Sensor と 1 個の Companion Processing Tool、合計 8 項目の公開 capability があります。画像・画面・OCR・追跡の直接観測と、下流の物理量を区別します。公開 `v0.6.0` には 7 個の Sensor Bundle が含まれ、`vector.compose-3d` は未リリースの experimental Tool です。3 言語の静的 reader は `docs/` に準備済みで、GitHub Pages の `main /docs` 設定後に公開されます。

<!-- section:project-status -->
## Project status

**7 Software Sensors · 1 Companion Processing Tool · 8 reusable public capabilities** · English / 简体中文 / 日本語

All 7 adapters and the Tool are experimental. The public `v0.6.0` Release contains 7 Sensor Bundles; the Tool is unreleased. The first E5 downstream reuse is complete, but no Sensor is claimed as fully validated.

<!-- section:catalog -->
## Sensor catalog

| Sensor | Purpose | Language | Maturity | Evidence | Example | Download |
| --- | --- | --- | --- | --- | --- | --- |
| [`camera.capture`](sensors/camera.capture/README.md) | Camera frames with timing/backend metadata | Python | experimental | E1 | [example](examples/python-camera-capture/README.md) | [bundle](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/camera.capture-0.3.0.zip) |
| [`screen.capture`](sensors/screen.capture/README.md) | User-authorized screen/window pixels | TypeScript | experimental | E1 | [example](examples/web-screen-capture/README.md) | [bundle](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/screen.capture-0.3.0.zip) |
| [`ocr.number`](sensors/ocr.number/README.md) | Numeric OCR from an image ROI | TypeScript | experimental | E3 | [example](examples/web-number-ocr/README.md) | [bundle](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/ocr.number-0.2.0.zip) |
| [`tracker.color-marker`](sensors/tracker.color-marker/README.md) | HSV/contour color-marker tracking | Python | experimental | E2 | [example](examples/python-color-marker/README.md) | [bundle](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.color-marker-0.2.0.zip) |
| [`tracker.spot-centroid`](sensors/tracker.spot-centroid/README.md) | Brightness-weighted light-spot centroid | Python | experimental | E5 | [example](examples/spot-centroid/README.md) | [bundle](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.spot-centroid-0.4.0.zip) |
| [`tracker.template`](sensors/tracker.template/README.md) | ROI-initialized single-object tracking | Python | experimental | E3 | [example](examples/python-template-tracker/README.md) | [bundle](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.template-0.4.0.zip) |
| [`tracker.yolo`](sensors/tracker.yolo/README.md) | Multi-target detection/tracking adapter | Python | experimental | E2 | [example](examples/python-yolo-tracker/README.md) | [bundle](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.yolo-0.5.0.zip) |

See the full [Sensor Catalog](docs/sensor-catalog.md). Evidence describes exercised paths; maturity is a separate release decision.

<!-- section:companion-tools -->
### Companion Processing Tools

| Tool | Purpose | Language | Status | Example | Documentation |
| --- | --- | --- | --- | --- | --- |
| [`vector.compose-3d`](processing/vector.compose-3d/README.md) | 3D vector composition and reconstruction from scalar components | TypeScript | experimental | [web demo](examples/web-vector-compose-3d/README.md) | [Tool Page](processing/vector.compose-3d/README.md) |

See the full [Tool Catalog](docs/tool-catalog.md). Companion Tools form an extensible processing layer and are not counted as Sensors.

<!-- section:quick-start -->
## Quick start

Start with [Getting Started](docs/getting-started.md), then choose either the Python wheel or TypeScript tgz from the [`v0.6.0` Experimental Release](https://github.com/WUHAO19831214/physics-software-sensors/releases/tag/v0.6.0). Nothing is published to PyPI or the npm registry.

```bash
python -m pip install './physics_software_sensors-0.5.0-py3-none-any.whl[classical-trackers]'
npm install ./physics-software-sensors-core-0.3.0.tgz
```

<!-- section:download -->
## Download

The Release contains one Python wheel, one TypeScript tgz, seven Sensor Bundles, `release-manifest.json` and `SHA256SUMS`. A Sensor Bundle is a readable documentation/example package; it does not duplicate the shared core. Read [Downloading Sensors](docs/downloading-sensors.md) and [Installation](docs/installation.md).

<!-- section:capability-showcase -->
## Capability Showcase

[![Physics Software Sensors: 7 Software Sensors and 1 Companion Processing Tool](docs/assets/capability-showcase.png)](docs/capability-showcase.md)

Representative standalone, synthetic and replay demonstrations. Evidence level varies by capability; the YOLO tile is **recorded detector replay**, not real YOLO inference. The image is an enhancement, while the text links below remain the canonical navigation when image delivery is unavailable.

[Camera Capture](sensors/camera.capture/README.md) · [Screen Capture](sensors/screen.capture/README.md) · [Number OCR](sensors/ocr.number/README.md) · [Color Marker](sensors/tracker.color-marker/README.md) · [Spot Centroid](sensors/tracker.spot-centroid/README.md) · [Template Tracker](sensors/tracker.template/README.md) · [YOLO Tracker](sensors/tracker.yolo/README.md) · [3D Vector Composition](processing/vector.compose-3d/README.md)

Coverage: **7/7 Software Sensors + 1/1 Companion Processing Tool = 8/8 reusable public capabilities**. Open the trilingual [Capability Showcase](docs/capability-showcase.md) for all eight detailed demo images and evidence boundaries.

<!-- section:principles -->
## Core principles

1. Do not break or silently rewrite source projects.
2. Pin provenance to repository, full commit SHA, path and symbol.
3. Preserve raw observations and distinguish downstream derivations.
4. Make time, coordinates, units, confidence and uncertainty explicit.
5. State evidence, maturity, licensing and model boundaries conservatively.

<!-- section:long-term-workflow -->
## Long-term workflow

```text
New Physics Project
      ↓
Reusable mature capability
      ↓
Sensor Intake
      ↓
Physics Software Sensors
      ↓
Experimental / Validation / Release
      ↓
Future Physics Projects
```

Future work enters through [Sensor Intake](docs/sensor-intake.md), the [Add New Sensor recipe](docs/agent-recipes/add-new-sensor.md), or an existing-Sensor maintenance track. The first completed extraction-to-reuse cycle is documented in [First Complete Reuse Loop](docs/first-reuse-loop.md).

<!-- section:documentation -->
## Documentation

- [Sensor Catalog](docs/sensor-catalog.md)
- [Companion Tool Catalog](docs/tool-catalog.md)
- [Capability Showcase](docs/capability-showcase.md)
- [Getting Started](docs/getting-started.md)
- [Evidence and Maturity](docs/evidence-and-maturity.md)
- [Sensor Intake](docs/sensor-intake.md)
- [First Complete Reuse Loop](docs/first-reuse-loop.md) and [Maintenance Guide](docs/maintenance.md)
- [Current Project Status](docs/project-status.md)
- [Terminology](docs/i18n/terminology.md) and [i18n Style Guide](docs/i18n/style-guide.md)
- [Demo Asset Inventory](docs/demo-asset-inventory.md)
- [Architecture](docs/architecture.md), [data format](docs/data-format.md), [benchmarking](docs/benchmarking.md)
- [Release v0.6.0](https://github.com/WUHAO19831214/physics-software-sensors/releases/tag/v0.6.0)

<!-- section:development -->
## Development and validation

```bash
python3 tools/validate_repo.py
pytest
npm --prefix packages/typescript test
```

See [CONTRIBUTING.md](CONTRIBUTING.md). A new Sensor or major capability follows the formal intake workflow; ordinary bug fixes do not.

<!-- section:non-goals -->
## Current non-goals

- No stable, production-ready, measurement-grade or metrology claim.
- No automatic YOLO model download or bundled model weight.
- No forced migration of historical experiment projects.
- No PyPI/npm registry publication; the first merged E5 integration is an offline replay path and does not replace the downstream live-camera implementation.

<!-- section:license -->
## License

Repository-owned code and documentation are MIT licensed. Historical source code, models, data and dependencies retain their own licensing boundaries; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Latest development handoff: [.agent-handoff/latest.md](.agent-handoff/latest.md) · [.agent-handoff/latest.json](.agent-handoff/latest.json)
