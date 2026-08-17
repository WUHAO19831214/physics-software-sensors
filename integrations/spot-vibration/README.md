# Spot vibration downstream reuse

This record demonstrates the first pinned downstream reuse of `tracker.spot-centroid`. The pilot is [`WUHAO19831214/spot-vibration-tracking-system-20260508-171952`](https://github.com/WUHAO19831214/spot-vibration-tracking-system-20260508-171952), based on its fixed historical source commit `7f0d91cc73afafaecc54acc46b2b9d69375d994a` and implemented in downstream Draft PR [#1](https://github.com/WUHAO19831214/spot-vibration-tracking-system-20260508-171952/pull/1).

```text
deterministic downstream BGR frame
                ↓
        feature-flagged adapter
         ↙       ↓        ↘
    legacy    library    compare
         ↘       ↓        ↙
       centroid pixel contract
                ↓
 downstream y-range and cm scaling
```

The adapter installs the public `v0.6.0` wheel by immutable Release URL and SHA-256. It defaults to `legacy`; `library` runs `SpotCentroidSensor`; `compare` runs both on the same in-memory pixels and writes a structured result. The browser application, live camera loop and legacy `app.js` implementation were not modified.

All seven direct-observation cases agreed within `1e-9 px`; the maximum floating-point delta was `7.105427357601002e-15`. Both paths derived `28 px` and `0.56 cm` for the project-owned three-frame sequence. Clean installation, all three modes, three downstream tests, static app startup, JavaScript syntax and rollback to legacy passed.

This satisfies E5 downstream-reuse evidence for this Sensor while maturity remains `experimental`. The replay fixtures are synthetic and there is still no E4 real optical/device validation, controlled mechanical displacement, repeatability or uncertainty evidence.

- [Machine record](integration.json)
- [Comparison summary](comparison-summary.md)
- [Rollback record](rollback.md)
