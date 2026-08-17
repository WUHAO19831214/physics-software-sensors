# Physics Software Sensors v0.6.0 — Experimental / Pre-stable Release

This is an experimental pre-stable release intended for evaluation, reuse experiments, teaching-tool development, and integration testing.

这是实验性、pre-stable 的公开评估版本；它不是 stable、production-ready、validated、measurement-grade 或 metrology-ready 版本。

## What's included

Seven software sensors, all still `experimental`:

- Camera Capture — E1
- Screen Capture — E1
- Number OCR — E3
- Color Marker Tracker — E2
- Spot Centroid Tracker — E2
- Template Tracker — E3
- YOLO Tracker — E2

Evidence levels describe exercised software paths, not metrological accuracy or maturity.

## Packages and bundles

- Python wheel: `physics_software_sensors-0.5.0-py3-none-any.whl`
- TypeScript tgz: `physics-software-sensors-core-0.3.0.tgz`
- Seven versioned Sensor Bundle zip files
- `release-manifest.json` and `SHA256SUMS`

Repository release `v0.6.0`, Python `0.5.0`, TypeScript `0.3.0`, Sensor implementation versions and Contract `1.0.0` remain intentionally independent. Packages are GitHub Release attachments only; nothing is published to PyPI or npm registry.

## Final release source and verification

- Release/tag source: `1a4a3fe45c1eaafe06c7e053644188b7abba8c62`
- Release: https://github.com/WUHAO19831214/physics-software-sensors/releases/tag/v0.6.0
- Two final builds: 11/11 generated files byte-identical in the recorded environment
- Python: 75 passed
- TypeScript: 15/15 offline and 18/18 full
- Composition: 5/5
- Local final-artifact clean room: Camera→Color/Spot/Template/YOLO-recorded 4/4; Screen→real Tesseract OCR passed
- Sensor Bundle structure: 7/7; package core copies: 0
- Tracked or packaged `.pt`/`.onnx`/`.engine`: 0
- Five fixed source repository commits: clean

Exact artifact bytes, SHA-256, build environment, experimental maturity and CI state are in `release-manifest.json`. Verify downloads with `SHA256SUMS`.

## Important limitations

- No sensor has E4 real-device or E5 downstream evidence; no metrology claim is made.
- No YOLO model or third-party weight is bundled or downloaded. Real inference requires a separately reviewed local runtime and `ModelArtifact`.
- GitHub Actions is not enabled because the maintainer OAuth credential lacks `workflow` scope. Validation used the fixed merge SHA, local test suites, two-build reproducibility and clean-room consumers.
- Historical source repository license state remains pending/NOASSERTION where documented.
- Real camera/browser/device compatibility is incomplete.

## Post-release download verification

All 11 attachments were downloaded again from GitHub and matched `SHA256SUMS`; the nine package/bundle artifacts also matched every size and SHA-256 entry in the published manifest. Fresh consumers installed only the downloaded wheel/tgz: Camera→Spot passed, Camera→YOLO-recorded passed, and Screen→real Tesseract OCR returned `-2.33`. All seven downloaded bundles passed structure, provenance, dependency-boundary and model-exclusion checks.

## Upgrade and rollback

This is the first public GitHub Release. To roll back an evaluation, uninstall the local wheel/tgz and return to Phase 3D merge commit `89d26f4f306204cdae72d6988f46191f3e789cbb`, or to the consumer's previous dependency pin. Existing source-project implementations must remain available behind a feature flag or old path until downstream comparison succeeds.

The attached manifest's `release_status` and first limitation intentionally preserve build-time candidate state. Publication state is recorded by the immutable annotated tag, GitHub Release page, this post-release report and Agent Handoff; the published attachment was not silently replaced after verification.
