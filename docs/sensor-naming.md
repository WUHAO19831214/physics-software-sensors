# Sensor ID naming

Use stable lowercase IDs with exactly one domain/capability boundary:

```text
<domain>.<capability>
```

Existing IDs establish the vocabulary: `camera.capture`, `screen.capture`, `ocr.number`, `tracker.color-marker`, `tracker.spot-centroid`, `tracker.template`, `tracker.yolo`.

Rules:

- ASCII lowercase letters/digits; words inside a segment use `-`.
- The ID describes the direct software observation/capability, not an uncalibrated downstream physical claim.
- Prefer an existing domain. A new domain requires an intake rationale.
- Do not include project names, UI names, implementation backends, versions or brands unless the capability is intrinsically that algorithm family (the existing `tracker.yolo` is such a public exception).
- Once an ID appears in a public release, do not rename it casually. A rename requires an alias, deprecation period, migration note and versioned contract decision.
- A proposal reserves no ID until its intake decision is `ACCEPT`.

The scaffold generator validates syntax but cannot decide whether an ID is scientifically or architecturally appropriate.
