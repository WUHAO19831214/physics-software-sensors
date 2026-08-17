# Rollback record

The downstream adapter defaults to `SPOT_SENSOR_BACKEND=legacy`. During validation the modes were executed in this order: `legacy`, `library`, `compare`, then `legacy` again. All returned success. The structured comparison does not select or alter browser experiment output.

Rollback consists of either leaving the flag unset or setting:

```bash
SPOT_SENSOR_BACKEND=legacy python integration/spot_sensor/runner.py
```

The optional Python environment can then be removed without touching the application. `app.js`, `index.html`, camera permission, calibration, sweep, table and chart paths do not import the package. A local static-server request and `node --check app.js` passed after integration, demonstrating that the original app remains independently startable.

No legacy implementation was deleted. Removing it, changing the live browser backend, or adding a browser-to-Python service requires a separate reviewed migration decision.
