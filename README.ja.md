# Physics Software Sensors — 物理実験ソフトウェアセンサーライブラリ

[English Docs](https://wuhao19831214.github.io/physics-software-sensors/) | [简体中文 Docs](https://wuhao19831214.github.io/physics-software-sensors/zh-CN/) | **日本語**

Markdown sources: [English](README.md) | [简体中文](README.zh-CN.md) | **日本語**

<!-- section:introduction -->
## これは何か？

**物理実験のための再利用可能なソフトウェアセンサー基盤です。** カメラフレーム、画面ピクセル、画像処理による観測を、来歴を追跡できる `FramePacket` と `SensorEvent` に統一し、将来の物理実験プロジェクトから再利用できるようにします。

Sensor の出力を処理する再利用可能な補助処理ツールも収録します。これらのツールを、新しい直接観測を行う Sensor とは扱いません。

新しい実験アプリケーションではなく、長期的に保守する基盤ライブラリです。ソースプロジェクトは変更せず、過去の実装と利用状況の事実源として維持します。

```text
物理実験プロジェクト
      ↓
再利用可能な成熟機能
      ↓
Physics Software Sensors
      ↓
将来の物理実験プロジェクト
```

成熟した機能を adapter として段階的に抽出し、固定 commit に対するテスト、文書化、ベンチマークを経て再利用します。ピクセル位置、OCR 文字列、信頼度、バウンディングボックスは直接観測であり、自動的に校正済み物理量になるわけではありません。

```text
物理的／ソフトウェア source
        ↓
Capture Sensor → FramePacket
        ↓
Processor Sensor → SensorEvent / スカラー測定値
        ↓
補助処理ツール
        ↓
物理実験アプリケーション
```

例：`screen.capture → ocr.number → vector.compose-3d → 3次元合成ベクトル`。最後の段階は既存のスカラー測定値を再構成するもので、新しい量を観測しません。

<!-- section:language-access -->
## 言語アクセス

repository の 3 言語コンテンツ完全性：**PASS**。English、简体中文、日本語の Markdown はいずれも完全な source document として維持されています。地域によって GitHub の file view が一時的に失敗しても、repository のトップから次の概要を確認できます。

- **English quick summary:** A reusable software sensing layer for physics experiments with 7 Software Sensors, 1 Companion Processing Tool and 8 public capabilities. It keeps direct image/screen/OCR/tracking observations separate from downstream physical quantities. Public `v0.6.0` contains seven Sensor Bundles, while `vector.compose-3d` is an unreleased experimental Tool. The trilingual documentation website is now served by GitHub Pages from `main /docs`.
- **简体中文快速说明：**这是面向物理实验的可复用软件传感器基础层，包含 7 个软件传感器、1 个配套处理工具和 8 项公开能力。它明确区分图像、屏幕、OCR、追踪的直接观测与后续物理量。公开 `v0.6.0` 包含 7 个 Sensor Bundle，`vector.compose-3d` 仍是未发布的 experimental 工具。三语静态阅读页现在由 GitHub Pages 从 `main /docs` 提供。

<!-- section:project-status -->
## Project status

**7 Software Sensor · 1 Companion Processing Tool · 再利用可能な公開 capability 全 8 項** · English / 简体中文 / 日本語

7 個の adapter と本ツールはすべて experimental です。公開 `v0.6.0` Release には 7 個の Sensor Bundle が含まれ、本ツールは未リリースです。最初の E5 downstream reuse は完了していますが、すべての Sensor が validated であるとは主張しません。

<!-- section:catalog -->
## センサーカタログ

| Sensor | 用途 | 言語 | 成熟度 | エビデンス | Example | Download |
| --- | --- | --- | --- | --- | --- | --- |
| [`camera.capture`](https://wuhao19831214.github.io/physics-software-sensors/ja/sensors/camera-capture/) | 時刻・バックエンド情報付きカメラフレーム | Python | experimental | E1 | [example](https://wuhao19831214.github.io/physics-software-sensors/ja/examples/camera-capture/) | [download](https://wuhao19831214.github.io/physics-software-sensors/ja/downloads/) |
| [`screen.capture`](https://wuhao19831214.github.io/physics-software-sensors/ja/sensors/screen-capture/) | ユーザー許可済みの画面ピクセル | TypeScript | experimental | E1 | [example](https://wuhao19831214.github.io/physics-software-sensors/ja/examples/screen-capture/) | [download](https://wuhao19831214.github.io/physics-software-sensors/ja/downloads/) |
| [`ocr.number`](https://wuhao19831214.github.io/physics-software-sensors/ja/sensors/number-ocr/) | ROI から数値を OCR | TypeScript | experimental | E3 | [example](https://wuhao19831214.github.io/physics-software-sensors/ja/examples/number-ocr/) | [download](https://wuhao19831214.github.io/physics-software-sensors/ja/downloads/) |
| [`tracker.color-marker`](https://wuhao19831214.github.io/physics-software-sensors/ja/sensors/color-marker/) | HSV・輪郭によるカラーマーカー追跡 | Python | experimental | E2 | [example](https://wuhao19831214.github.io/physics-software-sensors/ja/examples/color-marker/) | [download](https://wuhao19831214.github.io/physics-software-sensors/ja/downloads/) |
| [`tracker.spot-centroid`](https://wuhao19831214.github.io/physics-software-sensors/ja/sensors/spot-centroid/) | 光スポットの輝度加重重心 | Python | experimental | E5 | [example](https://wuhao19831214.github.io/physics-software-sensors/ja/examples/spot-centroid/) | [download](https://wuhao19831214.github.io/physics-software-sensors/ja/downloads/) |
| [`tracker.template`](https://wuhao19831214.github.io/physics-software-sensors/ja/sensors/template-tracker/) | ROI 初期化型の単一物体追跡 | Python | experimental | E3 | [example](https://wuhao19831214.github.io/physics-software-sensors/ja/examples/template-tracker/) | [download](https://wuhao19831214.github.io/physics-software-sensors/ja/downloads/) |
| [`tracker.yolo`](https://wuhao19831214.github.io/physics-software-sensors/ja/sensors/yolo-tracker/) | 複数対象の検出・追跡 adapter | Python | experimental | E2 | [example](https://wuhao19831214.github.io/physics-software-sensors/ja/examples/yolo-tracker/) | [download](https://wuhao19831214.github.io/physics-software-sensors/ja/downloads/) |

詳細は[センサーカタログ](docs/sensor-catalog.ja.md)を参照してください。エビデンスレベルと成熟度は別の概念です。

<!-- section:companion-tools -->
### Companion Processing Tools

| Tool | 用途 | 言語 | 状態 | Example | 文書 |
| --- | --- | --- | --- | --- | --- |
| [`vector.compose-3d`](https://wuhao19831214.github.io/physics-software-sensors/ja/tools/vector-compose-3d/) | スカラー成分から3次元ベクトルを合成・再構成 | TypeScript | experimental | [Web demo](https://wuhao19831214.github.io/physics-software-sensors/ja/examples/vector-compose-3d/) | [Tool Page](https://wuhao19831214.github.io/physics-software-sensors/ja/tools/vector-compose-3d/) |

詳細は [Companion Tool Catalog](docs/tool-catalog.ja.md)を参照してください。Companion Tool は拡張可能な測定処理 layer であり、Sensor 数には含めません。

<!-- section:quick-start -->
## クイックスタート

[Getting Started](docs/getting-started.ja.md) を読み、[`v0.6.0` Experimental Release](https://github.com/WUHAO19831214/physics-software-sensors/releases/tag/v0.6.0) から Python wheel または TypeScript tgz を選びます。PyPI と npm registry には公開していません。

```bash
python -m pip install './physics_software_sensors-0.5.0-py3-none-any.whl[classical-trackers]'
npm install ./physics-software-sensors-core-0.3.0.tgz
```

<!-- section:download -->
## ダウンロード

Release には Python wheel、TypeScript tgz、7 個の Sensor Bundle、`release-manifest.json`、`SHA256SUMS` が含まれます。Sensor Bundle は文書・example 用であり、共通 core を複製しません。[Downloading Sensors](docs/downloading-sensors.ja.md) と [Installation](docs/installation.ja.md) を参照してください。

<!-- section:capability-showcase -->
## Capability Showcase

[![Physics Software Sensors：7 個の Software Sensor と 1 個の Companion Processing Tool](docs/assets/capability-showcase.png)](https://wuhao19831214.github.io/physics-software-sensors/ja/capability-showcase/)

standalone、synthetic、replay の代表的なデモを 1 枚にまとめています。エビデンスレベルは capability ごとに異なり、YOLO tile は **recorded detector replay** であって実 YOLO inference ではありません。画像は補助表示であり、配信できない場合も下記のテキストリンクから全項目へ移動できます。

[Camera Capture](https://wuhao19831214.github.io/physics-software-sensors/ja/sensors/camera-capture/) · [Screen Capture](https://wuhao19831214.github.io/physics-software-sensors/ja/sensors/screen-capture/) · [Number OCR](https://wuhao19831214.github.io/physics-software-sensors/ja/sensors/number-ocr/) · [Color Marker](https://wuhao19831214.github.io/physics-software-sensors/ja/sensors/color-marker/) · [光スポット重心](https://wuhao19831214.github.io/physics-software-sensors/ja/sensors/spot-centroid/) · [Template / Single-object Tracker](https://wuhao19831214.github.io/physics-software-sensors/ja/sensors/template-tracker/) · [YOLO Tracker](https://wuhao19831214.github.io/physics-software-sensors/ja/sensors/yolo-tracker/) · [3次元ベクトル合成](https://wuhao19831214.github.io/physics-software-sensors/ja/tools/vector-compose-3d/)

範囲：**7/7 Software Sensor + 1/1 Companion Processing Tool = 再利用可能な公開 capability 8/8 項**。8 枚の詳細 demo とエビデンス境界は、3 言語の [Capability Showcase](docs/capability-showcase.ja.md) に掲載しています。

<!-- section:principles -->
## 基本原則

1. ソースプロジェクトを壊さず、暗黙に書き換えない。
2. repository、完全な commit SHA、path、symbol まで来歴を固定する。
3. 生の観測値を保存し、下流の導出値と区別する。
4. 時刻、座標、単位、信頼度、不確かさを明示する。
5. エビデンス、成熟度、ライセンス、モデル境界を保守的に記述する。

<!-- section:long-term-workflow -->
## 長期 workflow

```text
新しい物理実験 project
      ↓
再利用可能な成熟機能
      ↓
Sensor Intake
      ↓
Physics Software Sensors
      ↓
Experimental / Validation / Release
      ↓
将来の物理実験 project
```

今後の作業は [Sensor Intake](docs/sensor-intake.ja.md)、[Add New Sensor recipe](docs/agent-recipes/add-new-sensor.md)、または既存 Sensor の maintenance track から開始し、新しい Phase を自動的に作りません。最初の抽出から再利用までの完全な cycle は[最初の完全な再利用ループ](docs/first-reuse-loop.ja.md)に記録しています。

<!-- section:documentation -->
## ドキュメント

- [3 言語ドキュメントサイト](https://wuhao19831214.github.io/physics-software-sensors/ja/)
- [センサーカタログ](docs/sensor-catalog.ja.md)
- [Companion Tool カタログ](docs/tool-catalog.ja.md)
- [Capability Showcase](docs/capability-showcase.ja.md)
- [Getting Started](docs/getting-started.ja.md)
- [エビデンスと成熟度](docs/evidence-and-maturity.ja.md)
- [Sensor Intake](docs/sensor-intake.ja.md)
- [最初の完全な再利用ループ](docs/first-reuse-loop.ja.md) と [Maintenance Guide](docs/maintenance.md)
- [Current Project Status](docs/project-status.md)
- [用語](docs/i18n/terminology.md) と [i18n Style Guide](docs/i18n/style-guide.md)
- [Demo Asset Inventory](docs/demo-asset-inventory.md)
- [Architecture](docs/architecture.md)、[Data Format](docs/data-format.md)、[Benchmarking](docs/benchmarking.md)
- [v0.6.0 Release](https://github.com/WUHAO19831214/physics-software-sensors/releases/tag/v0.6.0)

<!-- section:development -->
## 開発と検証

```bash
python3 tools/validate_repo.py
pytest
npm --prefix packages/typescript test
```

[CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。新しい Sensor または大規模機能のみ正式 intake が必要で、通常の bugfix には不要です。

<!-- section:non-goals -->
## 現在の対象外

- stable、production-ready、measurement-grade、metrology-ready とは主張しない。
- YOLO モデルを自動取得せず、weight を同梱しない。
- 過去の実験プロジェクトに移行を強制しない。
- PyPI/npm には公開しません。最初に merge された E5 統合は offline replay 経路であり、下流の live-camera 実装を置き換えません。

<!-- section:license -->
## ライセンス

本 repository 固有のコードと文書は MIT です。過去のソースコード、モデル、データ、依存関係にはそれぞれのライセンス境界があります。[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) を参照してください。

最新 handoff: [.agent-handoff/latest.md](.agent-handoff/latest.md) · [.agent-handoff/latest.json](.agent-handoff/latest.json)
