# センサーカタログ

[English](sensor-catalog.md) | [简体中文](sensor-catalog.zh-CN.md) | **日本語**

<!-- section:catalog -->
## 利用可能な Sensor

ここでの状態は本 repository の実装を表し、過去のソースプロジェクトの成熟度を表すものではありません。

| Sensor | 用途 | 言語 | 成熟度 | エビデンス | Example | Download |
| --- | --- | --- | --- | --- | --- | --- |
| [`camera.capture`](../sensors/camera.capture/README.ja.md) | カメラフレームと取得メタデータ | Python | experimental | E1 | [実行](../examples/python-camera-capture/README.md) | [0.3.0](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/camera.capture-0.3.0.zip) |
| [`screen.capture`](../sensors/screen.capture/README.ja.md) | 許可済み画面・ウィンドウのピクセル | TypeScript | experimental | E1 | [実行](../examples/web-screen-capture/README.md) | [0.3.0](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/screen.capture-0.3.0.zip) |
| [`ocr.number`](../sensors/ocr.number/README.ja.md) | ROI の数値 OCR | TypeScript | experimental | E3 | [実行](../examples/web-number-ocr/README.md) | [0.2.0](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/ocr.number-0.2.0.zip) |
| [`tracker.color-marker`](../sensors/tracker.color-marker/README.ja.md) | マーカー位置とロスト状態 | Python | experimental | E2 | [実行](../examples/python-color-marker/README.md) | [0.2.0](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.color-marker-0.2.0.zip) |
| [`tracker.spot-centroid`](../sensors/tracker.spot-centroid/README.ja.md) | 光スポットの輝度加重重心 | Python | experimental | E2 | [実行](../examples/spot-centroid/README.md) | [0.4.0](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.spot-centroid-0.4.0.zip) |
| [`tracker.template`](../sensors/tracker.template/README.ja.md) | ROI 初期化型単一物体トラッカー | Python | experimental | E3 | [実行](../examples/python-template-tracker/README.md) | [0.4.0](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.template-0.4.0.zip) |
| [`tracker.yolo`](../sensors/tracker.yolo/README.ja.md) | 複数対象の検出・追跡 adapter | Python | experimental | E2 | [実行](../examples/python-yolo-tracker/README.md) | [0.5.0](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.yolo-0.5.0.zip) |

<!-- section:status -->
## 状態の意味

- `contract-only`: 契約と文書のみで、本 repository の実装はない。
- `experimental`: 独立 adapter とオフライン証拠はあるが、実機・下流検証が未完の場合がある。
- `validated`: 対象 runtime/device、指標、ライセンスの gate を通過している。
- `stable`: validated API に加え、下流での固定 version 再利用と rollback が検証済み。

エビデンスレベルと成熟度は別です。[エビデンスと成熟度](evidence-and-maturity.ja.md)を参照してください。7 Sensor はすべて experimental で E4/E5 はありません。実 YOLO inference は not measured で、モデル weight は配布しません。
