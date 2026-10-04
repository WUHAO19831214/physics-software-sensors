# FringeLab fixed-source synthetic dataset

Source https://github.com/WUHAO19831214/webcam-laser-fringelab at `37a8b3996791790a22980b0d562996a65a3a65ef`; fixture source hashes are in packages/fringelab/source-files.json. No private photograph is included.

Inputs: fixed seeded 320×100 double-slit frame, a rotated ROI, explicit channel/profile parameters, manual ruler and three known mm anchors, arithmetic edge cases, five optical orders; four 720×280 synthetic rulers with light/dark/yellow bodies, rotation, missing ticks and perspective variation. Output: checked-in packages/fringelab/tests/fixtures/source-golden.json produced by the fixed git object, not the extracted implementation.

Protocol: verify original file hashes; run tools/fringelab-golden-harness.mjs against temporary source .ts and built package .js; JSON-normalize typed arrays/NaN; remove only ruler createdAt; compare all numeric and failure-state fields exactly. Maintain original algorithm tests and additional boundary/lifecycle regressions.

Limits: synthetic output demonstrates source compatibility, not an independently calibrated physical instrument. Known real-photo period ambiguity is preserved as a limitation; manual/multi-point modes remain first-class. Camera timing/error and OCR quality on actual devices are not measured here.
