# Yan'an Vector Reconstruction History

This is a source-history record, not a claim that the current Yan'an application still uses every historical channel. The source repository was inspected read-only at `cb073e89d6d87129287030f1df08bd540504eb39` with `git log`, `git show`, `git diff`, `git blame`, `git grep`, and string-history searches.

## Finding

Historical F1/F2/F3 is **CONFIRMED**, with a precise qualification: from the first force-visualization commit, the application treated the three simultaneous OCR scalar values as the x/y/z orthogonal components of one resultant force at a common point. The UI also called them three orthogonal forces. They were not documented as three arbitrary non-orthogonal vectors or as three axes returned by one hardware SDK.

The current application is different: it observes Fy and Fz from two OCR ROIs and constructs Fx as an explicit zero constraint. It retains F2/F3 only as migration aliases.

## Timeline

| Version / commit | Screen channels | Physical meaning | OCR path | Vector mapping | 3D behavior | Reason/change evidence |
| --- | --- | --- | --- | --- | --- | --- |
| `f3d93b3404d4246a4a0e4395070c2b7e67baea58` (initial MVP, 2026-05-29) | F1, F2, F3 default ROIs | Generic force-labeled scalar screen channels; no force-composition implementation yet | Tesseract ROI pipeline | None yet | Generic `ThreeDVisualizationPanel`; no proven F1/F2/F3 vector composition | First appearance of the three ROI IDs. This commit alone does not prove xyz semantics. |
| `ac46ed58ed020c96e75d34d70759477ef898bbef` (2026-05-31) | F1, F2, F3 all required | README: three orthogonal forces at the same force point; F1→x, F2→y, F3→z; resultant `(F1,F2,F3)` | `readTesseractForces` finds all three Tesseract samples | Classroom `(F1,F2,F3)`; magnitude `sqrt(F1²+F2²+F3²)` | Component arrows and staged F1+F2→F12, then F12+F3→resultant | First definitive semantic and executable evidence. |
| `f75bd9002c8b7c1a38baadc459cb400ffa04e65d` (2026-06-03) | F1, F2, F3 | Same orthogonal-component model | Same | Classroom x→scene X, classroom y→scene Z, classroom z→scene Y | `createSceneForceVectors` makes three axis-aligned vectors and their sum | Adds the explicit classroom/Three.js mapping comments. |
| `ed33d00774cd7eedf1ff4c3bd9a2cf9225410cf5` (Yan'an customization, 2026-06-04) | Fy, Fz defaults; legacy F2/F3 aliases | Apparatus force is represented in the y-z plane; x is the conductor direction | `readTesseractForces` reads Fy or F2 and Fz or F3; it does not read Fx | `{fx: 0, fy: observed, fz: observed}` | Only Fy/Fz component arrows plus resultant; magnitude remains `sqrt(fx²+fy²+fz²)` | Commit title says Yan'an High School customization; code/UI changed together. No commit body states a more detailed reason, so the apparatus-plane rationale is an inference from the coordinate labels and explicit zero constraint. |
| `c9f362adc99b498d0ca606f8ed51e1a60b142b3c` (2026-06-05) → current `cb073e89d6d87129287030f1df08bd540504eb39` | Fy, Fz, with F2/F3 compatibility | Current two-observed-component behavior | Same | Adds `SCENE_X_POSITIVE_SIGN = -1`; classroom `(x,y,z)`→scene `(-x,z,y)` | Current renderer mapping | Current code and integration docs confirm behavior. Some older README overview text still mentions F1/F2/F3 and is stale. |

## File- and symbol-level evidence

| Commit | File | Symbol/text | Evidence |
| --- | --- | --- | --- |
| `f3d93b3404d4246a4a0e4395070c2b7e67baea58` | `src/screen/ScreenCapturePanel.tsx` | default F1/F2/F3 ROI definitions | Earliest channel appearance. |
| `ac46ed58ed020c96e75d34d70759477ef898bbef` | `README.md` | force-composition description | States F1=x, F2=y, F3=z and resultant `(F1,F2,F3)`. |
| `ac46ed58ed020c96e75d34d70759477ef898bbef` | `src/visualization/ForceVisualization3D.tsx` | `ForceTriplet`, `readTesseractForces`, force group | Requires all three OCR samples and computes the resultant. |
| `ed33d00774cd7eedf1ff4c3bd9a2cf9225410cf5` | `src/screen/ScreenCapturePanel.tsx` | defaults and legacy ROI migration | Switches defaults to Fy/Fz while detecting old F1/F2/F3 configuration. |
| `ed33d00774cd7eedf1ff4c3bd9a2cf9225410cf5` | `src/visualization/ForceVisualization3D.tsx` | `ForceTriplet`, `readTesseractForces` | Renames fields to fx/fy/fz, reads two values, sets `fx: 0`. |
| `cb073e89d6d87129287030f1df08bd540504eb39` | `src/visualization/ForceVisualization3D.tsx` | `createSceneForceVectors` | Maps classroom x/y/z to scene -X/Z/Y and sums the vectors. |
| `cb073e89d6d87129287030f1df08bd540504eb39` | `docs/DATA_PIPELINE.md`, `docs/SENSOR_INTEGRATION.md` | current data-flow descriptions | Confirms Fy/Fz reading with F2/F3 compatibility. |

`git blame` attributes the current Fy/Fz lookup and `fx: 0` to `ed33d007…`; it attributes the current sign inversion to `c9f362ad…`. `git log -S "channelId: 'F1'"` finds the initial introduction and the Yan'an removal/migration commit.

## Architectural decision

No new direct observation exists here. `screen.capture` observes pixels, `ocr.number` derives scalar readings from those pixels, and vector reconstruction then processes existing scalar measurements. The reusable extraction is therefore `vector.compose-3d`, a **Companion Processing Tool**, not an eighth Sensor.

The extraction is a clean-room rewrite of the small, general mathematical behavior. No source code, UI, logo, screenshot, or other asset was copied because the source repository has no explicit license file. Teacher controls, magnetic-field rendering, left-hand-rule UI, screenshots, layout, scaling panels, and lesson orchestration remain source-project concerns.
