# Companion Tool Catalog

**English** | [简体中文](tool-catalog.zh-CN.md) | [日本語](tool-catalog.ja.md)

<!-- section:catalog -->
## Catalog

Companion Tools process existing observations or measurements; they do not create a new direct observation and are not counted as Sensors.

| Tool | Purpose | Language | Status | Source | Example | Docs |
| --- | --- | --- | --- | --- | --- | --- |
| [`vector.compose-3d`](../processing/vector.compose-3d/README.md) | Compose traceable x/y/z scalar components into a 3D vector and optional render model | TypeScript | `experimental` `0.1.0` | Yan'an Ampere-force teacher application | [Web demo](../examples/web-vector-compose-3d/README.md) | [Source record](../processing/vector.compose-3d/SOURCE.md) |
| [`calibration.scale-1d`](../processing/calibration.scale-1d/README.md) | Confirmed two-point and piecewise multi-point 1D calibration | TypeScript | experimental 0.1.0 | FringeLab | [Web demo](../examples/web-fringelab-toolkit/README.md) | [Source](../processing/calibration.scale-1d/SOURCE.md) |
| [`signal.profile-features`](../processing/signal.profile-features/README.md) | Smoothing, background subtraction, peaks, widths and period | TypeScript | experimental 0.1.0 | FringeLab | [Web demo](../examples/web-fringelab-toolkit/README.md) | [Source](../processing/signal.profile-features/SOURCE.md) |
| [`optics.fringe-wavelength`](../processing/optics.fringe-wavelength/README.md) | Slit/diffraction wavelength inversion, regression and uncertainty | TypeScript | experimental 0.1.0 | FringeLab | [Web demo](../examples/web-fringelab-toolkit/README.md) | [Source](../processing/optics.fringe-wavelength/SOURCE.md) |

<!-- section:status -->
## Status boundary

Repository inventory: **9 Sensors · 4 Companion Tools**. The tool is unreleased development after immutable `v0.6.0`; it is not present in that Release and does not change Sensor maturity or evidence.
