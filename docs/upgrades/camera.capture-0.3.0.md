# Upgrade record: camera.capture 0.3.0

- Date: 2026-08-16
- Contract: FramePacket `1.0.0` unchanged
- Implementation: first Python adapter (`0.1.0 contract-only → 0.3.0 adapter-present`)
- Source anchors: see [`SOURCE.md`](../../sensors/camera.capture/SOURCE.md)
- Algorithm change: none; capture boundary extracted and tracking/UI removed
- Added behavior: backend seam, deterministic replay, OpenCV backend, artifact hash, three clocks, requested/nominal/measured rate and drop metadata
- Compatibility: existing FramePacket fields unchanged; new capture metadata uses optional `payload`
- Verification: seven camera tests, full Python suite, clean wheel consumer, 3-frame L1 replay
- Rollback: pin package `0.2.0` or continue using unchanged source applications
- Pending: real-device L2 and source-license review
