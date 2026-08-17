# Physics Software Sensors — Maintenance Handoff

## Baseline state

- Status: **MAINTENANCE_READY**
- Phase 5: **COMPLETE**
- Project state: **long-term maintenance**
- Baseline public Release: **v0.6.0 — Experimental**
- Sensors: **7**, all with experimental maturity
- Languages: **English / 简体中文 / 日本語**
- First E5 Sensor: **`tracker.spot-centroid`**

Phase 5 Library PR [#8](https://github.com/WUHAO19831214/physics-software-sensors/pull/8) was squash-merged as `2c3e91ed3c36f23b82c76cfd70076807adc1f891`. Downstream Spot Vibration PR [#1](https://github.com/WUHAO19831214/spot-vibration-tracking-system-20260508-171952/pull/1) was merged first as `172429fae463274ee354e54d56400096c2c6d375`.

## First complete reuse loop

The historical source SHA remains `7f0d91cc73afafaecc54acc46b2b9d69375d994a`; it identifies where `trackRedSpot` behavior came from. The downstream merge SHA is separate evidence that the public `v0.6.0` wheel was reused. The complete chain is documented in [First Complete Reuse Loop](../docs/first-reuse-loop.md) and the machine record in [`integrations/spot-vibration`](../integrations/spot-vibration/integration.json).

The downstream adapter pins package `0.5.0`, Sensor `tracker.spot-centroid@0.4.0` and wheel SHA-256 `191258d71e036d5f7b9b2ef3b43c2a70d6a6058af984ce65ea39ddb23db573c9`. `legacy`, `library` and `compare` passed on the integration branch and merged `main`; default and rollback remain `legacy`. Seven same-frame cases matched within `1e-9 px`, maximum delta was `7.105427357601002e-15`, and both downstream paths produced `28 px / 0.56 cm`.

This is E5 software reuse evidence, not E4 physical validation. The browser realtime path was not replaced, and real camera/optical movement, exposure robustness, repeatability and uncertainty remain open. `tracker.spot-centroid` therefore remains `experimental`.

## Final verification

- Repository validation: **PASS**, 43 JSON files.
- i18n: **PASS**, 8 public document sets, 7 × 3 Sensor Pages, 46 terms.
- Python: **86 passed**; composition **5/5**.
- TypeScript: **15/15 offline**, **18/18 full**.
- Package build: wheel **1/1**, tgz **1/1**.
- Sensor Bundles: **7/7**, trilingual pages **7/7**.
- Tracked model weights: **0**.
- Downstream merged `main`: integration **3/3**, all modes, rollback and static app smoke **PASS**; legacy browser files unchanged.

## Immutable release

`v0.6.0` is unchanged: annotated tag object `c067c6c0e8196a284d6cba618a9fac5923bce8f7` still peels to `1a4a3fe45c1eaafe06c7e053644188b7abba8c62`, with the same 11 attachments. No `v0.7.0`, PyPI or npm publication occurred.

## Maintenance workflow

Read [Current Project Status](../docs/project-status.md) and [Maintenance Guide](../docs/maintenance.md) before work. Future tasks use one of:

- `NEW_SENSOR` — formal Sensor Intake and scaffold;
- `SENSOR_UPGRADE` — old/new benchmark, golden, compatibility decision, upgrade record and version bump;
- `VALIDATION` — reproducible real-world evidence and matrix update;
- `DOWNSTREAM_INTEGRATION` — pinned dependency, feature flag, comparison and rollback;
- `RELEASE` — checklist, reproducible artifacts, licensing and immutable tag;
- `MAINTENANCE` — compatible fixes and documentation.

There is no automatic Phase 6. There is no blocker for maintenance. A future `v0.7.0` may package multilingual/intake/reuse documentation, but requires a separate release decision.
