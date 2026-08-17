# YOLO Detection and Tracking Sensor

**English** | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

Sensor ID: `tracker.yolo` · Implementation version: `0.5.0` · Maturity: `experimental` · Evidence: `E2` · Release: `v0.6.0`

<!-- section:name -->
## Name
YOLO Detection and Tracking Sensor
<!-- section:description -->
## One-line description
Converts multi-target detector/tracker backend results into traceable detections, bounding boxes and Track IDs.
<!-- section:physics-use -->
## Typical physics experiment use
Observes multiple visible objects/people for image-space trajectories when a reviewed local model and runtime are appropriate.
<!-- section:measurement -->
## What it actually measures
Class labels, detector confidence, bbox/center and backend Track ID. Confidence is not accuracy, tracking confidence or physical uncertainty; pixels need calibration for physical quantities.
<!-- section:sources -->
## Source projects
| Repository | Commit | Source paths / use |
| --- | --- | --- |
| [audio-visual-soundfield-tracker-stable](https://github.com/WUHAO19831214/audio-visual-soundfield-tracker-stable) | `85740d686c67452a057540edb564d713e01ccc51` | `src/detector.py::Detector.detect/track/_detect_hog`, `camera_processor.py`, config/setup/model docs/tests; YOLO/ByteTrack and HOG fallback boundary |
<!-- section:how-it-works -->
## How it works
Frame → selected backend → model artifact verification where applicable → detection → optional ByteTrack/recorded Track IDs → normalized adapter result/fallback evidence → `SensorEvent`.
<!-- section:input -->
## Input
Camera/image `FramePacket`, backend configuration, class filters and (for real YOLO) an explicit reviewed local `ModelArtifact` path/SHA-256/license status.
<!-- section:output -->
## Output
Detection/tracking `SensorEvent` with all detections: class ID/name, bbox/center, detector confidence, optional Track ID and requested/actual/attempted backend metadata.
<!-- section:demo -->
## Demo
[![Recorded detector replay](assets/overview.png)](assets/README.md) This is recorded source-compatible output—not real YOLO inference or model accuracy evidence.
<!-- section:example -->
## Minimal example
Run [python-yolo-tracker](../../examples/python-yolo-tracker/README.md) with `RecordedDetectorBackend`; it downloads no model.
<!-- section:distribution -->
## Distribution / Download
Python package `0.5.0`; offline `yolo-recorded`; [tracker.yolo-0.5.0.zip](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.yolo-0.5.0.zip). Real `yolo-runtime` is separate.
<!-- section:evidence -->
## Evidence level
`E2`: fixed source recorded output and adapter/fallback/lifecycle tests. Real Ultralytics/ByteTrack inference was not executed.
<!-- section:maturity -->
## Maturity
`experimental`; manifest `incubating/adapter-present`.
<!-- section:limitations -->
## Known limitations
No `.pt`/`.onnx`/`.engine` is bundled or auto-downloaded. HOG is person-only and not YOLO-equivalent. Model accuracy, real ByteTrack behavior and lab/device performance are not measured.
<!-- section:benchmark -->
## Benchmark
See [benchmark](benchmarks/README.md): adapter/source compatibility, multi-target/lost/fallback semantics and latency; model accuracy remains not measured.
<!-- section:provenance -->
## Provenance
Source symbols, model/license boundary and replay construction are in [SOURCE.md](SOURCE.md) and [YOLO review](../../docs/yolo-model-and-license-review.md); facts in [sensor.json](sensor.json).
