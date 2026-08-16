# Physics Software Sensors — Agent Handoff
## Current Phase
Phase 3C — YOLO Tracker
## Status
READY_FOR_REVIEW

## Repository

* Repository: `WUHAO19831214/physics-software-sensors`
* Base branch: `main`
* Working branch: `agent/phase3c-yolo-tracker`
* Base SHA: `9d48904b86c4e2ec218faf2fd18968abbfa7f0b6`
* HEAD SHA: `6f4380f8a925f324c64cbd73fa45805f78dfe048` (exact tested implementation snapshot; the published tip is the handoff-only child commit described in `.agent-handoff/README.md`)
* PR: [#4](https://github.com/WUHAO19831214/physics-software-sensors/pull/4)
* PR state: OPEN / DRAFT
* Mergeable: MERGEABLE
* Working tree: clean after the handoff-only commit

## Previous Phase

* Previous PR: [#3](https://github.com/WUHAO19831214/physics-software-sensors/pull/3)
* Previous merge SHA: `9d48904b86c4e2ec218faf2fd18968abbfa7f0b6`

## Implemented

* Added `tracker.yolo@0.5.0` as the seventh experimental / incubating adapter.
* Added explicit local `ModelArtifact` with SHA-256, runtime, class names and license-state fields; HTTP(S) model URIs are rejected.
* Added deterministic `RecordedDetectorBackend`, optional `YoloDetectorBackend`, source-compatible person-only `OpenCVHogDetectorBackend`, and `CentroidAssociator`.
* Added multi-target `payload.detections[]` with bbox, center, class, detector score, track ID and native-ID availability; SensorEvent and FramePacket Schemas remain `1.0.0`.
* Separated detection from tracking and detector confidence from tracking confidence, uncertainty and physical accuracy.
* Added all/ID/name class filters, requested/actual/attempted backend metadata, explicit fallback/warning flags, and Schema-valid error events without mock detections.
* Added source-generated golden replay, offline example, assets, dataset card, microbenchmark, complete Sensor Page, upgrade record and model/license review.
* Added the repository-level Agent Handoff mechanism and validator.

## Public APIs

* `physics_sensors.core.ModelArtifact`
* `physics_sensors.tracking.ClassFilter`
* `physics_sensors.tracking.YoloDetection`
* `physics_sensors.tracking.DetectorFrameResult` / `DetectorBackend`
* `physics_sensors.tracking.RecordedDetectorBackend`
* `physics_sensors.tracking.OpenCVHogDetectorBackend`
* `physics_sensors.tracking.YoloDetectorBackend`
* `physics_sensors.tracking.CentroidAssociator`
* `physics_sensors.tracking.YoloTrackerSensor`

## Source Provenance

* Source repository: `WUHAO19831214/audio-visual-soundfield-tracker-stable`
* Source commit: `85740d686c67452a057540edb564d713e01ccc51`
* Source files: `src/detector.py`; `src/camera_processor.py`; `requirements.txt`; `config.yaml`; `scripts/setup_yolo.sh`; `models/README.md`; `tests/test_detector.py`; `tests/test_tracking.py`
* Class/function: `Detection`; `Detector.__init__/detect/track/_parse_yolo_results/_detect_hog`; `CentroidTracker.update/reset`; `CameraProcessor._update_tracks`
* Extraction method: dependency-injected behavior reimplementation plus direct execution of the fixed source for golden output; UI/business code, project-directory model scanning and automatic model preparation were excluded; source repository unchanged

## Tests

* Repository validation: passed — 35 JSON files, exactly 7 Sensor Pages/manifests, reviewed demo assets and local Markdown links.
* Python: 65 passed, 0 failed; YOLO module 16 passed.
* TypeScript: 18 passed, 0 failed.
* Golden: source script regenerated 3 detection, 6 tracking and 6 centroid source cases plus 7 recorded frames from the exact source SHA.
* Composition: 5/5 workflows — Camera→Color, Camera→Spot, Camera→Template, Camera→YOLO, Screen→OCR.
* Clean install: wheel `physics-software-sensors==0.5.0` imported/run outside the repository; Camera→four trackers passed; installed-wheel YOLO recorded example emitted 7/7 events.
* Clean install: npm tgz `@physics-software-sensors/core@0.3.0` installed in a clean consumer with an isolated npm cache; Screen→real-pixel Tesseract OCR passed.

## Benchmarks

Deterministic adapter, 500 mappings per serialization case on macOS arm64 / Python 3.12.13 / NumPy 2.5.2 / 360×260 synthetic frames:

* Single target median / p95: `0.099937 / 0.123583 ms`.
* Two-target serialization median / p95: `0.110354 / 0.130291 ms`.
* Class filters: 3/3.
* Tracking status + ID handling: 10/10.
* Real inference: not measured.
* Model/device/input/inference latency/FPS/process or GPU memory/detection count/accuracy: not measured.
* Reason: no maintainer-approved local model artifact; Ultralytics not installed; online download prohibited; no labelled evaluation set.

## Demo Assets

* `sensors/tracker.yolo/assets/overview.png`
* `sensors/tracker.yolo/assets/multi-target.png`
* `sensors/tracker.yolo/assets/tracking.png`
* `sensors/tracker.yolo/assets/fallback.png`
* `sensors/tracker.yolo/assets/events.json`

All are explicitly labelled recorded detector replay / synthetic fixture. None is represented as real inference.

## Licensing

* Repository license: MIT.
* Source license state: pending; the fixed historical source repository has no detected license file and GitHub metadata is `NOASSERTION`.
* Model/runtime license state: source dependency range is `ultralytics>=8.2,<9`; runtime was not installed in Phase 3C. Published Ultralytics metadata declares AGPL-3.0 with an Enterprise route; exact downstream terms require review.
* Weight redistribution state: not approved; no weight was committed, bundled, downloaded or redistributed. Artifact-specific weight license remains pending.
* Original ByteTrack and Ultralytics integration licensing are recorded separately; HOG uses OpenCV 4.x and is person-only.
* Review: `docs/yolo-model-and-license-review.md`.

## Source Repositories

* `audio-visual-soundfield-tracker-stable` — `85740d686c67452a057540edb564d713e01ccc51` — clean
* `spot-vibration-tracking-system-20260508-171952` — `7f0d91cc73afafaecc54acc46b2b9d69375d994a` — clean
* `forced-vibration-af-analyzer-20260502-122715` — `c3f58175a09ff29cacdfb976a5055758c4eff619` — clean
* `physics-experiment-bridge-mvp` — `8bba87df6475cae1e595fc925551db8bea83fb68` — clean
* `ampere-force-visualizer-teacher-yanan` — `cb073e89d6d87129287030f1df08bd540504eb39` — clean

## Contract Versions

* SensorEvent: `1.0.0`
* FramePacket: `1.0.0`
* Sensor implementation version: `tracker.yolo@0.5.0`

## Current Sensor Catalog

* `camera.capture` — experimental — `0.3.0`
* `screen.capture` — experimental — `0.3.0`
* `ocr.number` — experimental — `0.2.0`
* `tracker.color-marker` — experimental — `0.2.0`
* `tracker.spot-centroid` — experimental — `0.4.0`
* `tracker.template` — experimental — `0.4.0`
* `tracker.yolo` — experimental — `0.5.0`

## Remaining Blockers

None for current experimental phase.

Real inference, source/model license gates, labelled accuracy evaluation, real-camera L2, downstream integration and stable publication remain future maturity gates, not completed Phase 3C claims.

## Recommended Next Phase

After independent review, plan Phase 3D cross-sensor benchmark. Do not execute it from this handoff and do not merge Phase 3C automatically.

## ChatGPT Instruction

Review this handoff together with the current GitHub PR and repository state. Verify the claims independently from GitHub before accepting them. If the phase passes review, produce the next Codex prompt. Do not rely only on this handoff summary.
