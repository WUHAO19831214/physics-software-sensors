# Physics Software Sensors

**English** | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

<!-- section:introduction -->
## What is this?

**A reusable software sensing layer for physics experiments.** It turns camera frames, screen pixels and image-processing observations into traceable `FramePacket` and `SensorEvent` records that future physics projects can reuse.

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

<!-- section:catalog -->
## Sensor catalog

| Sensor | Purpose | Language | Maturity | Evidence | Example | Download |
| --- | --- | --- | --- | --- | --- | --- |
| [`camera.capture`](sensors/camera.capture/README.md) | Camera frames with timing/backend metadata | Python | experimental | E1 | [example](examples/python-camera-capture/README.md) | [bundle](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/camera.capture-0.3.0.zip) |
| [`screen.capture`](sensors/screen.capture/README.md) | User-authorized screen/window pixels | TypeScript | experimental | E1 | [example](examples/web-screen-capture/README.md) | [bundle](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/screen.capture-0.3.0.zip) |
| [`ocr.number`](sensors/ocr.number/README.md) | Numeric OCR from an image ROI | TypeScript | experimental | E3 | [example](examples/web-number-ocr/README.md) | [bundle](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/ocr.number-0.2.0.zip) |
| [`tracker.color-marker`](sensors/tracker.color-marker/README.md) | HSV/contour color-marker tracking | Python | experimental | E2 | [example](examples/python-color-marker/README.md) | [bundle](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.color-marker-0.2.0.zip) |
| [`tracker.spot-centroid`](sensors/tracker.spot-centroid/README.md) | Brightness-weighted light-spot centroid | Python | experimental | E2 | [example](examples/spot-centroid/README.md) | [bundle](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.spot-centroid-0.4.0.zip) |
| [`tracker.template`](sensors/tracker.template/README.md) | ROI-initialized single-object tracking | Python | experimental | E3 | [example](examples/python-template-tracker/README.md) | [bundle](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.template-0.4.0.zip) |
| [`tracker.yolo`](sensors/tracker.yolo/README.md) | Multi-target detection/tracking adapter | Python | experimental | E2 | [example](examples/python-yolo-tracker/README.md) | [bundle](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.yolo-0.5.0.zip) |

See the full [Sensor Catalog](docs/sensor-catalog.md). Evidence describes exercised paths; maturity is a separate release decision.

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

<!-- section:demonstrations -->
## Demonstrations

| Color Marker | Number OCR | Spot Centroid |
| --- | --- | --- |
| [![Color marker replay](sensors/tracker.color-marker/assets/overview.png)](sensors/tracker.color-marker/README.md) | [![OCR synthetic pixels](sensors/ocr.number/assets/overview.png)](sensors/ocr.number/README.md) | [![Spot centroid replay](sensors/tracker.spot-centroid/assets/overview.png)](sensors/tracker.spot-centroid/README.md) |

These are standalone synthetic/replay demonstrations, not real-device accuracy or metrology evidence. The YOLO public demo is recorded detector replay, not real model inference.

<!-- section:principles -->
## Core principles

1. Do not break or silently rewrite source projects.
2. Pin provenance to repository, full commit SHA, path and symbol.
3. Preserve raw observations and distinguish downstream derivations.
4. Make time, coordinates, units, confidence and uncertainty explicit.
5. State evidence, maturity, licensing and model boundaries conservatively.

<!-- section:documentation -->
## Documentation

- [Sensor Catalog](docs/sensor-catalog.md)
- [Getting Started](docs/getting-started.md)
- [Evidence and Maturity](docs/evidence-and-maturity.md)
- [Sensor Intake](docs/sensor-intake.md)
- [Terminology](docs/i18n/terminology.md) and [i18n Style Guide](docs/i18n/style-guide.md)
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
- No PyPI/npm registry publication and no Phase 5 downstream integration in this phase.

<!-- section:license -->
## License

Repository-owned code and documentation are MIT licensed. Historical source code, models, data and dependencies retain their own licensing boundaries; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Latest development handoff: [.agent-handoff/latest.md](.agent-handoff/latest.md) · [.agent-handoff/latest.json](.agent-handoff/latest.json)
