# 3次元ベクトル合成・再構成

[English](README.md) | [简体中文](README.zh-CN.md) | **日本語**

<!-- section:name -->
## 名称

`vector.compose-3d` · 3次元ベクトル合成・再構成 · version `0.1.0` · `experimental`

これは **Companion Processing Tool（補助処理ツール）**であり、Sensor ではありません。

<!-- section:purpose -->
## 用途

3 個のスカラー成分から追跡可能な3次元ベクトルを構成し、大きさ、正規化方向、方位角、仰角を求めます。OCR などのスカラー測定後に配置し、力、磁場、加速度、速度などの実験に利用できます。

<!-- section:boundary -->
## 観測境界

このツールは新しい直接観測を行いません。`screen.capture` が画面ピクセルを観測し、`ocr.number` がスカラー値を導出し、本ツールは既存の値を処理します。拘束条件で与えた成分を観測値として表現することはありません。

<!-- section:source -->
## ソースでの挙動

延安のアンペール力プロジェクトでは、旧版の F1/F2/F3 を x/y/z の直交スカラー成分として扱っていました。現在の main は Fy/Fz を OCR で観測し、Fx を明示的にゼロへ拘束します。[Git 履歴調査](../../docs/research/yanan-vector-reconstruction-history.md)では両者を区別しています。

<!-- section:input -->
## 入力

各 x/y/z 成分は、利用可能な場合の有限値、`observed | derived | constrained | default | missing`、任意のミリ秒タイムスタンプ、成分固有の信頼度、不確かさ、warning、error を保持します。物理量、単位、座標系は呼び出し側の metadata であり、数学 core は力に限定されません。

<!-- section:output -->
## 出力

`Vector3Measurement` は成分、大きさ、正規化ベクトル、方向、最新成分時刻、成分間の時間差、状態、統合していない成分別品質を保持します。方位角は度単位の `[0, 360)` で、x-y 平面の +x から +y 方向です。仰角は度単位の `[-90, 90]` で、x-y 平面から +z 方向です。ゼロベクトルでは `normalized` と `direction` が `null` になります。

<!-- section:example -->
## 最小例

```ts
import { Vector3Assembler } from '@physics-software-sensors/core';

const result = new Vector3Assembler({ maxComponentSkewMs: 150 }).compose({
  quantity: 'force',
  unit: 'N',
  coordinateSystem: 'classroom-x-y-z',
  components: {
    x: { value: 0, source: 'constrained' },
    y: { value: 1.2, source: 'observed', timestampMs: 1000 },
    z: { value: -0.8, source: 'observed', timestampMs: 1040 },
  },
});
```

OCR 失敗は `{ source: 'missing' }` へ変換します。その場合は `incomplete` のままとし、架空のベクトルを生成しません。

<!-- section:quality -->
## 時刻と品質

タイムスタンプ差が `maxComponentSkewMs` を超えると、結果を保持したまま `component-time-skew` と warning を付けます。成分ごとの信頼度は別々に保持し、平均値を「ベクトル精度」とは呼びません。

<!-- section:coordinates -->
## 座標と任意レンダリングアダプター

数学 core は呼び出し側の x/y/z 座標系を使います。`CoordinateTransform3` は独立した行列アダプターです。延安用の任意変換は教室座標 `(x,y,z)` → Three.js scene `(-x,z,y)` です。`createVector3RenderModel` は軸、成分矢印、合成矢印のデータだけを生成し、Three.js やアプリ UI を所有しません。

<!-- section:demo -->
## Demo とテスト

[小規模ブラウザ demo](../../examples/web-vector-compose-3d/README.md)は手入力と recorded OCR を扱います。source golden、数学、成分 source、時刻差、座標、OCR composition の検証は [benchmark](benchmarks/README.md)を参照してください。

<!-- section:status -->
## 状態と配布

現在は `experimental`、version `0.1.0` で、未リリースの TypeScript source tree にのみ存在します。不変の `v0.6.0` Release には含まれず、`v0.7.0` も未公開です。Sensor 数は引き続き 7 です。

<!-- section:limitations -->
## 既知の制約

- 延安プロジェクトのリアルタイム処理へは未統合です。
- 物理校正や計量上の不確かさを推定しません。
- Three.js 依存も完全な 3D scene renderer もなく、renderer-neutral な矢印データのみを提供します。
- 呼び出し側のタイムスタンプは同じ clock domain である必要があります。
- ブラウザ／OS 間の性能 benchmark は未実施です。

<!-- section:provenance -->
## 来歴

commit/file/symbol のアンカーと clean rewrite のライセンス判断は [SOURCE.md](SOURCE.md)を参照してください。ソースリポジトリのコードや素材は複製していません。
