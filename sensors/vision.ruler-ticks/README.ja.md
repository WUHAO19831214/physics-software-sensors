# 実物定規の目盛り候補

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

`vision.ruler-ticks` · `0.1.0` · experimental · E2 · unreleased

<!-- section:name -->
## Name

実物定規の目盛り候補

<!-- section:description -->
## Description

実物定規の目盛り位置を未確認候補として返します。

<!-- section:physics-use -->
## Physics Use

画像スケールの補助測定に使用し、手動と多点方式を維持します。

<!-- section:measurement -->
## Measurement

Tick pixel position; fitted mm-per-pixel is an unconfirmed model-dependent inference.

<!-- section:sources -->
## Sources

https://github.com/WUHAO19831214/webcam-laser-fringelab · `37a8b3996791790a22980b0d562996a65a3a65ef` · lib/ruler-detection.ts, lib/ruler.worker.ts, lib/ruler-ocr.ts

<!-- section:how-it-works -->
## How It Works

固定ソースを使用し、相対 import のみ変更しました。

<!-- section:input -->
## Input

元画像の RGBA FramePacket、明示 ROI と設定。

<!-- section:output -->
## Output

SensorEvent with candidate/ticks/residuals and calibration_applied=false.

<!-- section:demo -->
## Demo

独立ブラウザー実行。画像はローカル処理です。 [Demo](../../examples/web-fringelab-toolkit/README.md)

<!-- section:example -->
## Example

```ts
import { RulerTicksSensor } from '@physics-software-sensors/fringelab/sensors';
// frame: RuntimeFramePacket containing native RGBA pixels from any source.
const sensor = new RulerTicksSensor();
const configured = sensor.configure({ region: { x: 80, y: 390, width: 750, height: 110 } });
if (!configured.accepted) throw new Error(configured.warnings.join('; '));
await sensor.start({ runId: frame.runId });
for await (const event of sensor.process(frame)) console.log(event);
await sensor.stop();
```

[Runnable example](../../examples/web-fringelab-toolkit/README.md)

<!-- section:distribution -->
## Distribution

TypeScript パッケージとソース。v0.6.0 には含まれません。 [Package](../../packages/fringelab/README.md)

<!-- section:evidence -->
## Evidence

固定ソース golden E2。実デバイス E4 と下流 E5 は未測定。

<!-- section:maturity -->
## Maturity

experimental。エビデンスは計測精度の認証ではありません。

<!-- section:limitations -->
## Limitations

ミリ目盛りモデルには周期の曖昧さがあります。OCR とスケールは人が確認します。1D 校正は2D射影補正ではありません。

<!-- section:benchmark -->
## Benchmark

[Benchmark record](../../benchmarks/results/fringelab-extraction-2026-10-05.md)

<!-- section:provenance -->
## Provenance

[SOURCE.md](SOURCE.md)
