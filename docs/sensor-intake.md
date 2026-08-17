# Future Sensor Intake

**English** | [简体中文](sensor-intake.zh-CN.md) | [日本語](sensor-intake.ja.md)

<!-- section:purpose -->
## Purpose

This repeatable workflow moves a mature project-local sensing capability into this repository without breaking the source project or turning the library into a miscellaneous utilities collection.

<!-- section:qualification -->
## What is worth a Sensor?

A candidate should satisfy most of these: proven project use; clear boundary/input/output; separable from UI/business state; cross-project value; deterministic testing; complete provenance; legally distributable dependencies/assets; and a direct relationship to physics experiment sensing/observation.

UI layout, lesson buttons/text, charts, one-project stores/databases, device workflow orchestration, untestable helpers and unrelated utilities do not belong here.

<!-- section:decision -->
## Intake decision

- `ACCEPT`: boundary, reuse value, provenance and legal/test path are sufficient for extraction.
- `DEFER`: useful candidate, but source behavior, evidence, licensing or boundary is not ready.
- `REJECT`: not a Sensor, not reusable, not testable or inappropriate for this repository. Record the reason.

<!-- section:lifecycle -->
## Lifecycle

```text
candidate → accepted → contract-only → incubating → experimental
          → validated → stable → deprecated
```

`candidate/accepted` are intake states. `contract-only/incubating/...` map onto existing contract and maturity fields; this workflow does not change the current schema enum. Evidence E0–E5 remains separate.

<!-- section:workflow -->
## Standard workflow

1. Complete [`SENSOR_PROPOSAL.md`](../templates/SENSOR_PROPOSAL.md).
2. Pin repository, full commit SHA, paths/symbols, actual physics use and license state.
3. Decide `ACCEPT`, `DEFER` or `REJECT` with reasons.
4. For accepted work, run `tools/new_sensor.py` only to create a truthful TODO scaffold.
5. Extract an adapter behind shared core; leave source/UI/business behavior unchanged.
6. Add L0 contract, L1 deterministic fixture, L2 source golden/replay and applicable L3/L4 evidence without inventing results.
7. Add EN/ZH-CN/JA Sensor Pages, example, real demo asset or explicit pending state, benchmark, dependency/license audit, clean install, bundle and CHANGELOG.
8. Promote only through [Evidence and Maturity](evidence-and-maturity.md) gates; retain downstream rollback.

<!-- section:observation-boundary -->
## Direct observation vs derived physics

Every proposal must separate direct observation (`camera frame`, `screen pixels`, `OCR text`, `pixel centroid`, `bbox`) from downstream quantities (`displacement`, `velocity`, `force`, `amplitude`, `frequency`, `angle`). The derivation, units, calibration and uncertainty cannot be implied by the Sensor name.

<!-- section:required-deliverables -->
## Required before experimental

EN/ZH/JA Sensor Page; `sensor.json`; `SOURCE.md` and source commit; standalone adapter; deterministic and golden/replay tests; example; non-fabricated demo evidence; benchmark; evidence/maturity; dependency/license audit; clean install; Sensor Bundle; CHANGELOG. Missing items prevent a phase-complete claim.

<!-- section:handoff -->
## Agent handoff

During an intake, `.agent-handoff/latest.json` may include `sensor_intake` with candidate ID, decision/reason and source repository/SHA. When no intake is active it is `null` for backward compatibility.
