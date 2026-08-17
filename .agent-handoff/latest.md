# Physics Software Sensors — Agent Handoff

## Current state

- Status: **RELEASED**
- Phase: **4A — Experimental Public Distribution**
- PR #6: [merged](https://github.com/WUHAO19831214/physics-software-sensors/pull/6)
- Phase 4A merge SHA: `1a4a3fe45c1eaafe06c7e053644188b7abba8c62`
- Annotated tag: `v0.6.0`, peeled target exactly the merge SHA
- Release: [Physics Software Sensors v0.6.0 — Experimental](https://github.com/WUHAO19831214/physics-software-sensors/releases/tag/v0.6.0), public pre-release
- Post-release documentation update: `89e0e845ae04fdeec094af9f47900b4ec987e049`
- Current planning branch: `agent/phase4b-i18n-sensor-intake`

## Release positioning

All seven sensors remain `experimental` with E1–E3 evidence. This GitHub-only release is pre-stable and is not stable, validated, production-ready, measurement-grade or metrology-ready. Nothing was published to PyPI or the npm registry. Historical source repositories were not modified.

| Surface | Version |
| --- | --- |
| Repository Release | `v0.6.0` |
| Python package | `0.5.0` |
| TypeScript package | `0.3.0` |
| SensorEvent / FramePacket contracts | `1.0.0` / `1.0.0` |

## Published artifacts

The Release has exactly 11 attachments: one wheel, one tgz, seven Sensor Bundles, `release-manifest.json` and `SHA256SUMS`. Canonical bytes and hashes are in [`release/release-manifest.json`](../release/release-manifest.json) and [`release/SHA256SUMS`](../release/SHA256SUMS). The manifest is the exact published attachment; its candidate-state wording records build-time state and was not silently rewritten after publication.

## Verification

- Full pre-release verification: repository validation; Python **75 passed**; TypeScript **15/15 offline**, **18/18 full**; composition **5/5**.
- Final merge-SHA rebuild: two isolated builds, **11/11 byte-identical**.
- GitHub download: **11/11** attachments passed `SHA256SUMS`; manifest sizes/hashes passed **9/9**; local-final comparison passed **11/11**.
- Fresh downloaded-wheel consumer: Camera→Spot and Camera→YOLO-recorded passed.
- Fresh downloaded-tgz consumer: Screen→real Tesseract OCR passed with `-2.33`.
- Downloaded Sensor Bundles: **7/7** structure, provenance SHA, dependency boundary and model exclusion passed.
- Tracked or packaged `.pt`/`.onnx`/`.engine`: **0**.
- Five fixed source repository commits were freshly fetched and clean; no source repository changed.

## Boundaries

No sensor has E4 real-device or E5 downstream evidence. No YOLO weights are bundled or automatically downloaded. GitHub Actions remains disabled because the maintainer OAuth credential lacks `workflow` scope; fixed-SHA local, reproducibility and clean-consumer evidence is recorded instead.

## Next phase boundary

Phase 4A is complete. Phase 4B currently contains only [`docs/phase4b-plan.md`](../docs/phase4b-plan.md): a planning skeleton for English / Simplified Chinese / Japanese documentation and a long-term new-Sensor intake workflow. Do not begin large translation work or add an eighth sensor until the next task defines and reviews the implementation requirements.
