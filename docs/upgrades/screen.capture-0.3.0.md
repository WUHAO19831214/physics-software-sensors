# Upgrade record: screen.capture 0.3.0

- Date: 2026-08-16
- Contract: FramePacket `1.0.0` unchanged
- Implementation: first TypeScript adapter (`0.1.0 contract-only → 0.3.0 adapter-present`)
- Source anchors: see [`SOURCE.md`](../../sensors/screen.capture/SOURCE.md)
- Behavior change: source React panels are split into capture source and downstream OCR; no OCR/filter/store code copied
- Added behavior: explicit `start()` permission boundary, browser/recorded backends, stable errors, artifact hash, requested/measured sampling fields and serializer
- Compatibility: optional RuntimeFramePacket fields only; existing OCR inputs remain valid
- Verification: browser/replay/composition tests, real Tesseract composition, Schema validation and clean npm consumer
- Rollback: pin package `0.2.0` or continue using unchanged source applications
- Pending: browser/OS L2 matrix and source-license review
