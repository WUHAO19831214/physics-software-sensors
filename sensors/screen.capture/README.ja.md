# 画面キャプチャセンサー

[English](README.md) | [简体中文](README.zh-CN.md) | **日本語**

Sensor ID: `screen.capture` · Implementation version: `0.3.0` · Maturity: `experimental` · Evidence: `E1` · Release: `v0.6.0`

<!-- section:name -->
## 名称
画面キャプチャセンサー
<!-- section:description -->
## 一文での説明
ユーザーが選択した画面、window、tab の pixel を取得し、timestamp 付き screen `FramePacket` を出力します。
<!-- section:physics-use -->
## 代表的な物理実験での用途
利用可能な device SDK がない場合に、計測ソフト画面を下流の ROI/OCR 処理へ橋渡しします。
<!-- section:measurement -->
## 実際に観測するもの
直接観測するのは許可された画面 pixel と取得 lifecycle/time であり、機器内部値、SDK 値、物理量ではありません。
<!-- section:sources -->
## ソースプロジェクト
| Repository | Commit | Source path / use |
| --- | --- | --- |
| [physics-experiment-bridge-mvp](https://github.com/WUHAO19831214/physics-experiment-bridge-mvp) | `8bba87df6475cae1e595fc925551db8bea83fb68` | `ScreenCapturePanel.tsx`、`screenCaptureRuntime.ts`、`SCREEN_CAPTURE_PIPELINE.md`; 許可画面→ROI/OCR |
| [ampere-force-visualizer-teacher-yanan](https://github.com/WUHAO19831214/ampere-force-visualizer-teacher-yanan) | `cb073e89d6d87129287030f1df08bd540504eb39` | `ScreenCapturePanel.tsx`、`SENSOR_INTEGRATION.md`; Fy/Fz 表示 pixel bridge |
<!-- section:how-it-works -->
## 動作原理
User gesture → `getDisplayMedia` permission → stream → video/canvas pixel → time/status → screen `FramePacket`。Recorded backend で browser UI なしの決定的 replay が可能です。
<!-- section:input -->
## 入力
Browser permission/configuration または recorded RGBA frame、要求 sampling interval、source ID。
<!-- section:output -->
## 出力
ID、RGBA size/pixel、artifact URI、timestamp、quality flag を含む screen `FramePacket`。
<!-- section:demo -->
## Demo
[![画面 replay](assets/captured-screen-frame.png)](assets/README.md) Synthetic replay は browser/device 互換性の証拠ではありません。
<!-- section:example -->
## 最小 example
[web-screen-capture](../../examples/web-screen-capture/README.md) を実行し、OCR 合成は [web-screen-to-ocr](../../examples/web-screen-to-ocr/README.md) を参照します。
<!-- section:distribution -->
## 配布 / Download
TypeScript package `0.3.0`; [screen.capture-0.3.0.zip](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/screen.capture-0.3.0.zip)。Bundle は共通 tgz に依存します。
<!-- section:evidence -->
## エビデンスレベル
`E1`: 決定的 recorded RGBA replay。Browser capture は自動実行しません。
<!-- section:maturity -->
## 成熟度
`experimental`; manifest は `incubating/adapter-present`。
<!-- section:limitations -->
## 既知の制限
Permission は user gesture で開始し、reload 後は通常再許可が必要です。拒否/終了は capture lifecycle error です。OCR 失敗を mock 数値で置換しません。
<!-- section:benchmark -->
## Benchmark
[Benchmark](benchmarks/README.md) と[互換性 matrix](../../docs/compatibility-matrix.md)を参照してください。
<!-- section:provenance -->
## 来歴
[SOURCE.md](SOURCE.md) と [sensor.json](sensor.json) を参照してください。
