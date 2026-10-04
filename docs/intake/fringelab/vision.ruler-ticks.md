# Sensor Proposal: vision.ruler-ticks

Decision: ACCEPT (2026-10-04).

Fixed source: https://github.com/WUHAO19831214/webcam-laser-fringelab, `37a8b3996791790a22980b0d562996a65a3a65ef`.

Files: lib/ruler-detection.ts, lib/ruler.worker.ts, lib/ruler-ocr.ts

Symbols: detectPhysicalRuler, fitRulerTicksRobust, recognizeRulerReadings

Input: original RGBA FramePacket and explicit ROI/options. Output: pixel/profile observations and quality, not calibrated physical quantities. Reuse: optics, spatial image measurements and camera teaching applications.

Dependencies: shared core contracts; pure detection/strip code is dependency-free. Browser OCR is optional and retains Tesseract.js terms. Source-owner authorization and completion conditions are recorded in the adjacent JSON.

New-domain rationale: vision domain: geometric tick positions and candidate periods are direct visual observations, not object tracking, OCR text or confirmed physical scale.
