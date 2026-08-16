# YOLO Model and License Review

Review date: 2026-08-16. Scope: `tracker.yolo` Phase 3C experimental adapter. This is a technical inventory, not legal advice.

## Decision

The library ships **no YOLO weights** and performs **no automatic model download**. A real YOLO backend starts only from an explicit local `ModelArtifact` whose SHA-256 matches the file. Phase 3C real inference was not executed because no maintainer-approved local artifact was supplied and the development environment did not contain the Ultralytics runtime. Recorded replay and the source-compatible OpenCV HOG fallback remain fully offline.

| Item | Result |
| --- | --- |
| Python package | `physics-software-sensors` / import `physics_sensors`, implementation `0.5.0`; repository code is MIT |
| Runtime version | Source declares `ultralytics>=8.2,<9`; Phase 3C environment: **not installed**, exact runtime therefore **not measured** |
| Model family | Source expects YOLOv8 through `ultralytics.YOLO`; adapter does not hard-code a weight artifact |
| Weight filename | Source searches `models/yolov8n.pt` then repository-root `yolov8n.pt`; neither file is tracked at the fixed source commit |
| Weight source | Source `setup_yolo.sh` can ask Ultralytics to resolve `yolov8n.pt`; this setup path was audited but **not run** |
| Weight committed? | No `.pt`, `.onnx`, or `.engine` in the fixed source checkout or this repository; all remain excluded |
| Runtime license | Ultralytics package metadata declares AGPL-3.0; Ultralytics also advertises an Enterprise option. A downstream adopter must review which terms apply to its distribution/use |
| Weight license | **Pending artifact-specific review.** The filename and download host alone are insufficient evidence for redistribution terms |
| Redistribution | Runtime dependency is optional. Weight redistribution is **not approved** by this project until the exact artifact and applicable terms are reviewed |
| ByteTrack source | Ultralytics `bytetrack.yaml` selected by name; its repository file is under Ultralytics licensing. The original FoundationVision ByteTrack repository publishes an MIT license; these facts do not automatically relicense Ultralytics integration code |
| HOG fallback | OpenCV 4.x HOG default people detector; OpenCV 4.x repository license is Apache-2.0. It is person-only and is not capability-equivalent to YOLO |

## Source evidence

Fixed application source: [`WUHAO19831214/audio-visual-soundfield-tracker-stable@85740d6`](https://github.com/WUHAO19831214/audio-visual-soundfield-tracker-stable/tree/85740d686c67452a057540edb564d713e01ccc51).

- `src/detector.py` loads only the two local paths above. If neither exists, or loading/inference fails, it uses OpenCV HOG.
- `src/detector.py::track` calls Ultralytics with `persist=True`, tracker `bytetrack.yaml`, configured confidence and the source person-only class filter.
- `src/camera_processor.py::CentroidTracker` associates detections when native IDs are unavailable; defaults are `max_missed=12` and `max_distance_ratio=0.18`.
- `requirements.txt` declares `ultralytics>=8.2,<9` and `lap>=0.5.12,<1`.
- `scripts/setup_yolo.sh` is an explicit setup operation capable of triggering Ultralytics model resolution; neither library import nor Phase 3C tests call it.

## Third-party references checked

- [Ultralytics Python package metadata](https://github.com/ultralytics/ultralytics/blob/main/pyproject.toml) — runtime license declaration.
- [Ultralytics YOLOv8 documentation](https://docs.ultralytics.com/models/yolov8/) — model family and published licensing routes.
- [Ultralytics ByteTrack configuration](https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/trackers/bytetrack.yaml) — default tracker configuration distributed with the runtime.
- [Ultralytics tracking documentation](https://docs.ultralytics.com/modes/track/) — `persist=True` and model/tracker usage semantics.
- [FoundationVision ByteTrack license](https://github.com/FoundationVision/ByteTrack/blob/main/LICENSE) — original repository MIT text.
- [OpenCV 4.x license](https://github.com/opencv/opencv/blob/4.x/LICENSE) — fallback runtime licensing.

Links document the state reviewed on the review date. Releases and commercial terms can change; repeat this review before publishing a runtime bundle or approving a model artifact.

## `ModelArtifact` boundary

Required fields are `model_id`, `model_family`, `uri`, `sha256`, `runtime`, `runtime_version`, `class_names`, and `license_state`. The backend rejects `http://` and `https://` URIs and verifies the local SHA before constructing the runtime model. This describes an artifact; it does not certify that the artifact is licensed.

An adopter must provide an exact local file and make its own artifact-specific license decision:

```python
artifact = ModelArtifact(
    model_id="maintainer-approved-id",
    model_family="YOLOv8",
    uri="/absolute/path/to/model.pt",
    sha256="<64 lowercase hexadecimal characters>",
    runtime="ultralytics",
    runtime_version="<installed exact version>",
    class_names=("person",),
    license_state="<reviewed state>",
)
```

## Release gate

Before any weight or preconfigured real-inference bundle is published, record the exact weight URL/release, SHA-256, model card, terms, runtime version, distribution mode, and maintainer approval. Until then:

- real inference remains optional and user-supplied;
- CI and examples remain offline by default;
- no weight is copied into a wheel, npm tarball, GitHub Release, fixture, or demo asset;
- no accuracy claim is permitted without a labelled evaluation dataset.
