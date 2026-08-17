# YOLO 検出・追跡センサー

[English](README.md) | [简体中文](README.zh-CN.md) | **日本語**

Sensor ID: `tracker.yolo` · Implementation version: `0.5.0` · Maturity: `experimental` · Evidence: `E2` · Release: `v0.6.0`

<!-- section:name -->
## 名称
YOLO 検出・追跡センサー
<!-- section:description -->
## 一文での説明
複数対象 detector/tracker backend の結果を、来歴付き detection、bbox、Track ID に変換します。
<!-- section:physics-use -->
## 代表的な物理実験での用途
審査済みローカル model/runtime が適切な場合に、複数の可視物体・人物の画像軌跡を観測します。
<!-- section:measurement -->
## 実際に観測するもの
Class label、detector confidence、bbox/center、backend Track ID です。Confidence は精度、tracking confidence、物理的不確かさではなく、物理量には pixel 校正が必要です。
<!-- section:sources -->
## ソースプロジェクト
| Repository | Commit | Source path / use |
| --- | --- | --- |
| [audio-visual-soundfield-tracker-stable](https://github.com/WUHAO19831214/audio-visual-soundfield-tracker-stable) | `85740d686c67452a057540edb564d713e01ccc51` | `detector.py::Detector.detect/track/_detect_hog`、`camera_processor.py`、config/setup/model docs/tests; YOLO/ByteTrack と HOG fallback boundary |
<!-- section:how-it-works -->
## 動作原理
Frame → backend 選択 → 必要時 model artifact 検証 → detection → 任意 ByteTrack/recorded Track ID → adapter result/fallback evidence → `SensorEvent`。
<!-- section:input -->
## 入力
Camera/image `FramePacket`、backend 設定、class filter。実 YOLO では審査済みローカル `ModelArtifact` path/SHA-256/license status が必要です。
<!-- section:output -->
## 出力
各対象の class ID/name、bbox/center、detector confidence、任意 Track ID、requested/actual/attempted backend metadata を含む `SensorEvent`。
<!-- section:demo -->
## Demo
[![Recorded detector replay](assets/overview.png)](assets/README.md) Source-compatible recorded output で、実 YOLO inference や model accuracy の証拠ではありません。
<!-- section:example -->
## 最小 example
[python-yolo-tracker](../../examples/python-yolo-tracker/README.md) で model を取得しない `RecordedDetectorBackend` を実行します。
<!-- section:distribution -->
## 配布 / Download
Python package `0.5.0`; offline `yolo-recorded`; [tracker.yolo-0.5.0.zip](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.yolo-0.5.0.zip)。実 `yolo-runtime` は別です。
<!-- section:evidence -->
## エビデンスレベル
`E2`: 固定 source recorded output と adapter/fallback/lifecycle test。実 Ultralytics/ByteTrack inference は未実行です。
<!-- section:maturity -->
## 成熟度
`experimental`; manifest は `incubating/adapter-present`。
<!-- section:limitations -->
## 既知の制限
`.pt`/`.onnx`/`.engine` を同梱・自動取得しません。HOG は person-only で YOLO と同等ではありません。Model accuracy、実 ByteTrack、実験室/device performance は未測定です。
<!-- section:benchmark -->
## Benchmark
[Benchmark](benchmarks/README.md): adapter/source compatibility、multi-target/lost/fallback semantics、latency。Model accuracy は not measured。
<!-- section:provenance -->
## 来歴
Source symbol、model/license boundary、replay construction は [SOURCE.md](SOURCE.md) と [YOLO review](../../docs/yolo-model-and-license-review.md)、facts は [sensor.json](sensor.json) にあります。
