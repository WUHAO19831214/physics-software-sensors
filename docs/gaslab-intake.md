# GasLab and Core support intake

**English** | [简体中文](gaslab-intake.zh-CN.md) | [日本語](gaslab-intake.ja.md)

<!-- section:decision -->
## Decision

ACCEPT as experimental Core support utilities and a headless gas teaching-model domain package (MAINTENANCE). DEFER promotion to a named Sensor/Companion Tool: simulation is not direct observation, and a model package does not satisfy measurement-processing intake merely by resembling FringeLab. Catalog remains 9 Sensors + 4 Tools = 13 capabilities. Core source becomes unreleased 0.3.1; gaslab is unreleased 0.1.0. No registry or Release publication.

<!-- section:provenance -->
## Provenance

[Fixed source paths and MIT review](../packages/gaslab/SOURCE.md). Original PSS branches: `feat/core-ocr-fit-stabilizer` at `6262fd87a032f2c665a476653f226496688b85f9`, followed by `feat/gaslab-core` at `5fbade46aa6a819e56c5cb360c87ab0bf9ca7eb5`. The review branch retains both commits; original branches are preserved.

<!-- section:review -->
## Review findings and changes

Original tests passed (Core 41, gaslab 17), but did not cover signed Celsius parsing, mixed-unit noise, nonfinite readings, constant-series origin R², full elapsed time, snapshot aliasing or capsule initialization. Reproduced -20 ℃ becoming +20 ℃; NaN classified valid; step(1) advancing only 0.1 seconds; old snapshots mutating; 112/1000 capsule samples outside original boundary. Fixes preserve signs and converted/source units, require explicit unitless ROI fallback, reject invalid numeric/clock inputs, report poor origin-fit R² honestly, honor full durations, isolate snapshots/configuration, restart seeded RNG, sample valid geometry and reflect independent corner/rim contacts. Replay has validated copied data, recorded epochs, segmented input timing and pause. Display pressure is explicitly separated from SI pressure.

<!-- section:validation -->
## Validation

[Review evidence](../benchmarks/results/gaslab-intake.json) · [runnable headless replay](../examples/headless-gaslab/README.md). Baseline SourceSensor/ProcessorSensor contracts and immutable v0.6.0 downloads are unchanged. Pure synthetic tests and local consumer builds do not establish hardware precision. GasLab's capsule is a one-hemisphere cylinder with a flat top; wall projection loses overshoot. No molecule-molecule interactions or moving piston are implemented.

<!-- section:consumer -->
## Downstream state

[Charles-law local reuse](../integrations/charles-law-gaslab/README.md). The source checkout's test/build pass and package imports are verified, but its changes are uncommitted. It delegates sampling/scaling and Core helpers; the rendered particle engines and replay UI still live in that application. It is not an E5 merged engine/driver integration. Updated tarballs are validated in a temporary copy, leaving that checkout's dependencies/changes intact.

<!-- section:rollback -->
## Rollback and remaining work

Use prior package/source commits or remove the new package. Before catalog promotion: identify recurring measured inputs, provenance/failure contract and formal Tool/Sensor intake; simulation alone cannot be promoted. Before remote downstream acceptance: review and commit the local app adaptation with fixed package hashes. The unrelated draft PR #11 remains a separate navigation task.
