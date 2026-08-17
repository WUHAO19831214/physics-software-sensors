# Release reproducibility report

Status: **verified for the recorded environment, release/tag SHA and downloaded GitHub attachments**.

Phase 4A built squash-merge commit `1a4a3fe45c1eaafe06c7e053644188b7abba8c62` twice in separate empty temporary directories with `SOURCE_DATE_EPOCH=1786931073` (the commit timestamp) and `PYTHONHASHSEED=0`.

Environment: Darwin 25.3.0 arm64, Python 3.12.13, Node 24.13.0, npm 11.6.2.

## Result

All 11 generated files were byte-for-byte identical across the two builds:

- Python wheel: 1/1 match;
- TypeScript tgz: 1/1 match;
- Sensor bundles: 7/7 match;
- `release-manifest.json`: match;
- `SHA256SUMS`: match.

The canonical hashes are committed in [`SHA256SUMS`](SHA256SUMS). The 11 GitHub Release attachments were downloaded into a fresh directory and passed the same checksum file; all downloaded files were byte-identical to the final local build. Fresh consumers installed the downloaded wheel/tgz and passed Camera→Spot, Camera→YOLO-recorded and Screen→real Tesseract OCR (`-2.33`). Seven downloaded bundles passed structure and model-boundary checks.

This demonstrates deterministic output for the same Git SHA and recorded toolchain/environment plus publication integrity. It does not yet prove cross-OS, cross-architecture or future-build-backend reproducibility; those remain `not measured`.
