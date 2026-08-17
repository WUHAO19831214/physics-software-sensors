# Sensor Catalog

**English** | [简体中文](sensor-catalog.zh-CN.md) | [日本語](sensor-catalog.ja.md)

<!-- section:catalog -->
## Available Sensors

Status describes the implementation in this repository, not the historical source project's maturity.

| Sensor | Purpose | Language | Maturity | Evidence | Example | Download |
| --- | --- | --- | --- | --- | --- | --- |
| [`camera.capture`](../sensors/camera.capture/README.md) | Camera frames and capture metadata | Python | experimental | E1 | [run](../examples/python-camera-capture/README.md) | [0.3.0](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/camera.capture-0.3.0.zip) |
| [`screen.capture`](../sensors/screen.capture/README.md) | User-authorized screen/window pixels | TypeScript | experimental | E1 | [run](../examples/web-screen-capture/README.md) | [0.3.0](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/screen.capture-0.3.0.zip) |
| [`ocr.number`](../sensors/ocr.number/README.md) | Numeric OCR from an ROI | TypeScript | experimental | E3 | [run](../examples/web-number-ocr/README.md) | [0.2.0](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/ocr.number-0.2.0.zip) |
| [`tracker.color-marker`](../sensors/tracker.color-marker/README.md) | Color marker position/lost state | Python | experimental | E2 | [run](../examples/python-color-marker/README.md) | [0.2.0](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.color-marker-0.2.0.zip) |
| [`tracker.spot-centroid`](../sensors/tracker.spot-centroid/README.md) | Light-spot weighted centroid | Python | experimental | E2 | [run](../examples/spot-centroid/README.md) | [0.4.0](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.spot-centroid-0.4.0.zip) |
| [`tracker.template`](../sensors/tracker.template/README.md) | ROI-initialized single-object tracker | Python | experimental | E3 | [run](../examples/python-template-tracker/README.md) | [0.4.0](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.template-0.4.0.zip) |
| [`tracker.yolo`](../sensors/tracker.yolo/README.md) | Multi-target detector/tracker adapter | Python | experimental | E2 | [run](../examples/python-yolo-tracker/README.md) | [0.5.0](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.yolo-0.5.0.zip) |

<!-- section:status -->
## Status meaning

- `contract-only`: contract and documentation, no repository implementation.
- `experimental`: standalone adapter and offline evidence; real-device/downstream validation may be missing.
- `validated`: applicable real runtime/device, metrics and licensing gates have passed.
- `stable`: validated public API plus downstream pinned reuse and rollback evidence.

Evidence is not maturity. See [Evidence and Maturity](evidence-and-maturity.md). All seven Sensors remain experimental; no Sensor has E4 or E5 evidence. Real YOLO inference remains not measured and no model weight is distributed.
