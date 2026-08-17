# Current Maintenance State

Machine-readable facts are in [`project-status.json`](project-status.json).

| Item | Current state |
| --- | --- |
| Project mode | Long-term maintenance |
| Baseline public Release | `v0.6.0` Experimental |
| Sensors | 7 |
| Companion Tools | 1 (`vector.compose-3d`, experimental, unreleased) |
| Public capabilities | 8 total; 7/7 Sensor + 1/1 Tool; one aggregate homepage image with 8/8 text links |
| Homepage stabilization | PR #9 merged at `ff0906835d7f81cbb01e756931ed455f4b5c43e6` |
| Multilingual public docs | GitHub Pages enabled from `main /docs`: <https://wuhao19831214.github.io/physics-software-sensors/> |
| Implemented adapters | 7, all `experimental` |
| Public languages | English / 简体中文 / 日本語 |
| Distribution | Python wheel, TypeScript tgz, 7 Sensor Bundles on GitHub Release |
| New Sensor workflow | Intake, proposal, scaffold and agent recipe ready |
| First downstream reuse | `tracker.spot-centroid`, E5, merged Spot Vibration integration |
| E4 real device/lab evidence | none |
| CI | Workflow templates exist; repository automation is not enabled |

`tracker.spot-centroid` reached E5 before E4. This is allowed because evidence records exercised dimensions rather than forcing a linear maturity ladder. It remains `experimental`.

Current work should enter through one of the maintenance tracks in [Maintenance Guide](maintenance.md). No Phase 6 is implied.
