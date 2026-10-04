# 1D プロファイル特徴

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

`signal.profile-features` · `0.1.0` · experimental · unreleased

<!-- section:name -->
## Name

1D プロファイル特徴

<!-- section:purpose -->
## Purpose

1D プロファイル特徴。既存の観測を処理し、新たな直接観測を生成しません。

<!-- section:boundary -->
## Boundary

1D プロファイル特徴。既存の観測を処理し、新たな直接観測を生成しません。

<!-- section:source -->
## Source

https://github.com/WUHAO19831214/webcam-laser-fringelab · `37a8b3996791790a22980b0d562996a65a3a65ef` · lib/signal.ts

<!-- section:input -->
## Input

finite signal array + axis/sample semantics + processing options

<!-- section:output -->
## Output

processed profile, peak/trough centers, widths and periods

<!-- section:example -->
## Example

```ts
import { Signal } from '@physics-software-sensors/fringelab';
const samples = Float64Array.from([0, 1, 3, 8, 13, 8, 3, 1, 0]);
const smoothed = Signal.gaussianSmooth(samples, 0.8);
const peaks = Signal.detectPeaks(smoothed, { minProminence: 2, minDistance: 3 });
const period = Signal.estimatePeriodAutocorrelation(smoothed);
// A short signal need not contain a measurable period. Widths are in samples;
// convert using the original pixel axis and confirmed scale, not display size.
```

[Runnable example](../../examples/web-fringelab-toolkit/README.md)

<!-- section:quality -->
## Quality

飽和、確認状態、ソース版、入力不確かさを維持。失効データを現測定にしません。

<!-- section:coordinates -->
## Coordinates

元画像ピクセル、mm 校正、m ベースの光学モデル。2D射影補正は含みません。

<!-- section:demo -->
## Demo

独立ブラウザー実行。画像はローカル処理です。 [Demo](../../examples/web-fringelab-toolkit/README.md)

<!-- section:status -->
## Status

experimental。エビデンスは計測精度の認証ではありません。 Version 0.1.0, unreleased; v0.6.0 unchanged.

<!-- section:limitations -->
## Limitations

lux/W/m² は出力しません。チャンネル、飽和、標本範囲を維持します。 ミリ目盛りモデルには周期の曖昧さがあります。OCR とスケールは人が確認します。1D 校正は2D射影補正ではありません。

<!-- section:provenance -->
## Provenance

[SOURCE.md](SOURCE.md)
