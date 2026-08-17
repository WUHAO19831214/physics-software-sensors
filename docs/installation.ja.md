# インストール

[English](installation.md) | [简体中文](installation.zh-CN.md) | **日本語**

<!-- section:prerequisites -->
## 前提条件

- Python package は Python 3.11+。
- TypeScript package は Node.js 18+。
- [`v0.6.0` Experimental](https://github.com/WUHAO19831214/physics-software-sensors/releases/tag/v0.6.0) から取得した artifact。registry package は公開していません。

<!-- section:python -->
## Python

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install ./physics_software_sensors-0.5.0-py3-none-any.whl
```

必要な extra だけをインストールします。

```bash
python -m pip install './physics_software_sensors-0.5.0-py3-none-any.whl[color-marker]'
python -m pip install './physics_software_sensors-0.5.0-py3-none-any.whl[camera-opencv]'
python -m pip install './physics_software_sensors-0.5.0-py3-none-any.whl[classical-trackers]'
python -m pip install './physics_software_sensors-0.5.0-py3-none-any.whl[yolo-recorded]'
```

`yolo-runtime` はライセンス確認後に任意の Ultralytics/`lap` を導入する extra です。モデルの提供・選択・自動取得は行いません。呼び出し側が審査済みローカル `ModelArtifact` の path、SHA-256、license status を指定します。

<!-- section:typescript -->
## TypeScript

```bash
npm install ./physics-software-sensors-core-0.3.0.tgz
```

```ts
import { ScreenCaptureSource, BrowserScreenBackend, NumberOCRSensor } from '@physics-software-sensors/core';
```

ブラウザ取得には secure context、ユーザー操作、明示的許可が必要です。実 Tesseract.js は言語データを取得・cache する場合がありますが、traineddata は tgz に含まれません。

<!-- section:verification -->
## 入手元の確認

インストール前に SHA-256 を確認してください。この release では `pip install physics-software-sensors` と `npm install @physics-software-sensors/core` を registry command として実行しません。[Downloading Sensors](downloading-sensors.ja.md) を参照してください。
