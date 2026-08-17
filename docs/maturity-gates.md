# Maturity gates

Maturity is a release decision layered on top of evidence. Passing a higher evidence level does not bypass these gates.

| Gate | Contract-only | Experimental | Validated | Stable |
| --- | --- | --- | --- | --- |
| Sensor Page, manifest, provenance | required | required | required | required |
| Schema-valid implementation | absent/optional | required | required | required |
| Deterministic success/failure tests | not required | required | required | required |
| Fixed-source compatibility | planned | applicable sensors required or explicit exception | required | required |
| Real runtime | not required | may be pending and disclosed | required where applicable | required |
| Real device/lab dataset (E4) | not required | pending | required | required |
| Metrics/limits/compatibility published | planned | partial with `not measured` | required | required |
| Dependency and artifact license review | planned | known risks disclosed | resolved for supported path | resolved |
| Downstream pinned integration + rollback (E5) | not required | not required | recommended | required |
| Public API/versioning/upgrade record | draft | experimental | compatibility controlled | stable SemVer commitment |

## Promotion policy

- `experimental → validated` requires an explicit review record; README completeness or test count alone is insufficient.
- `validated → stable` requires at least one E5 downstream integration, rollback evidence, clean install artifacts and resolved supported-path licensing.
- A regression, dependency/license change or lost reproducibility can demote maturity without changing the SensorEvent contract.
- Contract and implementation versions remain separate.

Current decision: all seven implementations stay `experimental`. `tracker.spot-centroid` has E5 offline downstream-reuse evidence, but still lacks E4 real optical/device evidence and other applicable validation gates. No other Sensor has E5.
