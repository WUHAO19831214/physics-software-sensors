# Getting Started

**English** | [简体中文](getting-started.zh-CN.md) | [日本語](getting-started.ja.md)

<!-- section:choose -->
## 1. Choose the direct observation

Choose camera/screen capture for pixels, OCR for displayed text, or a tracker for an image-space position/bounding box. If you need displacement, force, frequency or angle, document the downstream calibration/derivation separately.

<!-- section:download -->
## 2. Download and verify

Use the [`v0.6.0` Experimental Release](https://github.com/WUHAO19831214/physics-software-sensors/releases/tag/v0.6.0), verify `SHA256SUMS`, then follow [Installation](installation.md). No registry package is published.

<!-- section:run -->
## 3. Run a standalone example

Open the selected [Sensor Page](sensor-catalog.md), install only its declared dependencies and run the linked small example. Recorded/synthetic examples prove separation from the source application, not real-device accuracy.

### After sensing: process measurements

When an experiment needs a derived representation, continue into the separate [Companion Tool Catalog](tool-catalog.md). For example, `screen.capture → ocr.number → vector.compose-3d` turns displayed scalar components into a traceable 3D resultant. The Tool does not create a new observation, and the current unreleased Tool source is not part of `v0.6.0`.

<!-- section:interpret -->
## 4. Interpret conservatively

Read Evidence, Maturity, Known Limitations, Benchmark and Provenance before integration. Retain the old source-project path and a rollback mechanism until downstream comparison succeeds.
