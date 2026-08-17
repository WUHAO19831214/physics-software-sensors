# Source compatibility and micro-benchmark plan

Current executable evidence is deterministic source compatibility, not controlled physical validation.

| Check | Dataset | Acceptance | Current result |
| --- | --- | --- | --- |
| Historical component formula | pinned F1/F2/F3 golden case | magnitude and mapping error ≤ `1e-12` | PASS |
| Current Yan'an formula | pinned Fx=0, Fy/Fz case | magnitude and mapping error ≤ `1e-12` | PASS |
| OCR composition | recorded Number OCR results | preserve values/quality; no mock on failure | PASS |
| Time synchronization | deterministic timestamps | flag above configured skew | PASS |

Future benchmark work may record operations/second and allocation behavior across supported browsers and Node.js versions. Those metrics are not yet measured and are not necessary to claim the current experimental, deterministic core behavior.
