# Physics Software Sensors — Vector3 + Homepage Showcase Handoff

## Review state

- Status: **READY_FOR_REVIEW**
- Task: **NEW_REUSABLE_TOOL + HOMEPAGE_SHOWCASE**
- Draft PR: [#9](https://github.com/WUHAO19831214/physics-software-sensors/pull/9)
- Branch: `agent/tool-vector-compose-3d`
- Tested implementation/showcase SHA: `9b4c69cb851b5d7689b627f179a8d7322403391e`
- Sensors: **7**
- Companion Processing Tools: **1**
- Public capabilities: **8**
- Baseline Release: immutable `v0.6.0`; no merge or new publication

## Reusable Tool result

`vector.compose-3d` remains an experimental Companion Processing Tool, not a Sensor. Historical F1/F2/F3 is source-confirmed as orthogonal x/y/z scalar components of one resultant. Current Yan'an behavior remains `{Fx=0 constrained, Fy/Fz observed}`. The TypeScript core, time-skew/quality semantics, coordinate adapter, recorded OCR composition, 10-case source golden and clean-rewrite provenance are unchanged by this homepage work.

Source history: [research record](../docs/research/yanan-vector-reconstruction-history.md) · [SOURCE](../processing/vector.compose-3d/SOURCE.md).

## Homepage Showcase report

1. Sensor count: **7**, unchanged.
2. Companion Tool count: **1**, `vector.compose-3d`.
3. Homepage Sensor Catalog: **7/7** entries in EN/ZH/JA.
4. Homepage Companion Tool Catalog: **1/1** separate entry in EN/ZH/JA; it is not mixed into the Sensor table.
5. Sensor demo assets: **7/7** — camera, screen, OCR, color marker, spot centroid, template tracker and YOLO.
6. Vector Tool demo asset: **1/1** — [`processing/vector.compose-3d/assets/overview.png`](../processing/vector.compose-3d/assets/overview.png).
7. Reused assets: **7** existing reviewed Sensor assets.
8. Newly generated assets: **1**. It is an actual standalone browser screenshot in recorded Fy/Fz OCR mode, not a fabricated UI or copied source screenshot.
9. Broken homepage image/page links: **0**.
10. Homepage parity: **PASS** for English / 简体中文 / 日本語, with identical 7+1 structure and evidence boundaries.
11. Repository validation: **PASS**, including exact 8-image gallery and public capability counts.
12. Python: **89/89 PASS**.
13. TypeScript: **30/30 PASS**; offline count remains **27/27**.
14. Vector/OCR focused tests: **12/12 PASS**.
15. PR HEAD: resolved from `refs/heads/agent/tool-vector-compose-3d`; the final containing handoff commit is published after validation.
16. Blockers: **none**. Known gaps remain source-license absence (clean rewrite/no copied source assets), no controlled physical validation, no downstream realtime Yan'an integration, and no full Three.js renderer.

## Gallery evidence

| Capability | Homepage asset | Evidence |
| --- | --- | --- |
| `camera.capture` | `sensors/camera.capture/assets/captured-frame.png` | deterministic synthetic camera replay |
| `screen.capture` | `sensors/screen.capture/assets/captured-screen-frame.png` | recorded synthetic shared-window pixels |
| `ocr.number` | `sensors/ocr.number/assets/overview.png` | synthetic pixels through actual Tesseract.js path |
| `tracker.color-marker` | `sensors/tracker.color-marker/assets/overview.png` | actual adapter on synthetic input |
| `tracker.spot-centroid` | `sensors/tracker.spot-centroid/assets/overview.png` | actual adapter replay on synthetic input |
| `tracker.template` | `sensors/tracker.template/assets/overview.png` | actual OpenCV CSRT synthetic replay |
| `tracker.yolo` | `sensors/tracker.yolo/assets/overview.png` | **recorded detector replay**, not real YOLO inference |
| `vector.compose-3d` | `processing/vector.compose-3d/assets/overview.png` | actual standalone runtime, recorded OCR mode |

The exhaustive 55-file scan is in [Demo Asset Inventory](../docs/demo-asset-inventory.md). The Vector screenshot is 1112×720 px, SHA-256 `8ddeafac006676affbb26828e72019a0a890cd2efbde67367d9f13daa757d9c2`.

## Immutable state

- Source repository `WUHAO19831214/ampere-force-visualizer-teacher-yanan`: unchanged at `cb073e89d6d87129287030f1df08bd540504eb39`.
- Library remote main: unchanged from maintenance baseline during this PR.
- `v0.6.0`: unchanged.
- Draft PR #9: remains Draft and unmerged.
- No `v0.7.0`, PyPI, npm, second Tool or downstream integration was created.

Recommended next action: inspect the Vector3 + Homepage Showcase handoff and decide whether Draft PR #9 can be merged. Do not merge automatically.
