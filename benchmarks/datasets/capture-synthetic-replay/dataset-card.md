# Dataset Card — Capture Synthetic Replay

- ID: `capture-synthetic-replay-v1`
- Sensors: `camera.capture`, `screen.capture`
- Privacy: repository-generated pixels only; no camera image, screen content, person or device identifier
- License: repository MIT
- Evidence: deterministic source-adapter behavior, not real device/runtime compatibility

## Camera cases

Three 640×360 BGR frames with fixed 50 ms monotonic intervals, nominal 20 FPS and one injected dropped-frame count. The request intentionally says 1280×720 at 30 FPS so tests can verify that requested, nominal and measured rates are not conflated.

## Screen cases

Two 2×1 RGBA frames with fixed 250 ms intervals and one injected dropped-frame count. A separate repository-generated 800×300 shared-window-style frame is used for Screen→OCR composition.

## Intended use and limits

Use only for serialization, lifecycle, timing-field, hash, drop accounting and composition regression. Do not use it to claim camera FPS, browser capture performance, permission compatibility, image quality, CPU/memory, or physical measurement accuracy.
