# Capability Showcase

**English** | [简体中文](capability-showcase.zh-CN.md) | [日本語](capability-showcase.ja.md)

<!-- section:overview -->
## Overview

The repository homepage loads one aggregate preview to reduce independent GitHub Raw/CDN requests. This detail page keeps the eight reviewed demonstrations available when a reader intentionally opens the gallery.

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

<!-- section:evidence -->
## Evidence boundary

These are representative standalone, synthetic, recorded or replay demonstrations. Evidence level varies by capability; none of the images alone establishes real-device accuracy, calibration, repeatability or metrology performance. Canonical assets remain version-controlled in this repository.
