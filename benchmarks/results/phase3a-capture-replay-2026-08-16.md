# Phase 3A capture replay — 2026-08-16

## Scope and evidence

L0/L1 only. Inputs are repository-generated synthetic/recorded pixels. No real camera, browser screen share, device timing, physical measurement accuracy, CPU peak, or memory peak claim is made.

| Sensor | Input | Requested | Backend/fixture timing | Delivered | Dropped | Result |
| --- | --- | --- | --- | --- | --- | --- |
| `camera.capture@0.3.0` | 3 × 640×360 BGR | 1280×720 @ 30 FPS | nominal 20 FPS; fixed 50 ms intervals | 3/3; measured 20.0 FPS | 1 injected/preserved | Schema, lifecycle, hash, rate separation passed |
| `screen.capture@0.3.0` | 2 × 2×1 RGBA | 100 ms sampling | fixed 250 ms intervals | 2/2; measured 4 Hz | 1 injected/preserved | replay, hash, rate separation passed |
| screen → OCR | 800×300 RGBA `-2.33` | 500 ms | one recorded frame | 1/1 | 0 | Tesseract rawText/value both `-2.33` |

Camera inter-frame jitter is 0 ms by fixture construction; it is a determinism assertion, not hardware performance. A single standalone screen frame correctly reports measured interval/rate as `null`.

## Gates exercised

- Python FramePacket validation, replay, drop and lifecycle tests;
- TypeScript recorded replay, browser permission request timing, permission denial and stream-source composition;
- serialized Screen FramePacket validated by the repository JSON Schema;
- real-pixel Tesseract composition with no mock fallback;
- clean wheel/tarball consumer imports and source→processor smoke.

## Pending L2/L3

CPU, memory, first-frame/capture delivery latency, OpenCV backend/device matrix, browser/OS chooser behavior, long-run jitter/drops, disconnect/end recovery, exposure/resolution negotiation and privacy-reviewed real frames.
