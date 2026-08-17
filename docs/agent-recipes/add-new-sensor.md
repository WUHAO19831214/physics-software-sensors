# Agent recipe: add a new Sensor

The user only needs to provide the source repository/project, a capability description and why it is mature/useful. A source commit and candidate ID help but may be resolved during inventory.

## Required execution order

1. Inventory the fixed source repository; pin the current full commit if none was supplied.
2. Identify exact files, symbols, real physics use, direct observations and downstream derived quantities.
3. Complete [`templates/SENSOR_PROPOSAL.md`](../../templates/SENSOR_PROPOSAL.md).
4. Review reuse boundary, testability, dependencies/assets, privacy and license state.
5. Record `ACCEPT`, `DEFER` or `REJECT`; stop extraction for DEFER/REJECT.
6. For ACCEPT, run [`tools/new_sensor.py`](../../tools/new_sensor.py) in a clean branch, review every TODO and update the document map.
7. Extract a standalone adapter behind shared core without changing the source project.
8. Build contract/schema tests, deterministic fixtures, source golden/replay and applicable real runtime/device evidence.
9. Add example, truthful demo state, benchmark metrics, provenance, dependency/license review and three-language Sensor Pages.
10. Verify clean installation and Sensor Bundle; update changelog and Agent Handoff.

Never invent a source commit, benchmark result, model license, demo screenshot, confidence, physical calibration or maturity. Use `not measured` or `pending` and stop at the correct gate.

Reusable user prompt: [`templates/ADD_SENSOR_PROMPT.md`](../../templates/ADD_SENSOR_PROMPT.md).
