# GasLab and Core support provenance

Source: https://github.com/WUHAO19831214/charles-law-isochoric-lab at `b62d7fbefd412e2696096b3bce8fc0af3c5f8c3c`. Owner: WUHAO19831214. Its checked-in MIT license permits reuse; [source-files.json](source-files.json) pins historical file hashes. This is a refactoring/generalization and new destination implementation, not a claim of byte-identical extraction.

Historical paths/symbols: `src/simulation/maxwellBoltzmann.ts` (reference sigma 1.6 at 300 K, `sampleMaxwellVelocity`, `getTheoreticalVrms`, `getTheoreticalVp`, `getTheoreticalVavg`, `maxwellPdf`); `src/simulation/molecularSystem.ts` and `src/simulation/claudeModel/gasModel.ts` (wall geometry, speed scaling and collision statistics); `src/sensors/ocrRecognizer.ts` (pressure/temperature parsing); `src/utils/mathFitting.ts` (linear fitting, extrapolation and nice ticks).

Antigravity's PSS transfer commits are Core `6262fd87a032f2c665a476653f226496688b85f9` and gaslab `5fbade46aa6a819e56c5cb360c87ab0bf9ca7eb5`. GasSimulationEngine/Driver, generic container APIs and shared support modules are destination abstractions. The review changes fix signed parsing, unit consistency, missing-data handling, time, snapshot isolation, seeded reset, geometry and corner contacts; source application behavior is therefore not asserted equivalent for these bug cases.

The source application's uncommitted local adaptation consumes sampling/scaling and Core helpers. It does not replace its rendered molecular systems or replay UI with GasSimulationEngine/Driver. Its test/build pass is local evidence, not a remotely merged integration. React/Three.js teaching UI and third-party OCR/assets are not copied into gaslab. The target package has zero runtime dependencies and no real sensor acquisition.

Rollback: remove the unreleased packages or pin the source/PSS commits above. Existing released bundles and v0.6.0 artifacts are unchanged. Real-device validation, generic molecular interactions and piston dynamics remain out of scope.

The historical source default RMS speed is `sqrt(3)*1.6` (about 2.771 display units/s), whereas the new default is 2.5. Same-input comparisons use an explicit historical calibration to preserve that source convention; identical defaults are not claimed. The local app already adapted to the new 2.5 convention before this review.
