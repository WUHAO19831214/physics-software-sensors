# テンプレート／単一物体トラッカー

[English](README.md) | [简体中文](README.zh-CN.md) | **日本語**

Sensor ID: `tracker.template` · Implementation version: `0.4.0` · Maturity: `experimental` · Evidence: `E3` · Release: `v0.6.0`

<!-- section:name -->
## 名称
テンプレート／単一物体トラッカー
<!-- section:description -->
## 一文での説明
ROI から 1 対象を初期化し、OpenCV CSRT/KCF/MIL fallback で画像上の bbox を追跡します。
<!-- section:physics-use -->
## 代表的な物理実験での用途
色分割が適さない運動・振動実験で、1 つの可視対象を連続追跡します。
<!-- section:measurement -->
## 実際に観測するもの
画像座標の bbox/center と tracking/lost/backend state です。静的テンプレートマッチングではなく、pixel motion は校正なしに物理変位にはなりません。
<!-- section:sources -->
## ソースプロジェクト
| Repository | Commit | Source path / use |
| --- | --- | --- |
| [audio-visual-soundfield-tracker-stable](https://github.com/WUHAO19831214/audio-visual-soundfield-tracker-stable) | `85740d686c67452a057540edb564d713e01ccc51` | `object_template_tracker.py::initialize/update/reset/create_opencv_tracker/validate_bbox` と tests; 抽出 ROI tracker |
| [physics-experiment-bridge-mvp](https://github.com/WUHAO19831214/physics-experiment-bridge-mvp) | `8bba87df6475cae1e595fc925551db8bea83fb68` | `TemplateMatchingAnalyzer.ts`; 関連 static matching profile、未抽出 |
<!-- section:how-it-works -->
## 動作原理
Initialization frame + ROI validation → CSRT→KCF→MIL backend → frame ごとの `update` → bbox/center または lost → 任意 reinitialize → `SensorEvent`。
<!-- section:input -->
## 入力
Camera/image `FramePacket`、initialization ROI、任意 backend preference。現 profile に template asset は不要です。
<!-- section:output -->
## 出力
Bbox、center、requested/actual backend、fallback attempt、initialization/reinitialization、lost state を含む `SensorEvent`。OpenCV は校正済み confidence を提供しません。
<!-- section:demo -->
## Demo
[![ROI tracker replay](assets/overview.png)](assets/README.md) 実 OpenCV runtime を synthetic target で実行したもので、実験精度の証拠ではありません。
<!-- section:example -->
## 最小 example
[python-template-tracker](../../examples/python-template-tracker/README.md) で `TemplateTrackerSensor` を実行します。
<!-- section:distribution -->
## 配布 / Download
Python package `0.5.0` + `classical-trackers`; [tracker.template-0.4.0.zip](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.template-0.4.0.zip)。
<!-- section:evidence -->
## エビデンスレベル
`E3`: 実 OpenCV contrib tracker を controlled synthetic/scripted sequence で実行済み。
<!-- section:maturity -->
## 成熟度
`experimental`; manifest は `incubating/adapter-present`。
<!-- section:limitations -->
## 既知の制限
Fallback は behavior/performance を変えます。Occlusion、scale、blur、不正 ROI で lost になります。校正済み confidence、物理 scale、E4 実機証拠はありません。
<!-- section:benchmark -->
## Benchmark
[Benchmark](benchmarks/README.md): initialization/update success、bbox/center error、lost/reinitialize、backend、latency。
<!-- section:provenance -->
## 来歴
Algorithm family boundary、source symbol、comparison は [SOURCE.md](SOURCE.md)、facts は [sensor.json](sensor.json) にあります。
