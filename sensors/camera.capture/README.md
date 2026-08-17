# Camera Capture Sensor

**English** | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

Sensor ID: `camera.capture` · Implementation version: `0.3.0` · Maturity: `experimental` · Evidence: `E1` · Release: `v0.6.0`

<!-- section:name -->
## Name
Camera Capture Sensor

<!-- section:description -->
## One-line description
Produces camera/image-sequence frames with explicit timestamps, backend metadata and capture quality information.

<!-- section:physics-use -->
## Typical physics experiment use
Supplies visual input for motion, vibration, trajectory, light-spot and synchronized audio/visual experiments without embedding their UI or physics business logic.

<!-- section:measurement -->
## What it actually measures
It directly observes image pixels and capture timing/status. Position, displacement, velocity or amplitude are downstream results requiring another Sensor and, for physical units, calibration.

<!-- section:sources -->
## Source projects
| Repository | Commit | Source paths / use |
| --- | --- | --- |
| [audio-visual-soundfield-tracker-stable](https://github.com/WUHAO19831214/audio-visual-soundfield-tracker-stable) | `85740d686c67452a057540edb564d713e01ccc51` | `src/browser_capture.py`, `camera_devices.py`, `local_capture.py`, `camera_processor.py`; OpenCV/WebRTC frames |
| [spot-vibration-tracking-system-20260508-171952](https://github.com/WUHAO19831214/spot-vibration-tracking-system-20260508-171952) | `7f0d91cc73afafaecc54acc46b2b9d69375d994a` | `app.js`; camera-to-canvas spot processing |
| [forced-vibration-af-analyzer-20260502-122715](https://github.com/WUHAO19831214/forced-vibration-af-analyzer-20260502-122715) | `c3f58175a09ff29cacdfb976a5055758c4eff619` | `app.js`; camera selection and vibration input |
| [physics-experiment-bridge-mvp](https://github.com/WUHAO19831214/physics-experiment-bridge-mvp) | `8bba87df6475cae1e595fc925551db8bea83fb68` | `src/camera/CameraCapturePanel.tsx`, `cameraUtils.ts` |
| [ampere-force-visualizer-teacher-yanan](https://github.com/WUHAO19831214/ampere-force-visualizer-teacher-yanan) | `cb073e89d6d87129287030f1df08bd540504eb39` | same camera boundary in the teacher application |

<!-- section:how-it-works -->
## How it works
Backend → frame read → wall/monotonic timestamp → pixel/media metadata → requested vs measured rate/status → `FramePacket`. Current Python backends are OpenCV and deterministic image-sequence replay.

<!-- section:input -->
## Input
Camera device/backend configuration, requested width/height/FPS and optional image sequence. Browser camera remains a cross-language contract rather than this Python implementation.

<!-- section:output -->
## Output
A camera `FramePacket` with frame/run/sequence IDs, dimensions, color/media type, observed/monotonic time, backend status and quality flags.

<!-- section:demo -->
## Demo
[![Synthetic replay frame](assets/captured-frame.png)](assets/README.md) Synthetic replay proves the adapter path, not real-camera compatibility or timing accuracy.

<!-- section:example -->
## Minimal example
Run [python-camera-capture](../../examples/python-camera-capture/README.md) with `CameraSource` and `ImageSequenceCameraBackend`.

<!-- section:distribution -->
## Distribution / Download
Python package `0.5.0`; [camera.capture-0.3.0.zip](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/camera.capture-0.3.0.zip). The bundle does not copy package core.

<!-- section:evidence -->
## Evidence level
`E1`: deterministic synthetic image-sequence replay only.

<!-- section:maturity -->
## Maturity
`experimental`; the manifest remains `incubating/adapter-present`. Page completeness does not promote it.

<!-- section:limitations -->
## Known limitations
Requested FPS/resolution may differ from backend nominal/measured values. Real cameras, drivers, dropped-frame behavior and timing accuracy have no E4 evidence.

<!-- section:benchmark -->
## Benchmark
See [capture replay benchmark](benchmarks/README.md) and the repository [benchmark summary](../../docs/benchmark-summary.md).

<!-- section:provenance -->
## Provenance
File/symbol-level extraction and validation are recorded in [SOURCE.md](SOURCE.md); machine facts are in [sensor.json](sensor.json).
