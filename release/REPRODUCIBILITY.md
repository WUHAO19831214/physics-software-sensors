# Release reproducibility report

Status: **verified for the recorded environment and tested SHA**.

Phase 4A built tested commit `1dda09eb54883e94689e27472f97e03aeab59c91` twice in separate empty temporary directories with `SOURCE_DATE_EPOCH=1786929487` (the commit timestamp) and `PYTHONHASHSEED=0`.

Environment: Darwin 25.3.0 arm64, Python 3.12.13, Node 24.13.0, npm 11.6.2.

## Result

All 11 generated files were byte-for-byte identical across the two builds:

- Python wheel: 1/1 match;
- TypeScript tgz: 1/1 match;
- Sensor bundles: 7/7 match;
- `release-manifest.json`: match;
- `SHA256SUMS`: match.

The canonical hashes are committed in [`SHA256SUMS`](SHA256SUMS). This demonstrates deterministic output for the same Git SHA and recorded toolchain/environment. It does not yet prove cross-OS, cross-architecture or future-build-backend reproducibility; those remain `not measured`.
