# Physics Software Sensors — Agent Handoff

## Current state

- Status: **READY_FOR_REVIEW**
- Phase: **4A — Experimental Public Distribution**
- Phase 3D merge SHA: `89d26f4f306204cdae72d6988f46191f3e789cbb`
- Branch: `agent/phase4a-experimental-release`
- Tested repository SHA: `14cebeaa25cc1493ae421bb344f251d8a6af06fd`
- Artifact source SHA: `1dda09eb54883e94689e27472f97e03aeab59c91`
- Draft PR: [#6](https://github.com/WUHAO19831214/physics-software-sensors/pull/6), OPEN / MERGEABLE at handoff preparation
- Proposed tag: `v0.6.0` — **not created**
- Proposed Release: `Physics Software Sensors v0.6.0 — Experimental` — **not created**

## Release positioning and versions

This is an experimental pre-stable release intended for evaluation, reuse experiments, teaching-tool development and integration testing. It is not stable, validated, production-ready, measurement-grade or metrology-ready.

| Version surface | Value |
| --- | --- |
| Repository Release | `v0.6.0` |
| Python package | `0.5.0` |
| TypeScript package | `0.3.0` |
| Sensor implementations | `0.2.0`–`0.5.0` by manifest |
| SensorEvent / FramePacket | `1.0.0` / `1.0.0` |

No package or Sensor version was forced to match the repository release.

## Release artifacts

`release/release-manifest.json` records the build environment, tested artifact source SHA, evidence note, exact bytes and SHA-256. `release/SHA256SUMS` covers all nine artifacts plus the manifest.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `physics_software_sensors-0.5.0-py3-none-any.whl` | 36,702 | `6fd6d903d392bd2f672d892b04a3234e9e998e5b0deea75b252dabdc9751dcef` |
| `physics-software-sensors-core-0.3.0.tgz` | 13,561 | `704e0f21ea5bdf02156af1cfdc0b8fce6605996f3ecb4dbe8fbb6b25f0b70d3a` |
| `camera.capture-0.3.0.zip` | 173,496 | `dbb0c59458764c3007989ae6033a2dc8d8f046a36e4d6109b990a618207730a9` |
| `screen.capture-0.3.0.zip` | 201,631 | `f3decb0c5c7a398430bfc25e7ba128e5eb6839d860a73b6e61cda3228f9c7326` |
| `ocr.number-0.2.0.zip` | 151,902 | `b3f2734bdf72742a4856bc2807a610332171d604b89352dabc034be94e282bed` |
| `tracker.color-marker-0.2.0.zip` | 122,791 | `8a450c764d90fab9243f5b9a5b87364be61bd4755fd018f02e27212f578f063e` |
| `tracker.spot-centroid-0.4.0.zip` | 150,181 | `f228c3e478f1abbb29076dd81ba8987b876f448f5b00e84bee485a524dc6bb73` |
| `tracker.template-0.4.0.zip` | 76,253 | `7284e2e72878daa044a1b41313447620e913083a93ad3b7b66af377821a538aa` |
| `tracker.yolo-0.5.0.zip` | 89,998 | `165559183f1602508e70dd911ca3ae020c839d9f8cca58050599c010d4497d93` |

No binary artifact is committed to the repository or published. These files remain in temporary RC directories for review/attachment after approval.

## Verification

- Repository validation: passed — 39 JSON files, exactly 7 Sensor Pages, all with Distribution sections, manifest and checksum structure.
- Python: **75 passed, 0 failed**.
- TypeScript: **15/15 offline**, **18/18 full**, including real Tesseract synthetic-pixel integration.
- Composition: **5/5**.
- Clean-room Python wheel: Camera→Color/Spot/Template/YOLO-recorded **4/4**.
- Clean-room TypeScript tgz: Screen→real Tesseract OCR passed with expected `-2.33`.
- Sensor bundles: **7/7** structure, BUNDLE/dependency metadata, root internal links and assets passed; package core copies: **0**.
- Reproducibility: two separate empty directories, **11/11 generated files byte-identical** for the recorded SHA/toolchain.
- Tracked or packaged `.pt`/`.onnx`/`.engine`: **0**.
- Five fixed source repository commits: freshly fetched and clean; no source repository modified.

## Public documentation and licensing

- Download guide: `docs/downloading-sensors.md`
- Installation guide: `docs/installation.md`
- Third-party summary: `THIRD_PARTY_NOTICES.md`
- Release Notes: `release/RELEASE_NOTES.md`
- Reproducibility: `release/REPRODUCIBILITY.md`
- Checklist: `release/RELEASE_CHECKLIST.md`
- Seven Sensor Pages each identify package, bundle, entrypoint, maturity/evidence and example.

Repository-owned code/docs are MIT. NumPy, OpenCV, Tesseract.js, pngjs, optional Ultralytics/`lap`, ByteTrack reference and browser API boundaries are recorded. Historical source license gaps remain pending/NOASSERTION; they were not assigned MIT.

## YOLO and CI boundaries

No YOLO weight is tracked, packaged or downloaded. The public offline path uses `RecordedDetectorBackend` with the new `yolo-recorded` extra. Real inference remains `not measured` and requires optional runtime plus a reviewed local `ModelArtifact`.

GitHub Actions remains disabled because the current OAuth credential lacks `workflow` scope. The reviewed no-model-download workflow stays at `templates/github-actions-ci.yml`; PR #6 has no checks, while fixed-SHA local and clean-room evidence is recorded above.

## Publication boundary and next action

No tag, GitHub Release, PyPI publication or npm registry publication was performed. All seven sensors remain experimental with E1–E3 evidence; no downstream migration or eighth sensor was started.

Ask ChatGPT to independently review Phase 4A and decide whether to merge, tag `v0.6.0`, create `Physics Software Sensors v0.6.0 — Experimental`, attach exactly the manifest-listed files plus manifest/SHA256SUMS, and perform post-download verification. Do not perform those actions automatically from this handoff.
