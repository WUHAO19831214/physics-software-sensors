# Homepage Showcase Stabilization — 2026-08-17

## Scope

Post-release maintenance for Draft PR #9. No Sensor algorithm, source repository, `v0.6.0` tag or Release attachment was changed.

## Observed incident

The public GitHub page showed the old three-image `main` README while PR #9 remained unmerged. During inspection, GitHub also displayed `Cannot retrieve latest commit at this time`, and README images failed to render.

The repository checks showed:

- GitHub Contents API: `200` for the inspected image;
- repository blobs: present and non-empty;
- local Pillow decode: `PASS` for 8/8 detailed assets;
- `raw.githubusercontent.com`: `429 Too Many Requests` during the incident.

This combination is classified as an **external GitHub Raw/CDN delivery issue**, not a broken repository image. No valid demo asset was deleted or moved to third-party hosting.

## Stabilization

- `tools/build_capability_showcase.py` reads eight fixed, version-controlled demo assets without network access.
- It produces `docs/assets/capability-showcase.png` as a 2×4, 1200×1458 PNG.
- The three root READMEs load that single aggregate instead of eight independent detailed PNGs.
- EN/ZH-CN/JA Capability Showcase pages retain the eight detailed images.
- Eight text capability links remain available on each homepage when image delivery fails.
- Offline validation checks 7 Sensors, 1 Companion Tool, 8 public capabilities, one decodable aggregate and 8/8 valid text targets.

## Evidence boundary

The aggregate contains representative standalone, synthetic, recorded and replay demonstrations. Evidence level varies by capability. The YOLO tile is recorded detector replay, not real YOLO inference. The aggregate does not change maturity or establish real-device accuracy.

## Rollback

Revert the stabilization commit to restore the previous multi-image homepage. Do not delete the eight canonical detail assets; they remain inputs to the generator and evidence pages.
