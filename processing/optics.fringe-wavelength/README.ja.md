# 光学縞の波長推定

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

`optics.fringe-wavelength` · `0.1.0` · experimental · unreleased

<!-- section:name -->
## Name

光学縞の波長推定

<!-- section:purpose -->
## Purpose

光学縞の波長推定。既存の観測を処理し、新たな直接観測を生成しません。

<!-- section:boundary -->
## Boundary

光学縞の波長推定。既存の観測を処理し、新たな直接観測を生成しません。

<!-- section:source -->
## Source

https://github.com/WUHAO19831214/webcam-laser-fringelab · `37a8b3996791790a22980b0d562996a65a3a65ef` · lib/physics.ts, lib/analysis.ts

<!-- section:input -->
## Input

calibrated positions, confirmed orders and a/d/L/errors

<!-- section:output -->
## Output

wavelength, regression, method/quality and uncertainty

<!-- section:example -->
## Example

```ts
import { Optics } from '@physics-software-sensors/fringelab';
const fit = Optics.fitDoubleSlitOrders({
  observations: [-2, -1, 0, 1, 2].map(order => ({
    order, screenPositionM: order * 0.0039
  })),
  screenDistanceM: 1.5,
  slitSeparationM: 0.00025,
  centerPositionM: 0
});
// Orders and metre positions must come from an explicitly confirmed workflow.
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
