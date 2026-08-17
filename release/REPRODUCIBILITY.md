# Release reproducibility report

Status: pending final RC comparison.

Phase 4A will build the same tested commit twice in separate empty temporary directories with `SOURCE_DATE_EPOCH` set to that commit's timestamp and `PYTHONHASHSEED=0`. It will compare the wheel, tgz, seven bundles, release manifest and `SHA256SUMS` byte-for-byte.

The final report will list exact matching/non-matching files and causes. Archive hashes will not be described as deterministic unless the two independent builds actually match.
