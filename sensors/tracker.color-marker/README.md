# Color Marker Tracker

**English** | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

Sensor ID: `tracker.color-marker` · Implementation version: `0.2.0` · Maturity: `experimental` · Evidence: `E2` · Release: `v0.6.0`

<!-- section:name -->
## Name
Color Marker Tracker
<!-- section:description -->
## One-line description
Finds a configured color marker in camera images and continuously emits its image-space position and lost state.
<!-- section:physics-use -->
## Typical physics experiment use
Tracks a colored ball/marker for motion, vibration or trajectory experiments and audio/visual alignment.
<!-- section:measurement -->
## What it actually measures
Pixel centroid, contour/area evidence and detection state. Pixel position is not displacement, velocity or amplitude until a documented calibration/time derivation is applied.
<!-- section:sources -->
## Source projects
| Repository | Commit | Source paths / use |
| --- | --- | --- |
| [audio-visual-soundfield-tracker-stable](https://github.com/WUHAO19831214/audio-visual-soundfield-tracker-stable) | `85740d686c67452a057540edb564d713e01ccc51` | `src/tennis_ball_tracker.py::TennisBallTracker.update`, mask/candidate functions and tests; extracted profile |
| [physics-experiment-bridge-mvp](https://github.com/WUHAO19831214/physics-experiment-bridge-mvp) | `8bba87df6475cae1e595fc925551db8bea83fb68` | `ColorTrackingAnalyzer.ts`, `MarkerTrackingAnalyzer.ts`; related browser profile, not extracted here |
<!-- section:how-it-works -->
## How it works
BGR frame → HSV conversion → threshold mask → morphology → contour candidates → area/circularity/continuity ranking → centroid smoothing/lost state → `SensorEvent`.
<!-- section:input -->
## Input
Camera/image `FramePacket`, HSV thresholds, area/circularity filters, smoothing and optional ROI/continuity settings.
<!-- section:output -->
## Output
Tracking `SensorEvent` with raw/smoothed pixel center, normalized position, bbox/area/quality evidence and explicit lost state.
<!-- section:demo -->
## Demo
[![Color marker replay](assets/overview.png)](assets/README.md) Standalone synthetic output, not a real experiment accuracy claim.
<!-- section:example -->
## Minimal example
Run [python-color-marker](../../examples/python-color-marker/README.md) with `ColorMarkerSensor`.
<!-- section:distribution -->
## Distribution / Download
Python package `0.5.0` with `color-marker`; [tracker.color-marker-0.2.0.zip](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.color-marker-0.2.0.zip).
<!-- section:evidence -->
## Evidence level
`E2`: fixed source commit execution/golden comparison plus deterministic success/lost/reacquire tests.
<!-- section:maturity -->
## Maturity
`experimental`; manifest `incubating/adapter-present`.
<!-- section:limitations -->
## Known limitations
HSV thresholds depend on camera and lighting. Similar colors, blur, occlusion and exposure can cause false/lost detections. Algorithm confidence is not physical uncertainty.
<!-- section:benchmark -->
## Benchmark
See [benchmark](benchmarks/README.md): success, lost-frame rate, center error, latency/FPS and source-output compatibility.
<!-- section:provenance -->
## Provenance
Extraction changes, source symbols, tolerances and golden method are in [SOURCE.md](SOURCE.md); facts in [sensor.json](sensor.json).
