# Physics Software Sensors — Agent Handoff
## Current Phase
Phase 3C — YOLO Tracker
## Status
IN_PROGRESS

## Repository

* Repository: `WUHAO19831214/physics-software-sensors`
* Base branch: `main`
* Working branch: `agent/phase3c-yolo-tracker`
* Base SHA: `9d48904b86c4e2ec218faf2fd18968abbfa7f0b6`
* HEAD SHA: `9d48904b86c4e2ec218faf2fd18968abbfa7f0b6`
* PR: not created
* PR state: not created
* Mergeable: unknown
* Working tree: modified during Phase 3C development

## Previous Phase

* Previous PR: #3
* Previous merge SHA: `9d48904b86c4e2ec218faf2fd18968abbfa7f0b6`

## Implemented

Phase 3C implementation is in progress. Final verified claims will replace this section before review.

## Public APIs

In progress; see the working tree and do not accept this handoff as completed evidence.

## Source Provenance

* Source repository: `WUHAO19831214/audio-visual-soundfield-tracker-stable`
* Source commit: `85740d686c67452a057540edb564d713e01ccc51`
* Source files: `src/detector.py`, `src/camera_processor.py`
* Class/function: `Detector`, `Detection`, `CentroidTracker`, `CameraProcessor._update_tracks`
* Extraction method: behavior-preserving adapter plus source-executed deterministic replay; source repository unchanged

## Tests

* Repository validation: pending final run
* Python: pending final run
* TypeScript: pending final run
* Golden: pending final run
* Composition: pending final run
* Clean install: pending final run

## Benchmarks

Final benchmark claims pending final run; real inference is not measured.

## Demo Assets

Final asset list pending final verification.

## Licensing

* Repository license: MIT
* Source license state: pending / fixed source repository has no detected license file
* Model/runtime license state: under documented review
* Weight redistribution state: no weight committed or redistributed

## Source Repositories

Five fixed source repositories are recorded in `latest.json`; all were clean at Phase 3C start.

## Contract Versions

* SensorEvent: `1.0.0`
* FramePacket: `1.0.0`
* Sensor implementation version: `0.5.0` (working)

## Current Sensor Catalog

`camera.capture`, `screen.capture`, `ocr.number`, `tracker.color-marker`, `tracker.spot-centroid`, `tracker.template`, `tracker.yolo`: experimental target state; final validation pending.

## Remaining Blockers

Final repository, package and GitHub verification is still in progress.

## Recommended Next Phase

Do not start another phase from an `IN_PROGRESS` handoff.

## ChatGPT Instruction

Review this handoff together with the current GitHub PR and repository state. Verify the claims independently from GitHub before accepting them. If the phase passes review, produce the next Codex prompt. Do not rely only on this handoff summary.
