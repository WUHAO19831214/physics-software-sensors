# 光スポット重心トラッカー

[English](README.md) | [简体中文](README.zh-CN.md) | **日本語**

Sensor ID: `tracker.spot-centroid` · Implementation version: `0.4.0` · Maturity: `experimental` · Evidence: `E2` · Release: `v0.6.0`

<!-- section:name -->
## 名称
光スポット重心（Spot Centroid）トラッカー
<!-- section:description -->
## 一文での説明
赤色の光スポットを検出し、画像上の輝度加重重心と quality/lost evidence を出力します。
<!-- section:physics-use -->
## 代表的な物理実験での用途
振動、共振、軌跡実験で投影・取り付けた赤色光スポットを観測し、下流で振幅・周波数を解析します。
<!-- section:measurement -->
## 実際に観測するもの
赤 candidate pixel、weighted centroid、bbox、weight sum、saturation/ROI-edge evidence、lost state です。機械変位や振幅を直接測定しません。
<!-- section:sources -->
## ソースプロジェクト
| Repository | Commit | Source path / use |
| --- | --- | --- |
| [spot-vibration-tracking-system-20260508-171952](https://github.com/WUHAO19831214/spot-vibration-tracking-system-20260508-171952) | `7f0d91cc73afafaecc54acc46b2b9d69375d994a` | `app.js::rgbToHsv/trackRedSpot/getAmplitudeFrom`; 赤色加重重心・sweep window |
| [forced-vibration-af-analyzer-20260502-122715](https://github.com/WUHAO19831214/forced-vibration-af-analyzer-20260502-122715) | `c3f58175a09ff29cacdfb976a5055758c4eff619` | 同一 threshold/weight 式; 強制振動画像範囲 |
<!-- section:how-it-works -->
## 動作原理
Frame/ROI → source-compatible red threshold → pixel brightness weight → weighted sum → centroid/bbox/quality flag または明示的 lost → `SensorEvent`。
<!-- section:input -->
## 入力
Camera/image `FramePacket`、normalized ROI、source-compatible red threshold/quality 設定。
<!-- section:output -->
## 出力
Pixel/normalized centroid、bbox、candidate/weight evidence、`spot-lost`、`low-signal`、`overexposed`、`roi-edge` 等を持つ `SensorEvent`。
<!-- section:demo -->
## Demo
[![光スポット重心 replay](assets/overview.png)](assets/README.md) Synthetic adapter output で、実験校正の証拠ではありません。
<!-- section:example -->
## 最小 example
[spot-centroid](../../examples/spot-centroid/README.md) で `SpotCentroidSensor` を実行します。
<!-- section:distribution -->
## 配布 / Download
Python package `0.5.0` + `classical-trackers`; [tracker.spot-centroid-0.4.0.zip](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/tracker.spot-centroid-0.4.0.zip)。
<!-- section:evidence -->
## エビデンスレベル
`E2`: source 式比較と centroid/lost/quality path の golden replay。
<!-- section:maturity -->
## 成熟度
`experimental`; manifest は `incubating/adapter-present`。
<!-- section:limitations -->
## 既知の制限
0.4.0 は source red-channel profile のみです。Exposure、弱い spot、ROI edge が結果に影響します。Repeatability、不確かさ、物理校正の E4 証拠はありません。
<!-- section:benchmark -->
## Benchmark
[Benchmark](benchmarks/README.md): centroid pixel error、missing rate、exposure/ROI sensitivity、latency。
<!-- section:provenance -->
## 来歴
固定 source function/formula と比較結果は [SOURCE.md](SOURCE.md)、facts は [sensor.json](sensor.json) にあります。
