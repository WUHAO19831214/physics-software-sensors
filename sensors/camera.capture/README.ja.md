# カメラキャプチャセンサー

[English](README.md) | [简体中文](README.zh-CN.md) | **日本語**

Sensor ID: `camera.capture` · Implementation version: `0.3.0` · Maturity: `experimental` · Evidence: `E1` · Release: `v0.6.0`

<!-- section:name -->
## 名称
カメラキャプチャセンサー

<!-- section:description -->
## 一文での説明
時刻、バックエンド、取得品質のメタデータを明示したカメラ・画像系列フレームを出力します。

<!-- section:physics-use -->
## 代表的な物理実験での用途
運動、振動、軌跡、光スポット、音声・映像同期実験へ視覚入力を供給し、元アプリの UI や実験ロジックには依存しません。

<!-- section:measurement -->
## 実際に観測するもの
直接観測するのは画像 pixel と取得時刻・状態です。位置、変位、速度、振幅には下流 Sensor が必要で、物理単位には校正が必要です。

<!-- section:sources -->
## ソースプロジェクト
| Repository | Commit | Source path / use |
| --- | --- | --- |
| [audio-visual-soundfield-tracker-stable](https://github.com/WUHAO19831214/audio-visual-soundfield-tracker-stable) | `85740d686c67452a057540edb564d713e01ccc51` | `browser_capture.py`、`camera_devices.py`、`local_capture.py`、`camera_processor.py`; OpenCV/WebRTC |
| [spot-vibration-tracking-system-20260508-171952](https://github.com/WUHAO19831214/spot-vibration-tracking-system-20260508-171952) | `7f0d91cc73afafaecc54acc46b2b9d69375d994a` | `app.js`; camera→canvas 光スポット処理 |
| [forced-vibration-af-analyzer-20260502-122715](https://github.com/WUHAO19831214/forced-vibration-af-analyzer-20260502-122715) | `c3f58175a09ff29cacdfb976a5055758c4eff619` | `app.js`; camera 選択と振動入力 |
| [physics-experiment-bridge-mvp](https://github.com/WUHAO19831214/physics-experiment-bridge-mvp) | `8bba87df6475cae1e595fc925551db8bea83fb68` | `CameraCapturePanel.tsx`、`cameraUtils.ts` |
| [ampere-force-visualizer-teacher-yanan](https://github.com/WUHAO19831214/ampere-force-visualizer-teacher-yanan) | `cb073e89d6d87129287030f1df08bd540504eb39` | 教師用アプリの同じ camera 境界 |

<!-- section:how-it-works -->
## 動作原理
Backend → frame 取得 → wall/monotonic timestamp → pixel/media metadata → requested/measured rate・status → `FramePacket`。現在の Python backend は OpenCV と決定的 image-sequence replay です。

<!-- section:input -->
## 入力
Camera device/backend 設定、要求 width/height/FPS、任意の画像系列。Browser camera は言語横断 contract で、現 Python 実装には含まれません。

<!-- section:output -->
## 出力
Frame/run/sequence ID、寸法、color/media type、observed/monotonic time、backend status、quality flag を含む camera `FramePacket`。

<!-- section:demo -->
## Demo
[![Synthetic replay frame](assets/captured-frame.png)](assets/README.md) Synthetic replay は adapter 経路の証拠で、実カメラ互換性や時刻精度の証拠ではありません。

<!-- section:example -->
## 最小 example
[python-camera-capture](../../examples/python-camera-capture/README.md) で `CameraSource` と `ImageSequenceCameraBackend` を実行します。

<!-- section:distribution -->
## 配布 / Download
Python package `0.5.0`; [camera.capture-0.3.0.zip](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/camera.capture-0.3.0.zip)。Bundle は package core を複製しません。

<!-- section:evidence -->
## エビデンスレベル
`E1`: 決定的 synthetic image-sequence replay のみ。

<!-- section:maturity -->
## 成熟度
`experimental`。Manifest は `incubating/adapter-present` のままで、文書の完成だけでは昇格しません。

<!-- section:limitations -->
## 既知の制限
要求 FPS/解像度は backend の nominal/measured 値と異なる場合があります。実 camera、driver、drop frame、時刻精度の E4 証拠はありません。

<!-- section:benchmark -->
## Benchmark
[Capture replay benchmark](benchmarks/README.md) と[集約結果](../../docs/benchmark-summary.md)を参照してください。

<!-- section:provenance -->
## 来歴
File/symbol 単位の抽出・検証は [SOURCE.md](SOURCE.md)、machine facts は [sensor.json](sensor.json) にあります。
