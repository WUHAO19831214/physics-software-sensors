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

## Publication actions — intentionally unchecked in the Draft PR

- [ ] PR receives independent review.
- [ ] Phase 4A PR is merged.
- [ ] Merge commit is tagged `v0.6.0`.
- [ ] GitHub Release `Physics Software Sensors v0.6.0 — Experimental` is created.
- [ ] Exactly the reviewed artifacts, manifest and `SHA256SUMS` are attached.
- [ ] Downloaded files pass post-release SHA-256 verification.
- [ ] Release page links are added to README/Sensor Pages in a follow-up if needed.

PyPI and npm registry publication are not checklist items for this release.
