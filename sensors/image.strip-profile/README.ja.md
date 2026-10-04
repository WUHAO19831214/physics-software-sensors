# 相対画像応答プロファイル

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

`image.strip-profile` · `0.1.0` · experimental · E2 · unreleased

<!-- section:name -->
## Name

相対画像応答プロファイル

<!-- section:description -->
## Description

回転 RGBA 帯域から相対カメラ応答を抽出します。

<!-- section:physics-use -->
## Physics Use

回折、画像プロファイル、光学計測に使用できます。

<!-- section:measurement -->
## Measurement

Relative DN, sample coverage and pixel axis; not calibrated intensity.

<!-- section:sources -->
## Sources

https://github.com/WUHAO19831214/webcam-laser-fringelab · `37a8b3996791790a22980b0d562996a65a3a65ef` · lib/signal.ts

<!-- section:how-it-works -->
## How It Works

固定ソースを使用し、相対 import のみ変更しました。

<!-- section:input -->
## Input

元画像の RGBA FramePacket、明示 ROI と設定。

<!-- section:output -->
## Output

SensorEvent with profile/channel/coverage payload.

<!-- section:demo -->
## Demo

独立ブラウザー実行。画像はローカル処理です。 [Demo](../../examples/web-fringelab-toolkit/README.md)

<!-- section:example -->
## Example

```ts
import { StripProfileSensor } from '@physics-software-sensors/fringelab/sensors';
// frame: RuntimeFramePacket containing native RGBA pixels from any source.
const sensor = new StripProfileSensor();
const configured = sensor.configure({ channel: 'r', roi: { centerX: 480, centerY: 270, width: 700, height: 50, angleDeg: 0 } });
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

lux/W/m² は出力しません。チャンネル、飽和、標本範囲を維持します。

<!-- section:benchmark -->
## Benchmark

[Benchmark record](../../benchmarks/results/fringelab-extraction-2026-10-05.md)

<!-- section:provenance -->
## Provenance

[SOURCE.md](SOURCE.md)
