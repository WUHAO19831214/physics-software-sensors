# GasLab と Core サポートの受入

[English](gaslab-intake.md) | [简体中文](gaslab-intake.zh-CN.md) | **日本語**

<!-- section:decision -->
## 判定

ACCEPT: 実験的 Core サポートとヘッドレス気体教育モデルパッケージ、MAINTENANCE。Sensor/Companion Tool 昇格は DEFER。シミュレーションは直接観測ではありません。現行カタログは 9 Sensor + 4 Tool = 13。Core ソースは未公開 0.3.1、gaslab は未公開 0.1.0。registry/Release への公開はありません。

<!-- section:provenance -->
## 出典

[固定出典と MIT レビュー](../packages/gaslab/SOURCE.md)。元 Core コミット `6262fd87a032f2c665a476653f226496688b85f9`、gaslab コミット `5fbade46aa6a819e56c5cb360c87ab0bf9ca7eb5`。レビュー分岐で両方を保持し、元ブランチは書き換えません。

<!-- section:review -->
## レビューと修正

元テスト Core 41、gaslab 17 は通過。しかし -20 ℃ の符号消失、NaN の有効判定、step(1) の 0.1 秒への切捨て、古いスナップショットの変更、Capsule 初期粒子 112/1000 の越境を再現しました。符号/単位、欠損/非有限値/時刻逆行、原点拘束 R²、全時間の進行、コピー、seed reset、幾何と独立壁面反射を修正。単位なし fallback は専用 ROI の明示設定に限定。Replay は入力コピー、検証、記録時刻起点、区分入力と pause を実装し、表示単位圧力と SI 圧力を分離します。

<!-- section:validation -->
## 検証範囲

[検証記録](../benchmarks/results/gaslab-intake.json) · [実行例](../examples/headless-gaslab/README.md)。既存 Sensor 契約と不変 v0.6.0 を保持。合成テストは実機精度の証拠ではありません。Capsule は下側半球一つと平らな上面を持ちます。境界投影で越境距離を捨て、粒子間衝突/可動ピストンはありません。

<!-- section:consumer -->
## 下流状態

[ローカル再利用](../integrations/charles-law-gaslab/README.md)。アプリのテストとビルドは通過しましたが、適用は未コミット。速度抽出/温度倍率と Core を再利用し、描画エンジンと replay UI はアプリ内に残ります。遠隔統合完了や E5 とは扱いません。新 tarball は一時コピーで検証し、元チェックアウトの依存と変更を保持します。

<!-- section:rollback -->
## ロールバックと残件

以前のソース/パッケージに固定するか新パッケージを外します。カタログ昇格には測定入力、来歴、失敗契約と正式受入が必要。下流適用の遠隔受入には変更コミットと固定パッケージハッシュが必要です。既存 draft PR #11 は別の文書ナビゲーション課題です。
