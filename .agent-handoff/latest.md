# Physics Software Sensors — Agent Handoff

## Current state

- Status: **READY_FOR_REVIEW**
- Phase: **4B — Multilingual Docs & Sensor Intake**
- Draft PR: [#7](https://github.com/WUHAO19831214/physics-software-sensors/pull/7), remains Draft and unmerged
- Branch: `agent/phase4b-i18n-sensor-intake`
- Tested implementation SHA: `8d671722535440e1f6f0c3f9dc85689f0e00ef6b`
- Languages: English / 简体中文 / 日本語
- No eighth Sensor, algorithm change, source-project change, maturity promotion or registry publication

## Multilingual public documentation

| Surface | Coverage |
| --- | ---: |
| Root README | 3 / 3 |
| Sensor Catalog | 3 / 3 |
| Seven Sensor Pages | 7 × 3 = 21 |
| Installation | 3 / 3 |
| Downloading Sensors | 3 / 3 |
| Getting Started | 3 / 3 |
| Evidence & Maturity | 3 / 3 |
| Sensor Intake | 3 / 3 |

English is the default prose language. Machine facts remain single-source in manifests, benchmark registry, release manifest and [`terminology.json`](../docs/i18n/terminology.json). [`document-map.json`](../docs/i18n/document-map.json) records the seven Tier A document sets and seven Sensor sets. All Sensor pages have the same 16 section markers.

The glossary has **46** entries. Sensitive decisions include `Software Sensor` / 软件传感器 / ソフトウェアセンサー; `FramePacket` and `SensorEvent` remain API identifiers; Japanese Spot Centroid is 光スポット重心; `tracker.template` is テンプレート／単一物体トラッカー and explicitly not static template matching.

## i18n validation

`python3 tools/validate_i18n.py` checks file/language navigation, section order, Sensor ID, implementation version, experimental maturity, E-level, v0.6.0 link and glossary structure. Result: **PASS**, 7 public document sets, 7 Sensor Pages × 3, 46 terms, 0 parity errors. The repository validator now includes this check.

## Future Sensor intake

- Workflow and ACCEPT/DEFER/REJECT: [`docs/sensor-intake.md`](../docs/sensor-intake.md)
- Stable ID rules and alias/deprecation boundary: [`docs/sensor-naming.md`](../docs/sensor-naming.md)
- Proposal: [`templates/SENSOR_PROPOSAL.md`](../templates/SENSOR_PROPOSAL.md)
- Generator: [`tools/new_sensor.py`](../tools/new_sensor.py)
- Agent recipe: [`docs/agent-recipes/add-new-sensor.md`](../docs/agent-recipes/add-new-sensor.md)
- Reusable prompt: [`templates/ADD_SENSOR_PROMPT.md`](../templates/ADD_SENSOR_PROMPT.md)

The generator accepts ID/name/language/category, refuses invalid IDs and overwrite, creates EN/ZH/JA pages plus manifest/SOURCE/CHANGELOG/assets/benchmarks/examples/implementation TODO, and updates the document map. Its default output is explicitly `contract-only` / manifest `planned`, E0, source/license/provenance pending. It does not invent a source SHA, benchmark, demo or implementation. Temporary generation and no-write dry-run both passed; no eighth formal Sensor was created.

## Verification at tested SHA

- Repository validation: **PASS** — 41 JSON files, 7 trilingual Sensor Pages, i18n parity and local links.
- Python: **82 passed, 0 failed** (includes composition 5/5 and 7 new i18n/intake/scaffold tests).
- TypeScript: **15/15 offline**, **18/18 full**, including real Tesseract.js synthetic-pixel integration.
- Package build: wheel **1/1**, tgz **1/1**.
- Sensor Bundle dry build: **7/7**; every bundle contains EN/ZH-CN/JA Sensor Pages.
- Tracked `.pt`/`.onnx`/`.engine`: **0**.
- Five fixed source commit URLs resolve exactly; no source repository was modified.

## Immutable release and boundaries

`v0.6.0` remains unchanged. Annotated tag object `c067c6c0e8196a284d6cba618a9fac5923bce8f7` still peels to `1a4a3fe45c1eaafe06c7e053644188b7abba8c62`; Release attachments were not replaced. All seven Sensors remain experimental with E1–E3 only. There is no E4/E5 evidence, PyPI/npm publication or Phase 5 integration. GitHub Actions remains disabled because the credential lacks `workflow` scope.

## Recommended next action

Independently review Phase 4B and keep PR #7 Draft. After review and an explicit merge decision, plan Phase 5 downstream reuse validation with pinned versions and rollback; do not start it automatically from this handoff.
