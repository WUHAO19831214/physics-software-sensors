# GasLab 実験的ドメインパッケージ

[English](README.md) | [简体中文](README.zh-CN.md) | **日本語**

`@physics-software-sensors/gaslab` 0.1.0 は UI、DOM、Three.js に依存しない気体教育モデルです。実行時依存はありません。Node >=22.13、NodeNext ESM を使用し、`.`, `./core`, `./physics`, `./simulation`, `./driver` を公開します。npm 未公開で、不変の v0.6.0 Release には含まれません。

```bash
npm ci --prefix packages/gaslab
npm --prefix packages/gaslab test
npm pack ./packages/gaslab --pack-destination /path/to/output
npm install /path/to/output/physics-software-sensors-gaslab-0.1.0.tgz
```

[API と使用例](README.md) · [ヘッドレス例](../../examples/headless-gaslab/README.md) · [出典](SOURCE.md) · [受入レビュー](../../docs/gaslab-intake.ja.md)。

速度の直交三成分を独立正規分布から抽出します。速さは自由度 3 の chi 分布、正規化した速さの二乗は chi-square 分布です。温度は正の kelvin を使用し、速度倍率は `sqrt(T2/T1)` です。

既定の `display` は表示スケールで、壁面圧力単位は `simulation` です。Pa と解釈してはいけません。`unitSystem: 'si'` では m/kg/s/K を指定し、表示校正を省略します。速度を質量と Boltzmann 定数から算出し、壁面力積/面積/秒を Pa と表示します。外部 kPa 読値は駆動メタデータに分離します。`T/T0` は理論上の教育倍率です。

`capsule` は直筒長 `cylinderHeight`、下側半球一つ、平らな上面を持つ容器です。面積は `2*pi*r*h + 3*pi*r*r`。粒子間衝突や可動ピストンはありません。境界投影は越境距離を捨てる数値近似です。実機精度・計量性能は未検証です。

`step(dt)` は非負の全秒数を進め、0 は状態を進めません。不正入力や百万を超える内部サブステップは例外になります。粒子スナップショットを独立コピーし、seed 付き reset で初期状態を再現します。

Replay は有限で厳密に増加する秒のタイムスタンプを使い、最初の記録から開始します。各記録境界で区分一定の入力を適用し、倍率は入力時間とシミュレーション時間の両方に作用します。`setReplayPaused(true)` で両方停止します。最終入力は保持します。Seek は入力カーソルのみ変更し、過去の軌跡は復元しません。軌跡再現には reset と最初からの replay を使います。Live 入力は呼出側が供給し、取得器は内蔵しません。固定統計窓は開始直後に衝突のない時間を含みます。

このモデルパッケージは Sensor/Companion Tool に加算しません。現行カタログは 9/4、合計 13。新パッケージを外すか以前のコミットに固定してロールバックできます。
