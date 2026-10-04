# 確認済みの2点・多点局所校正

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

`calibration.scale-1d` · `0.1.0` · experimental · unreleased

<!-- section:name -->
## Name

確認済みの2点・多点局所校正

<!-- section:purpose -->
## Purpose

確認済みの2点・多点局所校正。既存の観測を処理し、新たな直接観測を生成しません。

<!-- section:boundary -->
## Boundary

確認済みの2点・多点局所校正。既存の観測を処理し、新たな直接観測を生成しません。

<!-- section:source -->
## Source

https://github.com/WUHAO19831214/webcam-laser-fringelab · `37a8b3996791790a22980b0d562996a65a3a65ef` · lib/ruler.ts, lib/spatial.ts

<!-- section:input -->
## Input

pixel points + known mm readings + source/calibration IDs

<!-- section:output -->
## Output

position mm, extrapolation and stale status

<!-- section:example -->
## Example

```ts
import { confirmTwoPointCalibration, calibratedPosition,
  confirmMultiPointCalibration } from '@physics-software-sensors/fringelab';
const scale = confirmTwoPointCalibration({ start: { x: 20, y: 40 },
  end: { x: 120, y: 40 }, knownLengthMm: 10 }, 'photo:1', 'scale:1');
const position = calibratedPosition({ x: 70, y: 40 }, scale, 'photo:1');
// position.valueMm === 5; a different source key returns stale/null.
const localScale = confirmMultiPointCalibration([
  { x: 0, y: 0, mm: 0 }, { x: 100, y: 0, mm: 10 },
  { x: 220, y: 0, mm: 20 }
], 'photo:1', 'scale:2');
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
