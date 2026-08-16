# Release-readiness dry runs

Phase 3D proves that distributable shapes can be built; it does **not** publish them.

## Package candidates

```bash
python tools/build_release_artifacts.py --output /tmp/physics-sensors-dist
```

The script builds exactly one Python wheel and one npm tgz, then writes `manifest.json` with package versions, file sizes, SHA-256 values, environment and tested Git SHA. It never invokes PyPI, npm publish or GitHub Release, and it does not install or download YOLO artifacts. The committed [`templates/RELEASE_MANIFEST.json`](../templates/RELEASE_MANIFEST.json) documents the stable record shape.

## Single-sensor documentation bundles

```bash
python tools/build_sensor_bundle.py --output /tmp/physics-sensor-bundles
```

The script creates seven deterministic zip files. Each contains a Sensor Page snapshot, provenance/assets, its small example, `INSTALL.md`, `DEPENDENCIES.json` and `BUNDLE.json`. It intentionally excludes package core implementation: consumers install the matching wheel/tgz instead of copying a single source file. Bundle and package outputs are ignored local build products and are not committed or published.

## Publication gate

Actual publication requires a reviewed release version, successful CI, clean-install verification, resolved supported-path dependency/license review, signed-off changelog and explicit maintainer approval. Those gates are not satisfied by this dry run alone.
