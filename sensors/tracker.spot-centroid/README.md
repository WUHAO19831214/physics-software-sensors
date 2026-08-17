# Spot Centroid Tracker

**English** | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

Sensor ID: `tracker.spot-centroid` · Implementation version: `0.4.0` · Maturity: `experimental` · Evidence: `E5` · Release: `v0.6.0`

<!-- section:name -->
## Name
Spot Centroid Tracker
<!-- section:description -->
## One-line description
Finds a red light spot and emits its brightness-weighted image-space centroid with quality/lost evidence.
<!-- section:physics-use -->
## Typical physics experiment use
Observes a projected/attached red spot in vibration, resonance and trajectory experiments before downstream amplitude/frequency analysis.
<!-- section:measurement -->
## What it actually measures
Red candidate pixels, weighted centroid, bbox, weight sum, saturation/ROI-edge evidence and lost state. It does **not** directly measure mechanical displacement or amplitude.
<!-- section:sources -->
## Source projects
| Repository | Commit | Source paths / use |
| --- | --- | --- |
| [spot-vibration-tracking-system-20260508-171952](https://github.com/WUHAO19831214/spot-vibration-tracking-system-20260508-171952) | `7f0d91cc73afafaecc54acc46b2b9d69375d994a` | `app.js::rgbToHsv/trackRedSpot/getAmplitudeFrom`; weighted red centroid and sweep windows |
| [forced-vibration-af-analyzer-20260502-122715](https://github.com/WUHAO19831214/forced-vibration-af-analyzer-20260502-122715) | `c3f58175a09ff29cacdfb976a5055758c4eff619` | same core threshold/weight formula; forced-vibration image range |
<!-- section:how-it-works -->
## How it works
Frame/ROI → source-compatible red-channel threshold → per-pixel brightness weights → weighted sums → centroid/bbox/quality flags or explicit lost → `SensorEvent`.
<!-- section:input -->
## Input
Camera/image `FramePacket`, normalized ROI and source-compatible red threshold/quality configuration.
<!-- section:output -->
## Output
Centroid/tracking `SensorEvent` with pixel/normalized centroid, bbox, candidate/weight evidence and flags such as `spot-lost`, `low-signal`, `overexposed`, `roi-edge`.
<!-- section:demo -->
## Demo
[![Spot centroid replay](assets/overview.png)](assets/README.md) Synthetic adapter output, not real-experiment calibration evidence.
<!-- section:example -->
## Minimal example
Run [spot-centroid](../../examples/spot-centroid/README.md) with `SpotCentroidSensor`.
<!-- section:distribution -->
## Distribution / Download
Python package `0.5.0` with `classical-trackers`; [tracker.spot-centroid-0.4.0.zip](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.spot-centroid-0.4.0.zip).
<!-- section:evidence -->
## Evidence level
`E5`: source-compatible golden replay plus a pinned downstream project integration with comparison and rollback. The Release manifest retains its historical E2-at-publication record; E5 was established by post-release reuse.

### Downstream reuse

The browser-only [Spot Vibration Tracking System](https://github.com/WUHAO19831214/spot-vibration-tracking-system-20260508-171952) uses the public `v0.6.0` wheel in an offline replay adapter behind `legacy/library/compare`. Seven same-frame cases matched within `1e-9 px`, downstream `y` range matched at `28 px / 0.56 cm`, and rollback passed. See the [integration record](../../integrations/spot-vibration/README.md). This does not claim realtime browser integration or real optical accuracy.
<!-- section:maturity -->
## Maturity
`experimental`; manifest `incubating/adapter-present`.
<!-- section:limitations -->
## Known limitations
Version 0.4.0 implements the source red-channel profile only. Exposure, weak spots and ROI edges affect results. No repeatability, uncertainty or physical calibration has E4 evidence.
<!-- section:benchmark -->
## Benchmark
See [benchmark](benchmarks/README.md): centroid pixel error, missing rate, exposure/ROI sensitivity and latency.
<!-- section:provenance -->
## Provenance
Fixed source functions/formulas and comparison results are in [SOURCE.md](SOURCE.md); facts in [sensor.json](sensor.json).
