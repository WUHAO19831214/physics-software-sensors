# Package dependency audit

Audit date: 2026-08-16. This is a release-readiness inventory, not legal advice. Package metadata and upstream license links must be rechecked for every release candidate.

## Python package `physics-software-sensors@0.5.0`

| Dependency | Used by | Required/optional | License | Bundled? | Runtime download? |
| --- | --- | --- | --- | --- | --- |
| NumPy `>=1.26,<3` | arrays/trackers | optional extras | [BSD-3-Clause](https://numpy.org/doc/stable/license.html) | no | no |
| OpenCV contrib headless `>=4.9,<5` | camera/classical trackers | optional extras | [Apache-2.0 for 4.5+](https://opencv.org/license/) | no | no |
| Ultralytics `>=8.2,<9` | real YOLO | optional `yolo-runtime` | [AGPL-3.0 / enterprise route in metadata](https://github.com/ultralytics/ultralytics/blob/main/pyproject.toml) | no | library may obtain models; this repository forbids automatic model download |
| `lap >=0.5.12,<1` | tracking runtime | optional `yolo-runtime` | [BSD-2-Clause](https://github.com/gatagat/lap/blob/master/LICENSE) | no | no |
| jsonschema / pytest | validation/tests | dev only | upstream-specific | no | package install only |

The original ByteTrack repository is [MIT licensed](https://github.com/FoundationVision/ByteTrack/blob/main/LICENSE), but that does not replace the license terms of the actual Ultralytics integration. Model weights are separate artifacts: no weight is committed, downloaded, bundled or approved for redistribution.

## TypeScript package `@physics-software-sensors/core@0.3.0`

| Dependency | Used by | Required/optional | License | Bundled? | Runtime download? |
| --- | --- | --- | --- | --- | --- |
| Tesseract.js `^7.0.0` | real number OCR | required package dependency | [Apache-2.0](https://github.com/naptha/tesseract.js/) | no | worker may fetch/cache language data |
| pngjs `^7.0.0` | PNG pixel fixtures | required package dependency | [MIT](https://github.com/pngjs/pngjs/blob/main/LICENSE) | no | no |
| TypeScript / Node types | build/typecheck | dev only | upstream-specific | no | package install only |

Browser `getDisplayMedia` is a platform API, not bundled and not downloaded. It is required only by the live screen driver; recorded replay remains usable without it.

The npm package remains `private: true`; Phase 3D only creates a local tgz. Publishing scope/naming is intentionally undecided.

## Release boundaries

- The committed CI template and release dry runs do not install `yolo-runtime`, download model weights or run real YOLO inference. The workflow is not enabled because current GitHub credentials lack `workflow` scope.
- The offline TypeScript CI template excludes the real Tesseract integration test so a clean runner does not fetch language data; the full integration test remains a separately reported local test.
- Single-sensor bundles contain documentation, example code and dependency metadata. They do not duplicate `physics_sensors.core` or TypeScript core.
- Before stable publication: generate an SBOM/license report, resolve historical source-license gaps, review exact transitive versions and approve each model/language artifact policy.
