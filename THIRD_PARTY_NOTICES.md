# Third-party notices

This repository's original code and documentation are licensed under the repository [MIT License](LICENSE). The following inventory summarizes dependencies and boundaries for the proposed experimental GitHub Release; it does not replace upstream license texts or legal review.

| Component | Use | Required/optional | Bundled in RC? | License/boundary |
| --- | --- | --- | --- | --- |
| NumPy | Python pixel arrays/tracking | optional extras | not vendored; resolved by installer | BSD-3-Clause |
| OpenCV / opencv-contrib headless | camera and classical CV backends | optional extras | not vendored | Apache-2.0 for current 4.x releases |
| Tesseract.js | real Number OCR backend | TypeScript dependency | package dependency, not vendored source | Apache-2.0; language data may be fetched/cached at runtime |
| pngjs | deterministic PNG handling | TypeScript dependency | package dependency, not vendored source | MIT |
| Ultralytics | optional real YOLO backend | optional `yolo-runtime` only | not installed or bundled in RC | upstream package metadata declares AGPL-3.0 with a separate enterprise route; downstream review required |
| `lap` | optional tracking runtime dependency | optional `yolo-runtime` | not bundled | BSD-2-Clause |
| Original ByteTrack project | historical algorithm/runtime reference | not a direct bundled package | not bundled | MIT; this does not replace terms of an actual integration such as Ultralytics |
| Browser `getDisplayMedia` | live screen capture platform API | browser capability | not bundled | browser/platform API; requires user permission |

## Model and data artifacts

No YOLO `.pt`, `.onnx`, `.engine`, third-party weight, Tesseract traineddata, camera recording or private device dataset is distributed in this release candidate. Model artifacts have their own provenance and licenses and require explicit local review.

## Historical source repositories

The five source repositories document where behavior was historically used. Where those fixed repositories have no detected license file or GitHub reports `NOASSERTION`, their license state remains **pending/NOASSERTION**. This repository does not assign MIT to that historical source code. Extracted behavior, provenance method and modifications remain recorded per Sensor Page/SOURCE file.

See [package dependency audit](docs/package-dependency-audit.md) and [licensing/provenance policy](docs/licensing-and-provenance.md) for links and detailed review notes.
