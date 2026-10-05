# Capability Showcase

[English](capability-showcase.md) | [简体中文](capability-showcase.zh-CN.md) | **日本語**

<!-- section:overview -->
## 概要

現在の展示は9 Sensor と4処理 Tool を含みます。従来8項目の集約画像に加え、FringeLab の実行画像とコンポーネント表を掲載し、両バッチの再利用入口を案内します。

[![Physics Software Sensors capability showcase](assets/capability-showcase.png)](../README.ja.md)

集約画像は `python3 tools/build_capability_showcase.py` により、下記 8 枚から再現可能な形で生成されます。ネットワークや外部画像ホストは使用しません。

<!-- section:software-sensors -->
## Software Sensor

### Camera Capture

[![合成 recorded camera frame](../sensors/camera.capture/assets/captured-frame.png)](../sensors/camera.capture/README.ja.md)

recorded または live のカメラ画像を、時刻情報付き `FramePacket` にします。画像は決定的な synthetic camera replay であり、実カメラの検証結果ではありません。

### Screen Capture

[![合成 shared-window pixel](../sensors/screen.capture/assets/captured-screen-frame.png)](../sensors/screen.capture/README.ja.md)

ユーザーが許可した画面または window の pixel を `FramePacket` にします。画像は synthetic shared-window pixel です。

### Number OCR

[![数値 OCR replay](../sensors/ocr.number/assets/overview.png)](../sensors/ocr.number/README.ja.md)

画面画像の ROI にある文字を認識し、数値観測へ parse します。device SDK の値を直接取得するものではありません。

### Color Marker Tracker

[![カラーマーカー replay](../sensors/tracker.color-marker/assets/overview.png)](../sensors/tracker.color-marker/README.ja.md)

HSV カラーマーカーを検出して画像座標上の中心を報告します。pixel 位置は校正済みの物理変位ではありません。

### 光スポット重心

[![光スポット重心 replay](../sensors/tracker.spot-centroid/assets/overview.png)](../sensors/tracker.spot-centroid/README.ja.md)

画像 ROI 内にある光スポットの輝度加重重心を報告します。機械変位を直接測定する Sensor ではありません。

### Template / Single-object Tracker

[![単一物体 tracker replay](../sensors/tracker.template/assets/overview.png)](../sensors/tracker.template/README.ja.md)

OpenCV の単一物体 backend で初期 ROI を追跡し、bbox/lost 状態を出力します。静的な template matching ではありません。

### YOLO Tracker

[![Recorded detector replay](../sensors/tracker.yolo/assets/overview.png)](../sensors/tracker.yolo/README.ja.md)

**recorded detector replay** によって detection と track ID を示します。この公開画像は実 YOLO model inference のエビデンスではありません。

<!-- section:companion-tools -->
## Companion Processing Tools

### 3次元ベクトル合成

[![recorded OCR 成分から3次元合成ベクトルを構成](../processing/vector.compose-3d/assets/overview.png)](../processing/vector.compose-3d/README.ja.md)

追跡可能な x/y/z スカラー成分を、合成ベクトルと renderer-neutral な model に構成します。既存の観測から導出する Tool であり、新しい Sensor の直接観測ではありません。[standalone Web example](../examples/web-vector-compose-3d/README.md)も参照してください。

### FringeLab 光強度分布・光学測定ツールキット

光強度分布実験から抽出した再利用コンポーネントを `@physics-software-sensors/fringelab` 0.1.0 に収録しました。両バッチを組み合わせても、将来のプロジェクトに個別導入しても利用できます。

**第1バッチ：**電卓、ROI、仮想定規、手動校正、断面解析。

**第2バッチ：**自動定規、目盛り OCR、ブラウザカメラ、光学逆算。

| コンポーネント | 再利用する機能 | 入口 |
| --- | --- | --- |
| 浮動電卓 | 移動、複数インスタンス、四則・括弧・累乗・科学記数法 | [`UI`](../packages/fringelab/README.md) |
| ROI・仮想定規 | 元画像座標で移動・回転・サイズ変更、端点・目盛り・吸着 | [`UI`](../packages/fringelab/README.md) |
| 手動校正 | 既知の長さによる2点校正と編集可能な区分多点写像 | [`calibration.scale-1d`](../processing/calibration.scale-1d/README.ja.md) |
| 断面・信号解析 | 相対応答、チャンネル品質、平滑化、ピークと幅 | [`image.strip-profile`](../sensors/image.strip-profile/README.ja.md) |
| 自動定規 | 実物目盛り候補、手動・領域指定・コントラスト・吸着設定 | [`vision.ruler-ticks`](../sensors/vision.ruler-ticks/README.ja.md) |
| 定規 OCR・カメラ | cm 数値候補、ブラウザ取得・静止フレーム・カメラ設定 | [`browser`](../packages/fringelab/README.md) |
| 光学逆算 | 干渉・回折波長、回帰、不確かさとシミュレーション | [`optics.fringe-wavelength`](../processing/optics.fringe-wavelength/README.ja.md) |

[![FringeLab 光強度分布・光学測定ツールキット — synthetic example](assets/fringelab-toolkit.png)](fringelab-toolkit.ja.md)

[中国語ガイド](fringelab-toolkit.zh-CN.md) · [API・導入](../packages/fringelab/README.md) · [実行可能なサンプル](../examples/web-fringelab-toolkit/README.md) · [信号特徴ツール](../processing/signal.profile-features/README.ja.md) · [FringeLab guide](fringelab-toolkit.ja.md)

自動・OCR 候補は人の確認後に適用し、手動・多点モードも保持します。画像は650 nm 合成サンプルの実行結果です。DN は相対応答であり、実機測定精度を認証するものではありません。

現在のカタログ：**9/9 Sensor + 4/4 処理 Tool = 13/13 capability**。電卓・オーバーレイ UI は追加の再利用コンポーネントで、Sensor 数には含めません。

### 実験的熱モデルと Core サポート

[GasLab 0.1.0](../packages/gaslab/README.ja.md) はヘッドレス気体教育モデルです。未公開 Core 0.3.1 は量候補解析、回帰/外挿、読値安定化、任意 OCR 前処理を追加します。[レビューと証拠](gaslab-intake.ja.md) · [実行例](../examples/headless-gaslab/README.md)。モデル/サポートパッケージは上記 **13 Sensor/Companion Tool capability** と別扱いです。直接観測追加、npm 公開、v0.6.0 収録を意味しません。

<!-- section:evidence -->
## エビデンス境界

これらは standalone、synthetic、recorded、replay の代表的なデモです。エビデンスレベルは capability ごとに異なり、画像だけで実機精度、校正、再現性、計量性能を証明することはできません。canonical demo asset は引き続き本 repository で version control されます。
