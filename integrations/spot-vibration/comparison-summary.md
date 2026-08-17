# Spot centroid downstream comparison

## Fixed inputs

| Item | Fixed value |
| --- | --- |
| Historical downstream base | `7f0d91cc73afafaecc54acc46b2b9d69375d994a` |
| Downstream integration commit | `6d2a1b8c79bd6b0400c596db9b989235f3637ba3` |
| Public library release | `v0.6.0` |
| Wheel / Sensor | package `0.5.0` / `tracker.spot-centroid@0.4.0` |
| Wheel SHA-256 | `191258d71e036d5f7b9b2ef3b43c2a70d6a6058af984ce65ea39ddb23db573c9` |
| Structured downstream result | `integration/spot_sensor/results/comparison.json`, SHA-256 `229e1d86c23590752a34492f18f8c80845947335d45d29f0f6717f7edd301f6e` |

## Direct observations

The downstream `compare` mode passed the exact same BGR arrays to its fixed legacy reference and to the installed Release wheel. It compared detected/lost state, centroid `x/y`, radius and weight sum for normal, horizontal, vertical, intensity, blank, ROI-edge and overexposed cases.

| Metric | Result |
| --- | ---: |
| Cases matched | 7 / 7 |
| Detection/lost agreement | 7 / 7 |
| Pixel tolerance | `1e-9 px` |
| Maximum absolute numeric delta | `7.105427357601002e-15` |
| Blank stale-value check | explicit lost; `x/y = null` |

The tiny non-zero delta is ordinary floating-point summation-order noise; it is over five orders of magnitude below the fixed pixel tolerance. It is not rounded to zero in the evidence record.

## Downstream derived regression

The project, not the Sensor, owns `max(y)-min(y)` and `cm_per_pixel` conversion. For `normal → vertical → horizontal` at fixture ratio `0.02 cm/px`, both backends produced `28 px` and `0.56 cm`. This is regression evidence for project logic, not a claim that the fixture represents calibrated mechanical amplitude.

## Runtime boundary

The downstream application is browser JavaScript while the public Sensor is Python. A realtime browser/process bridge would change deployment and timing behavior, so this pilot intentionally validates the lower-risk offline replay boundary. The browser live-camera path stays legacy and was smoke-tested separately. Real camera frames, optics, controlled movement, repeatability and uncertainty remain not measured.
