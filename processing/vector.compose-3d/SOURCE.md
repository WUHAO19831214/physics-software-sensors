# Source and clean-rewrite record

## Source repository

- Repository: `WUHAO19831214/ampere-force-visualizer-teacher-yanan`
- Current reviewed commit: `cb073e89d6d87129287030f1df08bd540504eb39`
- Earliest F1/F2/F3 ROI commit: `f3d93b3404d4246a4a0e4395070c2b7e67baea58`
- Historical three-component force implementation: `ac46ed58ed020c96e75d34d70759477ef898bbef`
- Fy/Fz + constrained Fx transition: `ed33d00774cd7eedf1ff4c3bd9a2cf9225410cf5`
- Scene-X sign transition: `c9f362adc99b498d0ca606f8ed51e1a60b142b3c`

## Provenance anchors

| Commit | Path | Symbol | Role |
| --- | --- | --- | --- |
| `f3d93b3404d4246a4a0e4395070c2b7e67baea58` | `src/screen/ScreenCapturePanel.tsx` | default F1/F2/F3 ROI configuration | Earliest channel record. |
| `ac46ed58ed020c96e75d34d70759477ef898bbef` | `README.md` | 3D force-composition documentation | Defines F1/F2/F3 as orthogonal x/y/z components. |
| `ac46ed58ed020c96e75d34d70759477ef898bbef` | `src/visualization/ForceVisualization3D.tsx` | `ForceTriplet`, `readTesseractForces` | Historical three-OCR component flow and resultant magnitude. |
| `ed33d00774cd7eedf1ff4c3bd9a2cf9225410cf5` | `src/screen/ScreenCapturePanel.tsx` | defaults and legacy migration | Changes default screen channels to Fy/Fz. |
| `ed33d00774cd7eedf1ff4c3bd9a2cf9225410cf5` | `src/visualization/ForceVisualization3D.tsx` | `ForceTriplet`, `readTesseractForces` | Reads Fy/Fz, retains F2/F3 aliases, sets Fx to zero. |
| `cb073e89d6d87129287030f1df08bd540504eb39` | `src/visualization/ForceVisualization3D.tsx` | `createSceneForceVectors`, `SCENE_X_POSITIVE_SIGN` | Magnitude and classroom-to-scene behavior. |

The full research narrative is in [`../../docs/research/yanan-vector-reconstruction-history.md`](../../docs/research/yanan-vector-reconstruction-history.md).

## Extraction boundary

Extracted as general behavior: finite x/y/z components, magnitude, normalization, azimuth/elevation, explicit component sources, skew checking, quality preservation, a matrix coordinate transform, and renderer-neutral arrow data.

Not extracted: screen capture, OCR inference, React UI, Three.js scene ownership, magnetic field lines, left-hand rule, teacher controls, snapshots, scaling panels, layout, branding, lesson workflow, or source assets.

## Algorithm changes

The source did not have explicit missing/source/skew semantics or general azimuth/elevation output. The clean rewrite adds them because a reusable module must not treat a constrained zero as observed, silently combine asynchronous OCR results, or invent values for failed channels. The source-specific scene mapping is an opt-in transform and never changes core vector mathematics.

## Compatibility validation

`packages/typescript/tests/fixtures/vector3/yanan-golden.json` pins historical and current commits. Tests compare magnitude and component-to-scene mapping at `1e-12` tolerance. OCR composition tests reproduce the current `{Fx=0 constrained, Fy/Fz observed}` path and prove OCR failure produces an incomplete vector rather than a mock value.

## License decision

No explicit source-repository license file was found at the reviewed commit. This repository therefore does not claim that historical source code is MIT-licensed. The implementation is a small clean rewrite based on documented behavior and universal vector mathematics. No source code, screenshot, logo, or other asset was copied.
