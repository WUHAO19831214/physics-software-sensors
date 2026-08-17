# Template / Single-object Tracker

**English** | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

Sensor ID: `tracker.template` · Implementation version: `0.4.0` · Maturity: `experimental` · Evidence: `E3` · Release: `v0.6.0`

<!-- section:name -->
## Name
Template / Single-object Tracker
<!-- section:description -->
## One-line description
Initializes one target from an ROI and tracks its image-space bounding box with OpenCV CSRT/KCF/MIL fallback.
<!-- section:physics-use -->
## Typical physics experiment use
Follows one visible object in motion or vibration experiments when color segmentation is unsuitable.
<!-- section:measurement -->
## What it actually measures
Image-space bbox/center and tracking/lost/backend state. It is not static template matching, and pixel motion is not physical displacement without calibration.
<!-- section:sources -->
## Source projects
| Repository | Commit | Source paths / use |
| --- | --- | --- |
| [audio-visual-soundfield-tracker-stable](https://github.com/WUHAO19831214/audio-visual-soundfield-tracker-stable) | `85740d686c67452a057540edb564d713e01ccc51` | `object_template_tracker.py::initialize/update/reset/create_opencv_tracker/validate_bbox` and tests; extracted ROI tracker |
| [physics-experiment-bridge-mvp](https://github.com/WUHAO19831214/physics-experiment-bridge-mvp) | `8bba87df6475cae1e595fc925551db8bea83fb68` | `TemplateMatchingAnalyzer.ts`; related static matching profile, not extracted |
<!-- section:how-it-works -->
## How it works
Initialization frame + ROI validation → choose CSRT→KCF→MIL backend → per-frame `update` → bbox/center or lost → optional reinitialize → `SensorEvent`.
<!-- section:input -->
## Input
Camera/image `FramePacket`, initialization ROI and optional backend preference. A template asset is not required by the implemented profile.
<!-- section:output -->
## Output
Tracking `SensorEvent` with bbox, center, requested/actual backend, attempted fallbacks, initialization/reinitialization and lost state. OpenCV supplies no calibrated confidence.
<!-- section:demo -->
## Demo
[![ROI tracker replay](assets/overview.png)](assets/README.md) Real OpenCV runtime on synthetic targets, not real-experiment accuracy.
<!-- section:example -->
## Minimal example
Run [python-template-tracker](../../examples/python-template-tracker/README.md) with `TemplateTrackerSensor`.
<!-- section:distribution -->
## Distribution / Download
Python package `0.5.0` with `classical-trackers`; [tracker.template-0.4.0.zip](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.template-0.4.0.zip).
<!-- section:evidence -->
## Evidence level
`E3`: actual OpenCV contrib tracker executes on controlled synthetic/scripted sequences.
<!-- section:maturity -->
## Maturity
`experimental`; manifest `incubating/adapter-present`.
<!-- section:limitations -->
## Known limitations
Fallback changes behavior/performance. Occlusion, scale, blur and invalid ROI can cause lost state. There is no calibrated confidence, physical scale or E4 real-device evidence.
<!-- section:benchmark -->
## Benchmark
See [benchmark](benchmarks/README.md): initialization/update success, bbox/center error, lost/reinitialize, backend and latency.
<!-- section:provenance -->
## Provenance
Algorithm-family boundary, source symbols and comparisons are in [SOURCE.md](SOURCE.md); facts in [sensor.json](sensor.json).
