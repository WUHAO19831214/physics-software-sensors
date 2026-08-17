# Installation

**English** | [简体中文](installation.zh-CN.md) | [日本語](installation.ja.md)

<!-- section:prerequisites -->
## Prerequisites

- Python 3.11+ for the Python package.
- Node.js 18+ for the TypeScript package.
- Downloaded artifacts from [`v0.6.0` Experimental](https://github.com/WUHAO19831214/physics-software-sensors/releases/tag/v0.6.0); no registry package is published.

<!-- section:python -->
## Python

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install ./physics_software_sensors-0.5.0-py3-none-any.whl
```

Install only required extras:

```bash
python -m pip install './physics_software_sensors-0.5.0-py3-none-any.whl[color-marker]'
python -m pip install './physics_software_sensors-0.5.0-py3-none-any.whl[camera-opencv]'
python -m pip install './physics_software_sensors-0.5.0-py3-none-any.whl[classical-trackers]'
python -m pip install './physics_software_sensors-0.5.0-py3-none-any.whl[yolo-recorded]'
```

`yolo-runtime` installs optional Ultralytics/`lap` only after a licensing review. It does not supply, choose or download a model. The caller must provide a reviewed local `ModelArtifact` path, SHA-256 and license status.

<!-- section:typescript -->
## TypeScript

```bash
npm install ./physics-software-sensors-core-0.3.0.tgz
```

```ts
import { ScreenCaptureSource, BrowserScreenBackend, NumberOCRSensor } from '@physics-software-sensors/core';
```

Browser capture requires a secure context, a user gesture and explicit user permission. Real Tesseract.js may retrieve/cache language data; traineddata is not bundled.

<!-- section:verification -->
## Verify the source

Validate SHA-256 before installation. Do not run `pip install physics-software-sensors` or `npm install @physics-software-sensors/core` as registry commands for this release. See [Downloading Sensors](downloading-sensors.md).
