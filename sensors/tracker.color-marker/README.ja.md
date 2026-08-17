# カラーマーカートラッカー

[English](README.md) | [简体中文](README.zh-CN.md) | **日本語**

Sensor ID: `tracker.color-marker` · Implementation version: `0.2.0` · Maturity: `experimental` · Evidence: `E2` · Release: `v0.6.0`

<!-- section:name -->
## 名称
カラーマーカートラッカー
<!-- section:description -->
## 一文での説明
Camera image から指定色の marker を検出し、画像座標の位置とロスト状態を連続出力します。
<!-- section:physics-use -->
## 代表的な物理実験での用途
色付き球・marker を追跡し、運動、振動、軌跡、音声・映像整合の実験に使います。
<!-- section:measurement -->
## 実際に観測するもの
Pixel centroid、輪郭・面積の証拠、検出状態です。変位、速度、振幅には明示的な校正と時間導出が必要です。
<!-- section:sources -->
## ソースプロジェクト
| Repository | Commit | Source path / use |
| --- | --- | --- |
| [audio-visual-soundfield-tracker-stable](https://github.com/WUHAO19831214/audio-visual-soundfield-tracker-stable) | `85740d686c67452a057540edb564d713e01ccc51` | `tennis_ball_tracker.py::TennisBallTracker.update`、mask/candidate、tests; 抽出 profile |
| [physics-experiment-bridge-mvp](https://github.com/WUHAO19831214/physics-experiment-bridge-mvp) | `8bba87df6475cae1e595fc925551db8bea83fb68` | `ColorTrackingAnalyzer.ts`、`MarkerTrackingAnalyzer.ts`; 関連 browser profile、未抽出 |
<!-- section:how-it-works -->
## 動作原理
BGR frame → HSV → threshold mask → morphology → contour candidate → area/circularity/continuity ranking → centroid smoothing/lost → `SensorEvent`。
<!-- section:input -->
## 入力
Camera/image `FramePacket`、HSV threshold、area/circularity filter、smoothing、任意 ROI/continuity 設定。
<!-- section:output -->
## 出力
Raw/smoothed pixel center、normalized position、bbox/area/quality evidence、明示的 lost 状態を含む tracking `SensorEvent`。
<!-- section:demo -->
## Demo
[![Color marker replay](assets/overview.png)](assets/README.md) Standalone synthetic output で、実験精度の主張ではありません。
<!-- section:example -->
## 最小 example
[python-color-marker](../../examples/python-color-marker/README.md) で `ColorMarkerSensor` を実行します。
<!-- section:distribution -->
## 配布 / Download
Python package `0.5.0` + `color-marker`; [tracker.color-marker-0.2.0.zip](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.color-marker-0.2.0.zip)。
<!-- section:evidence -->
## エビデンスレベル
`E2`: 固定 source commit の実行/golden 比較と、決定的 success/lost/reacquire test。
<!-- section:maturity -->
## 成熟度
`experimental`; manifest は `incubating/adapter-present`。
<!-- section:limitations -->
## 既知の制限
HSV threshold は camera/照明に依存します。類似色、blur、occlusion、exposure で誤検出・lost が起きます。Algorithm confidence は物理的不確かさではありません。
<!-- section:benchmark -->
## Benchmark
[Benchmark](benchmarks/README.md): success、lost-frame rate、center error、latency/FPS、source-output compatibility。
<!-- section:provenance -->
## 来歴
抽出変更、source symbol、tolerance、golden method は [SOURCE.md](SOURCE.md)、facts は [sensor.json](sensor.json) にあります。
