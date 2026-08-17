# Physics Software Sensors v0.6.0 — Experimental

This is an experimental pre-stable release intended for evaluation, reuse experiments, teaching-tool development, and integration testing.

这是实验性、pre-stable 的公开评估版本，面向复用实验、教学工具开发和集成测试；它不是 stable、production-ready、validated 或 measurement-grade 版本。

## What's included

Seven software sensors, all still `experimental`:

- Camera Capture — E1
- Screen Capture — E1
- Number OCR — E3
- Color Marker Tracker — E2
- Spot Centroid Tracker — E2
- Template Tracker — E3
- YOLO Tracker — E2

Evidence levels describe actual exercised paths, not metrological accuracy or maturity.

## Packages

- `physics_software_sensors-0.5.0-py3-none-any.whl`
- `physics-software-sensors-core-0.3.0.tgz`

Repository release `v0.6.0`, Python `0.5.0`, TypeScript `0.3.0`, Sensor implementation versions and Contract `1.0.0` are intentionally independent.

## Sensor bundles

Seven versioned zip files provide an independently readable Sensor Page, provenance, assets, example, evidence and dependency/install metadata. They depend on the matching package artifact and do not copy package core.

## Important limitations

- Experimental only; no metrology claim, calibration guarantee or measurement-grade claim.
- Real-device validation is incomplete; no sensor currently has E4 or E5 evidence.
- No YOLO model or third-party weight is bundled or downloaded. Real inference requires a separately reviewed local runtime and `ModelArtifact`.
- GitHub Actions is not enabled because the maintainer OAuth credential lacks `workflow` scope. A reviewed offline workflow remains at `templates/github-actions-ci.yml`.
- Historical source repository license state remains pending/NOASSERTION where documented.
- The packages are distributed only as GitHub Release files; nothing is published to PyPI or npm registry.

## Verification

The final RC is accepted only after repository validation, Python tests, TypeScript offline/full tests, five composition paths, two independent builds, clean-room wheel/tgz tests, all seven bundle structure checks, model-weight exclusion and source-repository clean checks pass. Exact tested SHA, counts, environment, file sizes and SHA-256 values are recorded in `release-manifest.json`, `SHA256SUMS`, the reproducibility report and Agent Handoff.

## Upgrade and rollback

There is no previous public GitHub Release. To roll back an evaluation, uninstall the local wheel/tgz and return to the Phase 3D merge commit `89d26f4f306204cdae72d6988f46191f3e789cbb` (or a consumer's previously pinned commit). Do not delete existing source-project code; downstream integrations must retain a feature flag or dependency pin and an old path until comparison succeeds.

No tag or GitHub Release is created by the Phase 4A Draft PR. After independent approval only: squash merge, tag the merge commit as `v0.6.0`, create the Experimental GitHub Release, attach exactly the manifest-listed files, and verify downloads against `SHA256SUMS`.
