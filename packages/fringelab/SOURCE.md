# FringeLab extraction provenance

Source owner: WUHAO19831214. Repository: https://github.com/WUHAO19831214/webcam-laser-fringelab. Fixed commit: `37a8b3996791790a22980b0d562996a65a3a65ef`.

The source owner explicitly requested both extraction batches and collection into this owner-maintained MIT repository on 2026-10-04. This record covers transfer of author-owned TypeScript algorithms and helpers under the destination MIT license. The historical source root license is unchanged. Third-party libraries, trained language data and private photographs retain their own terms; none are relicensed as repository code.

`packages/fringelab/source-files.json` records SHA-256 for every original file. The 18 extracted source modules change relative module paths/extensions only. The virtual ruler/ROI React renderers, reusable floating panel, validated calibration/session wrappers, Worker runner, camera SourceSensor and processor adapters are new destination glue. The source application's teaching flow, deployment and device orchestration were not replaced.

Source calculator: `calculateExpression`; ROI: `roiLocalToWorld`, `roiWorldToLocal`, `resizeRoiFromCorner`; manual ruler: `calculateMmPerPixel`, `generateRulerTicks`, `suggestRulerAlignment`; local scale: `validateSpatialAnchors`, `mapScreenPointMm`; automatic ruler: `detectPhysicalRuler`, `fitRulerTicksRobust`; OCR: `recognizeRulerReadings`; profile: `extractStripProfile`; features: smoothing/background/period/peak/FWHM functions; optics: exact-order regression, uncertainty and models; simulator: `simulateDiffraction`.

Verification: `python tools/compare_fringelab_source.py --source /path/to/webcam-laser-fringelab` extracts the fixed git object into a temporary directory, verifies source hashes and compares source outputs against the package and checked-in golden. It never reads uncommitted source behavior. Original 55 tests are ported with import paths only. The source `syntheticRuler` fixture helper is separately anchored in the provenance manifest.

The four ruler golden scenes exercise light/dark/yellow/rotated/missing-tick/perspective cases. These are synthetic and do not certify physical ruler accuracy. Prior IMG_6815/IMG_6816 observations are historical records; the private photographs are not distributed. Automatic scale remains a candidate and manual/multi-point calibration remains available.

Browser OCR retains Tesseract.js 6 and SPARSE_TEXT/word boxes. It is a specialized companion backend; it does not silently change the existing ocr.number sensor's single-ROI contract or its Tesseract.js 7 backend. Browser camera uses existing camera.capture identity with backend version 0.3.1; the immutable Python release/backend stays 0.3.0.

Rollback: uninstall the new toolkit package or use the previous destination/source commit. The original FringeLab application continues to work independently; no global algorithm replacement occurred.
