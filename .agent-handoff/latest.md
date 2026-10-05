# GasLab and Core support review handoff

Status: READY_FOR_REVIEW. Draft [PR #13](https://github.com/WUHAO19831214/physics-software-sensors/pull/13). Working branch: `codex/gaslab-intake`, based on the original remote `feat/gaslab-core` transfer (which includes `feat/core-ocr-fit-stabilizer`). Both original branches and commits are preserved. Main and live Pages are unchanged.

ACCEPT: experimental Core support APIs (unreleased 0.3.1) and headless gas teaching-model domain package (unreleased 0.1.0). Sensor/Companion Tool promotion is deferred; counts remain 9 + 4 = 13. Immutable v0.6.0 and third-party/source boundaries are preserved.

- [Intake and review](../docs/gaslab-intake.md) · [中文](../docs/gaslab-intake.zh-CN.md) · [日本語](../docs/gaslab-intake.ja.md)
- [GasLab API/model/time/units](../packages/gaslab/README.md)
- [Fixed provenance](../packages/gaslab/SOURCE.md)
- [Runnable headless replay](../examples/headless-gaslab/README.md)
- [Machine verification evidence](../benchmarks/results/gaslab-intake.json)
- [Local consumer state and rollback](../integrations/charles-law-gaslab/README.md)

Validation: Core offline 50/50; gaslab 24/24; Python 94/94; historical source formula/output comparison 921 checks at 1e-12 with explicit historical calibration; all five packed gaslab exports and NodeNext types without DOM; original consumer and reviewed-tarball temporary copy each pass 7 verification groups and build. The consumer build retains browser-external/bundle-size warnings. The npm default cache has some root-owned entries; verification uses a worktree-local cache without changing system ownership.

Review fixes cover signed OCR/unit/noise failures, nonfinite/stale readings, origin-fit R², full simulation time, independent snapshots, seeded reset, valid capsule initialization, independent wall contacts and coherent replay/pause. Synthetic SI pressure is a coarse sanity check, not device validation. Wall projection loses overshoot. Molecule interactions and moving piston are not implemented.

The source app's uncommitted adapter uses sampling/scaling and Core helpers; its full rendered engines/replay UI remain local. Do not claim E5 or remotely merged downstream completion. Next: review this PR, then separately commit/pin the downstream adaptation. Older draft PR #11 is outside this handoff.
