# Demo Asset Inventory

Scan scope: `sensors/*/assets/`, `processing/*/assets/`, and `examples/`; extensions `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`. Scan date: 2026-08-17. A **Yes** showcase source is included in the generated aggregate and displayed individually on the trilingual Capability Showcase pages. Generated `examples/*/output/` files are local ignored output and are recorded here for completeness, not committed as public assets.

| Capability | Asset | Kind | Evidence | Showcase source |
| --- | --- | --- | --- | --- |
| `camera.capture` | `sensors/camera.capture/assets/captured-frame.png` | Public overview | Actual deterministic CameraSource replay on synthetic input | **Yes** |
| `camera.capture` | `sensors/camera.capture/assets/frame-packet-metadata.png` | Public detail | Serialized replay metadata | No |
| `camera.capture` | `sensors/camera.capture/assets/backend-information.png` | Public detail | Requested/nominal/measured replay metadata | No |
| `camera.capture` | `examples/python-camera-capture/output/captured-frame.png` | Ignored generated output | Local standalone replay output | No |
| `camera.capture` | `examples/python-camera-capture/output/frame-packet-metadata.png` | Ignored generated output | Local standalone replay output | No |
| `camera.capture` | `examples/python-camera-capture/output/backend-information.png` | Ignored generated output | Local standalone replay output | No |
| `screen.capture` | `sensors/screen.capture/assets/captured-screen-frame.png` | Public overview | Actual RecordedScreenBackend replay on synthetic shared-window pixels | **Yes** |
| `screen.capture` | `sensors/screen.capture/assets/frame-packet-metadata.png` | Public detail | Serialized FramePacket replay | No |
| `screen.capture` | `sensors/screen.capture/assets/permission-boundary.png` | Public detail | Browser permission/lifecycle boundary | No |
| `screen.capture` | `examples/web-screen-capture/sample/recorded-screen.png` | Fixture | Synthetic recorded-screen input | No |
| `screen.capture` | `examples/web-screen-capture/output/frame-packet-metadata.png` | Ignored generated output | Local standalone replay output | No |
| `screen.capture` | `examples/web-screen-capture/output/permission-boundary.png` | Ignored generated output | Local standalone replay output | No |
| `ocr.number` | `sensors/ocr.number/assets/overview.png` | Public overview | Actual Tesseract.js path on synthetic screen pixels | **Yes** |
| `ocr.number` | `sensors/ocr.number/assets/processing.png` | Public detail | ROI/preprocess/Tesseract.js/value pipeline | No |
| `ocr.number` | `examples/web-number-ocr/sample/alphabetic.png` | Fixture | Synthetic OCR failure input | No |
| `ocr.number` | `examples/web-number-ocr/sample/blank.png` | Fixture | Synthetic blank input | No |
| `ocr.number` | `examples/web-number-ocr/sample/engine-failure.png` | Fixture | Synthetic encoder/engine failure input | No |
| `ocr.number` | `examples/web-number-ocr/sample/negative.png` | Fixture | Synthetic negative number input | No |
| `ocr.number` | `examples/web-number-ocr/sample/positive.png` | Fixture | Synthetic positive number input | No |
| `ocr.number` | `examples/web-number-ocr/sample/zero.png` | Fixture | Synthetic zero input | No |
| `ocr.number` | `examples/web-number-ocr/output/alphabetic-roi.png` | Ignored generated output | Local ROI output | No |
| `ocr.number` | `examples/web-number-ocr/output/alphabetic-preprocessed.png` | Ignored generated output | Local preprocess output | No |
| `ocr.number` | `examples/web-number-ocr/output/blank-roi.png` | Ignored generated output | Local ROI output | No |
| `ocr.number` | `examples/web-number-ocr/output/blank-preprocessed.png` | Ignored generated output | Local preprocess output | No |
| `ocr.number` | `examples/web-number-ocr/output/negative-roi.png` | Ignored generated output | Local ROI output | No |
| `ocr.number` | `examples/web-number-ocr/output/negative-preprocessed.png` | Ignored generated output | Local preprocess output | No |
| `ocr.number` | `examples/web-number-ocr/output/positive-roi.png` | Ignored generated output | Local ROI output | No |
| `ocr.number` | `examples/web-number-ocr/output/positive-preprocessed.png` | Ignored generated output | Local preprocess output | No |
| `ocr.number` | `examples/web-number-ocr/output/zero-roi.png` | Ignored generated output | Local ROI output | No |
| `ocr.number` | `examples/web-number-ocr/output/zero-preprocessed.png` | Ignored generated output | Local preprocess output | No |
| `tracker.color-marker` | `sensors/tracker.color-marker/assets/overview.png` | Public overview | Actual ColorMarkerSensor run on synthetic input | **Yes** |
| `tracker.color-marker` | `sensors/tracker.color-marker/assets/processing.png` | Public detail | Input/mask/detection pipeline | No |
| `tracker.color-marker` | `sensors/tracker.color-marker/assets/lost-reacquire.png` | Public detail | Synthetic tracking/lost/reacquire lifecycle | No |
| `tracker.color-marker` | `examples/python-color-marker/sample/representative-input.png` | Fixture | Synthetic marker input | No |
| `tracker.color-marker` | `examples/python-color-marker/output/overview.png` | Ignored generated output | Local standalone output | No |
| `tracker.color-marker` | `examples/python-color-marker/output/processing.png` | Ignored generated output | Local standalone output | No |
| `tracker.color-marker` | `examples/python-color-marker/output/lost-reacquire.png` | Ignored generated output | Local standalone output | No |
| `tracker.spot-centroid` | `sensors/tracker.spot-centroid/assets/overview.png` | Public overview | Actual CameraSource → SpotCentroidSensor synthetic replay | **Yes** |
| `tracker.spot-centroid` | `sensors/tracker.spot-centroid/assets/processing.png` | Public detail | Input/mask/centroid pipeline | No |
| `tracker.spot-centroid` | `sensors/tracker.spot-centroid/assets/movement.png` | Public detail | Synthetic motion replay | No |
| `tracker.spot-centroid` | `examples/spot-centroid/sample/blank.png` | Fixture | Synthetic missing-spot input | No |
| `tracker.spot-centroid` | `examples/spot-centroid/sample/bright.png` | Fixture | Synthetic bright-spot input | No |
| `tracker.spot-centroid` | `examples/spot-centroid/sample/dim.png` | Fixture | Synthetic dim-spot input | No |
| `tracker.spot-centroid` | `examples/spot-centroid/sample/horizontal.png` | Fixture | Synthetic horizontal motion | No |
| `tracker.spot-centroid` | `examples/spot-centroid/sample/roi-edge.png` | Fixture | Synthetic ROI-edge case | No |
| `tracker.spot-centroid` | `examples/spot-centroid/sample/vertical.png` | Fixture | Synthetic vertical motion | No |
| `tracker.template` | `sensors/tracker.template/assets/overview.png` | Public overview | Actual OpenCV CSRT synthetic replay | **Yes** |
| `tracker.template` | `sensors/tracker.template/assets/initialization.png` | Public detail | Synthetic initialization ROI | No |
| `tracker.template` | `sensors/tracker.template/assets/tracking.png` | Public detail | Actual CSRT bbox update | No |
| `tracker.template` | `sensors/tracker.template/assets/lost.png` | Public detail | Explicit lost state on blank replay | No |
| `tracker.yolo` | `sensors/tracker.yolo/assets/overview.png` | Public overview | **Recorded detector replay**, not real YOLO inference | **Yes** |
| `tracker.yolo` | `sensors/tracker.yolo/assets/multi-target.png` | Public detail | Recorded multi-target fixture replay | No |
| `tracker.yolo` | `sensors/tracker.yolo/assets/tracking.png` | Public detail | Recorded ID lifecycle replay | No |
| `tracker.yolo` | `sensors/tracker.yolo/assets/fallback.png` | Public detail | Recorded requested/actual backend boundary | No |
| `vector.compose-3d` | `processing/vector.compose-3d/assets/overview.png` | Public overview | Actual standalone browser runtime in recorded Fy/Fz OCR mode | **Yes** |

## Homepage result

- Reused existing reviewed Sensor assets: **7**.
- Newly generated Tool runtime asset: **1** (`vector.compose-3d/assets/overview.png`).
- Aggregate homepage asset: **1** (`docs/assets/capability-showcase.png`), generated offline from the 8 reviewed sources by `tools/build_capability_showcase.py`.
- Root README image requests: **1** instead of 8; detailed trilingual pages retain all 8 individual images.
- Public capability visual and text-link coverage: **8/8**.
- Third-party/source-project images copied: **0**.
- Homepage YOLO evidence: recorded detector replay only.

Per-asset generation commands, hashes and scientific boundaries remain in each capability's `assets/README.md`.
