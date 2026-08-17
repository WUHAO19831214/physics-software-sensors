# Physics Software Sensors — Homepage Stabilization Handoff

## Review state

- Status: **MAINTENANCE_READY**
- Task: **HOMEPAGE_SHOWCASE_STABILIZATION**
- PR: [#9](https://github.com/WUHAO19831214/physics-software-sensors/pull/9) — **MERGED**
- Branch: `main`
- PR #9 merge SHA / tested public tree: `ff0906835d7f81cbb01e756931ed455f4b5c43e6`
- Sensors: **7**
- Companion Processing Tools: **1**
- Public capabilities: **8**
- Baseline Release: immutable `v0.6.0`

## Homepage stabilization

1. Eight canonical detail assets exist, are non-empty and decode locally: **8/8 PASS**.
2. The Vector screenshot was normalized from JPEG bytes to a real PNG without changing its displayed content. SHA-256: `acdf56337794a4513a4869b148beed6a77d15d294cd1e8171fae0a75e0fc7353`.
3. `tools/build_capability_showcase.py` creates one offline, reproducible 2×4 aggregate from those eight assets.
4. Aggregate: [`docs/assets/capability-showcase.png`](../docs/assets/capability-showcase.png), 1200×1458, 277904 bytes, SHA-256 `39fcb7a008388b925fdec3f5d4aafb86df2cef77f610aebef1de1fd275bd6a88`.
5. Each root README loads exactly one aggregate image and retains **8/8** text capability links.
6. The trilingual detail pages retain all eight individual demo images and evidence boundaries.
7. YOLO remains labeled **recorded detector replay**, not real YOLO inference.
8. No external image host or base64 embedding was introduced.

## GitHub delivery incident

During inspection, GitHub Contents API returned `200`, repository blobs existed, and local decode passed while `raw.githubusercontent.com` returned `429 Too Many Requests`. This is recorded as an **external GitHub Raw/CDN delivery issue**, not a broken repository image. The public status page reported GitHub operational, so the result is treated as regional/edge/IP delivery throttling. Valid assets were preserved.

## Verification

- Python: **90/90 PASS**.
- TypeScript: **30/30 PASS**.
- Vector/OCR focused: **12/12 PASS** from the package working directory.
- Composition: **5/5 PASS**.
- Homepage showcase tests: **3/3 PASS**.
- i18n: **PASS**, 10 public document sets, 7 Sensor Pages × 3, 1 Tool Page × 3, 54 terms.
- Showcase source/output decode: **8/8 + aggregate PASS**.
- Repository validation: **PASS** on merged `main`; rerun after the containing handoff commit.

## Immutable state

- Five historical source repositories: unchanged.
- Sensor algorithms and maturity: unchanged.
- `v0.6.0` tag and Release attachments: unchanged.
- No `v0.7.0`, PyPI, npm, new Sensor or second Tool was published.

## Merge result

- PR #9: **MERGED** at 2026-08-17T14:07:47Z.
- Squash merge SHA: `ff0906835d7f81cbb01e756931ed455f4b5c43e6`.
- Public `main`: contains 7 Sensors, 1 Companion Tool, the Capability Showcase and `vector.compose-3d`.
- `v0.6.0`: unchanged.

Next action: inspect the public `main` homepage and final showcase, then close the maintenance task.
