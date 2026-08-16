# Physics Software Sensors — Agent Handoff

## Current state

- Phase: **3D — Cross-sensor validation and release readiness**
- Status: **IN_PROGRESS**
- Branch: `agent/phase3d-cross-sensor-validation`
- Base / Phase 3C merge: `ad1220d6166e43dc68a0bd0477728600de880c54`
- Draft PR: not created yet
- Source repositories: unchanged and clean at their five fixed SHAs

## Scope

This phase consolidates evidence levels, benchmark and compatibility matrices, purposeful source-to-processor composition tests, package dependency review, CI, release dry runs and single-sensor documentation bundles. It adds no new sensor, changes no Phase 1 contract, modifies no source repository, downloads no YOLO weight and does not publish a package or release.

## Current evidence

| Sensor | Evidence | Reason |
| --- | --- | --- |
| `camera.capture` | E1 | deterministic synthetic replay only |
| `screen.capture` | E1 | recorded RGBA replay and mocked browser boundaries only |
| `ocr.number` | E3 | real Tesseract.js runtime on synthetic pixels |
| `tracker.color-marker` | E2 | fixed-source golden comparison on synthetic frames |
| `tracker.spot-centroid` | E2 | fixed-source executable golden comparison |
| `tracker.template` | E3 | real OpenCV contrib runtime on synthetic sequence |
| `tracker.yolo` | E2 | source replay and adapter seam; real model inference not run |

All seven sensors remain experimental. Evidence completeness does not promote maturity.

## SHA semantics

Schema 1.1 records an exact `tested_sha`, while the published tip and the commit containing this file use explicit Git resolvers. The concrete published and handoff SHAs will be reported after the final push; see `.agent-handoff/README.md`. This replaces the squash-unsafe Phase 3C parent assumption.

## Verification in progress

- New Python composition tests: 4 passed.
- Screen→OCR remains represented by the existing real Tesseract.js composition test.
- Repository-wide tests, clean installs, release dry run, seven bundle dry runs and CI are pending final execution.

## Boundary

Do not merge this phase and do not start Phase 4 from this handoff.
