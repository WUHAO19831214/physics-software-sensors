# Physics Software Sensors — NEW_REUSABLE_TOOL Handoff

## Review state

- Status: **READY_FOR_REVIEW**
- Task: **NEW_REUSABLE_TOOL**
- Tool: **`vector.compose-3d` — Companion Processing Tool**
- Draft PR: [#9](https://github.com/WUHAO19831214/physics-software-sensors/pull/9)
- Branch: `agent/tool-vector-compose-3d`
- Tested implementation SHA: `2759ccef506c1a5d4afe403bfddbcaa3c2a538cf`
- Sensors: **7**; Companion Tools: **1**
- Baseline Release: immutable `v0.6.0`; no new Release or registry publication

## 1–6. Source and historical decision

1. Source repository: `WUHAO19831214/ampere-force-visualizer-teacher-yanan`.
2. Current source SHA: `cb073e89d6d87129287030f1df08bd540504eb39`; inspected read-only and left clean.
3. Historical F1/F2/F3: **CONFIRMED**, first ROI IDs at `f3d93b3404d4246a4a0e4395070c2b7e67baea58`, first definitive 3D force implementation at `ac46ed58ed020c96e75d34d70759477ef898bbef`.
4. Meaning: three simultaneous scalar OCR values treated as the x/y/z orthogonal components of one resultant force at a common point; source UI also called them three orthogonal forces. They were not arbitrary non-orthogonal vectors or one hardware SDK's three-axis record.
5. Transition: `ed33d00774cd7eedf1ff4c3bd9a2cf9225410cf5` customized the application for Yan'an, changed default ROIs to Fy/Fz, retained F2/F3 aliases and set Fx to zero. The y-z apparatus-plane interpretation is supported by coordinate labels/code but is an inference; no richer commit body states the reason.
6. xyz conclusion: historical F1/F2/F3-to-x/y/z behavior is source-confirmed. Current main is instead `{Fx=0 constrained, Fy/Fz observed}`. Stale F1/F2/F3 overview text in the current README is not treated as current runtime truth.

Full evidence: [Yan'an history](../docs/research/yanan-vector-reconstruction-history.md) and [SOURCE](../processing/vector.compose-3d/SOURCE.md).

## 7–14. Architecture and API

7. Final ID: `vector.compose-3d`.
8. It is not a Sensor because it makes no direct observation: `screen.capture` observes pixels, `ocr.number` derives scalars, and this module performs downstream measurement processing.
9. Public core: `Vector3Assembler`, `composeVector3`, `Vector3Measurement`, `applyCoordinateTransform`, `createVector3RenderModel`, and `componentFromNumberOcrEvent` under `packages/typescript/src/processing/vector3/`.
10. Component source is explicit: `observed | derived | constrained | default | missing`. Missing yields an incomplete result; constrained zero is never reported as OCR-observed.
11. Each component may carry `timestampMs`; `maxComponentSkewMs` defaults to 150 ms and excessive spread emits `component-time-skew`.
12. Vector math uses caller coordinates. The opt-in Yan'an transform maps classroom `(x,y,z)` to scene `(-x,z,y)` and is tested separately.
13. The optional adapter emits renderer-neutral axes, component arrows and resultant arrow. It does not copy or depend on the large teacher Three.js UI.
14. Recorded `NumberOCRSensor` events compose through `componentFromNumberOcrEvent`; parse failure becomes `missing`, never a mock number.

## 15–19. Evidence and public surface

15. Golden fixture pins historical/current source commits and covers +x, +y, +z, xy, yz, xyz, negative, zero, historical F1/F2/F3 and current Fy/Fz+Fx=0. Magnitude, direction and scene mapping tolerance is `1e-12`.
16. Tests: Python **87/87**; TypeScript **30/30** full and **27/27** offline; new Vector/OCR tests **12/12**; existing composition matrix **5/5**; i18n and repository structure pass after the containing handoff commit.
17. Demo: `examples/web-vector-compose-3d/`, with manual input and recorded Fy/Fz OCR modes. It imports the built core and uses a minimal canvas projection.
18. EN/ZH/JA: one Tool Page × 3, Tool Catalog × 3, 54-entry terminology authority, parity validation extended to Tool manifests/pages.
19. Tool Catalog: `docs/tool-catalog.md`, `.zh-CN.md`, `.ja.md`; machine manifest: `processing/vector.compose-3d/tool.json`.

## 20–22. Repository and review boundary

20. Sensor count remains exactly **7**. Project status records **1 Companion Tool**, experimental `0.1.0`, unreleased.
21. Draft PR [#9](https://github.com/WUHAO19831214/physics-software-sensors/pull/9) remains unmerged.
22. Blockers/gaps: source repository has no explicit license, so implementation is a clean rewrite and no code/assets were copied; no downstream real-time Yan'an integration; no controlled physical validation; no full Three.js renderer; cross-browser performance is not measured. None blocks review of the experimental core.

## Immutable and source state

- Source repository main/worktree: unchanged at `cb073e89d6d87129287030f1df08bd540504eb39`.
- Library remote main: unchanged at `0c5d484d2b6d85c8e28308c2b7338bbc2a282e6b` when the Draft PR was created.
- `v0.6.0` tag object: unchanged at `c067c6c0e8196a284d6cba618a9fac5923bce8f7`.
- No `v0.7.0`, PyPI, npm, merge, or downstream integration action was performed.

Recommended next action: review the Vector3 handoff and decide whether Draft PR #9 should enter the long-term tool library. Do not merge automatically.
