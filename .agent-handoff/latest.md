# FringeLab collection handoff

Status: READY_FOR_REVIEW. Branch: `codex/fringelab-toolkit`. Both component batches delivered; current catalog 9 Sensors + 4 Companion Tools. Source and immutable v0.6.0 stay unchanged.

- [Toolkit guide](../docs/fringelab-toolkit.md)
- [Package API](../packages/fringelab/README.md)
- [Runnable browser example](../examples/web-fringelab-toolkit/README.md)
- [Evidence report](../benchmarks/results/fringelab-extraction-2026-10-05.md)
- [Machine-readable handoff](latest.json)

62 toolkit tests and 30 core tests passed; 7 browser flows, 5 event-schema checks and fixed-source output comparison passed. Synthetic/offline evidence; physical device and real-photo error remain not measured. Browser OCR completed with no usable anchor on the default synthetic crop. Automatic and OCR results remain drafts with full manual/multi-point fallback.

Build local tgz plus two new Sensor Bundles with `python3 tools/build_fringelab_artifacts.py`. The three languages document unreleased 0.1.0 separately from immutable v0.6.0. No registry publication or source application migration was performed.
