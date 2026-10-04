# Third-party boundaries

- Author-owned extracted TypeScript and new adapters/UI: destination MIT, per source-owner extraction request recorded in SOURCE.md.
- Tesseract.js 6: Apache-2.0; language data and WASM retain upstream terms. First OCR use may download a model. Images are processed locally.
- heic-to 1.6.5 / libheif: LGPL-3.0, unchanged optional dynamic dependency. Install without optional dependencies when HEIC is not required; normal PNG/JPEG/WebP decoding remains available. See licenses/heic-to-LGPL-3.0.txt. Model/code not copied into core.
- React/React DOM: MIT peer dependencies, required only for the /react entry point.
- Shared sensor contracts: @physics-software-sensors/core 0.3.0, MIT, installed from a local tgz. No npm registry publication is implied.
- No user photos, commercial fonts, model weights or source application's branding assets are included.
