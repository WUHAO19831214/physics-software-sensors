# Physics Software Sensors — Agent Handoff

## Current state

- Status: **READY_FOR_REVIEW**
- Phase: **5 — Downstream Reuse Validation**
- Library Draft PR: [#8](https://github.com/WUHAO19831214/physics-software-sensors/pull/8)
- Downstream Draft PR: [spot-vibration #1](https://github.com/WUHAO19831214/spot-vibration-tracking-system-20260508-171952/pull/1)
- Library branch: `agent/phase5-downstream-reuse`
- Tested implementation SHA: `d9ea8f91bf2cb35c4eaf39ffd719ffe0ed6a3a69`
- No Sensor algorithm/API change, source-main rewrite, maturity promotion, `v0.7.0` release, PyPI/npm publication or `v0.6.0` mutation

## Phase 4B closure

PR [#7](https://github.com/WUHAO19831214/physics-software-sensors/pull/7) passed the final repository, i18n, Python, TypeScript, composition, package and bundle checks, was moved out of Draft, and was squash-merged as `09e421755af50430af5753cbadf25e21cce9cd6c`. Post-merge repository/i18n smoke passed after replacing the stale Phase 4B handoff on this Phase 5 branch.

## Selected pilot and runtime decision

The pilot is `WUHAO19831214/spot-vibration-tracking-system-20260508-171952` with `tracker.spot-centroid`. Its fixed historical base and remote `main` at audit were both `7f0d91cc73afafaecc54acc46b2b9d69375d994a`; no silent rebase occurred.

The project is browser JavaScript while the released Sensor is Python. A realtime process bridge would change deployment, permissions and timing, so the low-risk integration is an offline project-side replay adapter. The downstream browser app and `app.js::trackRedSpot/rgbToHsv` remain unchanged. Integration commit `6d2a1b8c79bd6b0400c596db9b989235f3637ba3` exists only on `agent/physics-sensors-spot-integration` and Draft PR #1.

## Pinned dependency and modes

The downstream requirement uses the public `v0.6.0` Release wheel, package `physics-software-sensors==0.5.0`, Sensor `tracker.spot-centroid@0.4.0`, and artifact SHA-256 `191258d71e036d5f7b9b2ef3b43c2a70d6a6058af984ce65ea39ddb23db573c9`. No editable path, local workspace package or moving `main` is used.

`SPOT_SENSOR_BACKEND` accepts `legacy`, `library` and `compare`, defaulting to `legacy`. Compare mode sends identical in-memory BGR pixels to both implementations and writes a per-frame JSON record containing legacy output, library output and deltas. It does not change browser experiment output.

## Comparison and downstream regression

Normal, horizontal movement, vertical movement, lower intensity, blank/lost, ROI edge and overexposure cases passed 7/7. Detection/lost agreed for every frame. The maximum direct numeric delta was `7.105427357601002e-15`, below the fixed `1e-9 px` tolerance; blank output contained no stale centroid.

For the project-owned `normal → vertical → horizontal` sequence and fixture scale `0.02 cm/px`, legacy and library paths both produced `28 px` and `0.56 cm`. This is a regression of downstream `max(y)-min(y)` and calibration multiplication, not a new Sensor measurement or mechanical-amplitude accuracy claim.

## Smoke and rollback

The public wheel installed in a clean Python 3.12 environment. Downstream tests passed 3/3, all three modes exited successfully, `node --check app.js` passed, and a local static HTTP request loaded the existing app. Camera permission and physical hardware were not exercised.

Validation executed `legacy → library → compare → legacy`. Leaving the flag unset or selecting `legacy` rolls back; the optional Python environment can be removed because the browser app imports none of it. The legacy implementation was not deleted.

## Evidence decision

The seven E5 conditions are satisfied: real downstream repository reference, pinned public dependency, feature flag, same-input old/new comparison, downstream regression, tested rollback and integration documentation. Therefore only `tracker.spot-centroid` advances to **E5**. It remains **experimental** because the replay fixtures are synthetic and no E4 real optical/device, controlled movement, repeatability or uncertainty evidence exists. The detailed record is [`integrations/spot-vibration`](../integrations/spot-vibration/README.md).

## Verification

- Repository validation: **PASS** — 42 JSON files, 7 trilingual Sensor Pages, local links and evidence registry.
- i18n: **PASS** — 7 public document sets, 7 × 3 Sensor Pages, 46 terminology entries.
- Python: **84 passed, 0 failed**, including two downstream-record consistency tests and composition 5/5.
- TypeScript: **15/15 offline**, **18/18 full**.
- Package build: wheel **1/1**, TypeScript tgz **1/1**.
- Sensor Bundle build: **7/7**.
- Downstream: clean public-wheel install, integration **3/3**, all modes, structured comparison, static app smoke and rollback **PASS**.

## Immutable release and repository boundaries

`v0.6.0` remains the same annotated tag object `c067c6c0e8196a284d6cba618a9fac5923bce8f7`, peeling to `1a4a3fe45c1eaafe06c7e053644188b7abba8c62`, with the same 11 Release attachments. Its manifest correctly retains publication-time E1–E3 evidence; E5 is a post-release integration record. No `v0.7.0` was created.

The other four historical source repositories still have the fixed remote-main SHAs recorded in Phase 4B. The Spot project historical `main` is also unchanged; only its dedicated Draft integration branch is intentionally modified.

## Blockers and recommendation

There is no blocker for review. Realtime browser/library operation and E4 physical validation are deliberately deferred, not hidden. Review both Draft PRs together. If accepted, next plan a controlled E4 optical/device study and a second independent downstream pilot before considering `validated`/`stable` maturity or deciding on `v0.7.0`.
