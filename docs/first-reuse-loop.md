# First Complete Reuse Loop

**English** | [简体中文](first-reuse-loop.zh-CN.md) | [日本語](first-reuse-loop.ja.md)

<!-- section:loop -->
## The loop

```text
Spot Vibration project
      ↓
trackRedSpot source behavior
      ↓
tracker.spot-centroid
      ↓
Physics Software Sensors v0.6.0
      ↓
public wheel
      ↓
merged Spot Vibration integration
      ↓
legacy/library comparison + rollback
      ↓
E5 downstream reuse demonstrated
```

<!-- section:meaning -->
## What it demonstrates

A capability used in a physics project was extracted with fixed provenance, packaged in a public Release, then consumed again by the source project through a pinned dependency and reversible adapter. The merged downstream path defaults to `legacy`; `library` and `compare` are explicit offline replay modes.

Historical source commit `7f0d91cc73afafaecc54acc46b2b9d69375d994a` identifies where the algorithm came from. Downstream merge commit `172429fae463274ee354e54d56400096c2c6d375` proves where the released library was reused. These are intentionally different facts.

<!-- section:boundary -->
## Scientific boundary

This is a **software reuse loop**, not physical metrology validation. Seven synthetic same-frame cases, downstream calculation regression and rollback passed. A real camera, controlled optical movement, exposure robustness, repeatability and uncertainty remain E4 gaps, so `tracker.spot-centroid` stays `experimental` despite E5 reuse evidence.

Detailed evidence: [Spot Vibration integration record](../integrations/spot-vibration/README.md).
