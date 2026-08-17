# Add a Sensor — reusable Codex prompt

Use this template for a future task; it is not an instruction to add a Sensor now.

```text
Repository: WUHAO19831214/physics-software-sensors

SOURCE_REPOSITORY: <owner/repository or URL>
SOURCE_COMMIT: <full commit SHA, or NOT_PROVIDED>
CAPABILITY: <what the mature project-local capability does>
EXPECTED_SENSOR_ID: <candidate ID or UNSURE>
PHYSICS_USE: <real experiment use and direct observation>

Follow docs/sensor-intake.md and docs/sensor-naming.md.

1. If SOURCE_COMMIT is NOT_PROVIDED, fetch the source repository and pin the current reviewed commit before any extraction.
2. Produce a SENSOR_PROPOSAL with file/symbol provenance, observation-vs-derived-quantity boundary, dependencies, license state and existing evidence.
3. Decide ACCEPT, DEFER or REJECT with reasons. Do not scaffold on DEFER/REJECT.
4. On ACCEPT, generate a truthful scaffold; do not invent source SHA, benchmark, demo, maturity or implementation.
5. Extract through an adapter without modifying the source project; add deterministic and source-golden tests, benchmark, EN/ZH-CN/JA pages, example, bundle and clean-install evidence.
6. Keep the old downstream path and rollback until comparison succeeds. Update Agent Handoff with sensor_intake.
```
