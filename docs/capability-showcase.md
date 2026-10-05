# Capability Showcase

**English** | [简体中文](capability-showcase.zh-CN.md) | [日本語](capability-showcase.ja.md)

<!-- section:overview -->
## Overview

The current gallery covers 9 Sensors and 4 processing Tools. The original eight demonstrations share one aggregate preview; FringeLab adds a second verified runtime screenshot and a component table below.

[![Physics Software Sensors capability showcase](assets/capability-showcase.png)](../README.md)

The aggregate is reproducibly built from the eight images below with `python3 tools/build_capability_showcase.py`. It uses no network access or external image host.

<!-- section:software-sensors -->
## Software Sensors

### Camera Capture

[![Synthetic recorded camera frame](../sensors/camera.capture/assets/captured-frame.png)](../sensors/camera.capture/README.md)

Turns a recorded or live camera image into a timed `FramePacket`. The image is a deterministic synthetic camera replay, not a hardware-camera claim.

### Screen Capture

[![Synthetic shared-window pixels](../sensors/screen.capture/assets/captured-screen-frame.png)](../sensors/screen.capture/README.md)

Represents pixels from a user-authorized screen or window as a `FramePacket`. The image uses synthetic shared-window pixels.

### Number OCR

[![Numeric OCR replay](../sensors/ocr.number/assets/overview.png)](../sensors/ocr.number/README.md)

Recognizes text in a screen-image ROI and parses a numeric observation. It does not read a device SDK value.

### Color Marker Tracker

[![Color marker replay](../sensors/tracker.color-marker/assets/overview.png)](../sensors/tracker.color-marker/README.md)

Finds an HSV color marker and reports its image-space center. Pixel position is not calibrated physical displacement.

### Spot Centroid

[![Spot centroid replay](../sensors/tracker.spot-centroid/assets/overview.png)](../sensors/tracker.spot-centroid/README.md)

Reports the brightness-weighted centroid of a light spot inside the image ROI. It does not directly measure mechanical displacement.

### Template / Single-object Tracker

[![Single-object tracker replay](../sensors/tracker.template/assets/overview.png)](../sensors/tracker.template/README.md)

Tracks an ROI-initialized object with an OpenCV single-object backend and reports bbox/lost state; this is not static template matching.

### YOLO Tracker

[![Recorded detector replay](../sensors/tracker.yolo/assets/overview.png)](../sensors/tracker.yolo/README.md)

Demonstrates detections and track IDs through a **recorded detector replay**. This public image is not evidence of real YOLO model inference.

<!-- section:companion-tools -->
## Companion Processing Tools

### 3D Vector Composition

[![Recorded OCR components composed into a 3D resultant vector](../processing/vector.compose-3d/assets/overview.png)](../processing/vector.compose-3d/README.md)

Composes traceable scalar x/y/z components into a resultant vector and renderer-neutral model. It derives from existing observations and is not a new direct Sensor observation. See the [standalone web example](../examples/web-vector-compose-3d/README.md).

### FringeLab image and optics toolkit

Reusable components extracted from the light-distribution experiment, available together or independently in `@physics-software-sensors/fringelab` 0.1.0. Both batches are collected.

**Batch 1:** calculator, ROI, virtual ruler, manual calibration and profile analysis.

**Batch 2:** automatic ruler, ruler-number OCR, browser camera and optical inversion.

| Component | Reusable behavior | Entry point |
| --- | --- | --- |
| Floating calculator | Movable panel, independent instances, arithmetic and scientific notation | [`UI`](../packages/fringelab/README.md) |
| ROI and virtual ruler | Rotate/move/resize a native-pixel ROI; ruler endpoints, ticks and snapping | [`UI`](../packages/fringelab/README.md) |
| Manual calibration | Confirm a known interval or editable multi-point readings | [`calibration.scale-1d`](../processing/calibration.scale-1d/README.md) |
| Profile and signal analysis | Relative image response, channel quality, smoothing, peaks and widths | [`image.strip-profile`](../sensors/image.strip-profile/README.md) |
| Automatic ruler | Locate physical ticks; retain manual/region modes, contrast and snapping options | [`vision.ruler-ticks`](../sensors/vision.ruler-ticks/README.md) |
| Ruler OCR and camera | Draft centimetre readings; capture/freeze camera frames and inspect settings | [`browser`](../packages/fringelab/README.md) |
| Optical inversion | Interference/diffraction wavelength, regression, uncertainty and simulation | [`optics.fringe-wavelength`](../processing/optics.fringe-wavelength/README.md) |

[![FringeLab image and optics toolkit — synthetic example](assets/fringelab-toolkit.png)](fringelab-toolkit.md)

[Chinese guide](fringelab-toolkit.zh-CN.md) · [API and install](../packages/fringelab/README.md) · [runnable example](../examples/web-fringelab-toolkit/README.md) · [profile features](../processing/signal.profile-features/README.md) · [FringeLab guide](fringelab-toolkit.md)

Automatic/OCR readings remain drafts until confirmed; manual and multi-point modes are fully retained. The screenshot is a working synthetic 650 nm example. DN is relative response, and real-device precision is not established.

Current catalog: **9/9 Sensors + 4/4 processing Tools = 13/13 capabilities**. Calculator and overlay UI are additional reusable components, outside Sensor counts.

### Experimental thermal model and Core support

[GasLab 0.1.0](../packages/gaslab/README.md) adds a headless gas teaching model; unreleased Core 0.3.1 adds quantity candidates, fitting/extrapolation, reading stabilization and opt-in OCR preprocessing. [Review and evidence](gaslab-intake.md) · [runnable headless replay](../examples/headless-gaslab/README.md). Model/support packages are separate from the **13 Sensor/Companion Tool capabilities** above. No new observation, npm publication or v0.6.0 download is implied.

<!-- section:evidence -->
## Evidence boundary

These are representative standalone, synthetic, recorded or replay demonstrations. Evidence level varies by capability; none of the images alone establishes real-device accuracy, calibration, repeatability or metrology performance. Canonical assets remain version-controlled in this repository.
