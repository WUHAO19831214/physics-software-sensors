# 数値 OCR センサー

[English](README.md) | [简体中文](README.zh-CN.md) | **日本語**

Sensor ID: `ocr.number` · Implementation version: `0.2.0` · Maturity: `experimental` · Evidence: `E3` · Release: `v0.6.0`

<!-- section:name -->
## 名称
数値 OCR センサー
<!-- section:description -->
## 一文での説明
Frame の ROI から数値表示を読み取り、raw text、parse 値、信頼度、処理時間、warning、明示的 failure を保持します。
<!-- section:physics-use -->
## 代表的な物理実験での用途
直接 SDK data がない場合に既存計測ソフトの表示値を読み、授業可視化や同期解析へ渡します。
<!-- section:measurement -->
## 実際に観測するもの
経路は software display → screen pixels → OCR text → numeric parse です。機器内部を直接読まず、unit と物理範囲 check は設定・下流処理が担います。
<!-- section:sources -->
## ソースプロジェクト
| Repository | Commit | Source path / use |
| --- | --- | --- |
| [physics-experiment-bridge-mvp](https://github.com/WUHAO19831214/physics-experiment-bridge-mvp) | `8bba87df6475cae1e595fc925551db8bea83fb68` | `TesseractRecognizer.ts`、`extractNumber.ts`、preprocess、`OCR_VALIDATION.md`; 実 Tesseract.js |
| [ampere-force-visualizer-teacher-yanan](https://github.com/WUHAO19831214/ampere-force-visualizer-teacher-yanan) | `cb073e89d6d87129287030f1df08bd540504eb39` | 同一 recognizer/utilities; 教師用 Fy/Fz 表示読取 |
<!-- section:how-it-works -->
## 動作原理
RGBA frame → normalized ROI → preprocess → Tesseract.js/recorded recognizer → raw text 正規化 → numeric parse/validation → `SensorEvent`。失敗時に mock measurement は出しません。
<!-- section:input -->
## 入力
RGBA pixel を持つ screen/image `FramePacket`、ROI、whitelist/preprocess option、value name、unit。
<!-- section:output -->
## 出力
`raw_text`、成功時 measurement、信頼度、duration、warning/artifact、明示的 `OCR_RECOGNITION_FAILED`/`OCR_PARSE_FAILED` を持つ `SensorEvent`。
<!-- section:demo -->
## Demo
[![Synthetic pixel OCR](assets/overview.png)](assets/README.md) 実 Tesseract.js を synthetic pixels で実行した証拠で、実機表示ではありません。
<!-- section:example -->
## 最小 example
[web-number-ocr](../../examples/web-number-ocr/README.md) または [screen-to-ocr](../../examples/web-screen-to-ocr/README.md) を実行します。
<!-- section:distribution -->
## 配布 / Download
TypeScript package `0.3.0`; [ocr.number-0.2.0.zip](https://github.com/WUHAO19831214/physics-software-sensors/releases/download/v0.6.0/ocr.number-0.2.0.zip)。実 OCR は runtime に言語 data を取得する場合があります。
<!-- section:evidence -->
## エビデンスレベル
`E3`: 実 Tesseract.js を制御された synthetic pixels と failure path で実行済み。
<!-- section:maturity -->
## 成熟度
`experimental`; manifest は `incubating/adapter-present`。
<!-- section:limitations -->
## 既知の制限
標準 parse は科学表記を扱いません。文字正規化で英字と数字を誤る場合があります。信頼度は精度ではなく、実表示・font・scale・glare・browser の E4 証拠はありません。
<!-- section:benchmark -->
## Benchmark
[OCR benchmark](benchmarks/README.md) は exact match、parse success/error、latency、failure rate を扱います。
<!-- section:provenance -->
## 来歴
2 固定 commit の主要 OCR/preprocess file は同一です。Hash・変更は [SOURCE.md](SOURCE.md)、facts は [sensor.json](sensor.json) にあります。
