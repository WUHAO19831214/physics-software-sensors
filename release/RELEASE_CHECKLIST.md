# v0.6.0 Experimental Release checklist

## Release candidate validation

- [x] Repository validation passes.
- [x] Python full test suite passes.
- [x] TypeScript offline test suite passes without runtime model download.
- [x] TypeScript full suite, including real Tesseract synthetic-pixel integration, passes.
- [x] Composition matrix passes 5/5.
- [x] Python wheel and TypeScript tgz build from one recorded tested SHA.
- [x] Seven Sensor Bundles build and their `BUNDLE.json`/structure validate.
- [x] `release-manifest.json` records 9 artifacts, environment, contracts and hashes.
- [x] `SHA256SUMS` covers 9 artifacts plus the manifest.
- [x] Clean-room Python Camera/Color/Spot/Template/YOLO-recorded smoke passes.
- [x] Clean-room TypeScript Screen/OCR/real-pixel Tesseract smoke passes.
- [x] Two consecutive builds are compared and reproducibility is recorded honestly.
- [x] Dependency/license and historical source-license boundaries are reviewed.
- [x] No `.pt`, `.onnx`, `.engine` or third-party weight is tracked or packaged.
- [x] Release Notes, download/install docs, seven Distribution sections and Agent Handoff are complete.
- [x] Five fixed source repository commits are clean.

## Publication actions

- [x] PR receives independent review.
- [x] Phase 4A PR is squash-merged as `1a4a3fe45c1eaafe06c7e053644188b7abba8c62`.
- [x] Annotated tag `v0.6.0` points exactly to the merge commit.
- [x] GitHub pre-release `Physics Software Sensors v0.6.0 — Experimental` is created.
- [x] Exactly the reviewed 11 artifacts/metadata files are attached.
- [x] All 11 downloaded files pass post-release SHA-256 verification.
- [x] Downloaded wheel/tgz pass fresh consumer tests; downloaded bundles pass 7/7 checks.
- [x] Release page links are added to README, download guide and all seven Sensor Pages.

PyPI and npm registry publication are not checklist items for this release.
