[English](fringelab-toolkit.md) | [简体中文](fringelab-toolkit.zh-CN.md) | [日本語](fringelab-toolkit.ja.md)

<!-- section:overview -->
## FringeLab 再利用コンポーネント

両バッチを `@physics-software-sensors/fringelab` 0.1.0 に収録しました。固定 source は `webcam-laser-fringelab@37a8b3996791790a22980b0d562996a65a3a65ef` で、元アプリは変更しません。電卓、オーバーレイ、画像・カメラ補助機能を個別に利用でき、Next.js は不要です。

<!-- section:catalog -->
## 再利用する機能

電卓は算式パーサーと移動できる React パネルです。ROI は元画像座標で回転・サイズ変更と表示座標変換を行います。仮想定規は端点・本体の移動、角度吸着、磁気整列、mm 目盛りを提供します。校正は人が確認する2点・区分多点です。断面解析はチャンネル、相対 DN、背景減算、飽和品質、平滑化、ピーク・谷、サブピクセル中心、FWHM、自己相関を含みます。自動定規は従来の水平・回転・透視検出、領域指定と手動経路を保持します。ブラウザは画像・HEIC、定規 OCR、カメラ設定とエクスポートを提供します。光学は干渉・回折の逆算、多次数回帰、不確かさと決定的シミュレーションです。

<!-- section:run -->
## 実行と導入

repository root から次のコマンドを実行します。別プロジェクトではローカルでビルドした core と FringeLab の tgz をインストールします。純粋なアルゴリズム、共通契約の Sensor、ブラウザ補助、オプションの React UI は別の entry point です。実行可能なサンプルで組み合わせを確認できます。

```sh
npm --prefix packages/typescript ci
npm --prefix packages/typescript run build
npm --prefix packages/fringelab ci
npm --prefix packages/fringelab test
npm --prefix examples/web-fringelab-toolkit ci
npm --prefix examples/web-fringelab-toolkit run dev
# Local artifacts + clean-install smoke test:
python3 tools/build_fringelab_artifacts.py
```

<!-- section:measurement -->
## 測定手順

650 nm の合成サンプルを読み、30 mm の手動定規を確認して計算します。多点モードでは元画像にアンカーを置き、読み値を編集できます。自動検出・OCR は候補だけを作成し、単位と長さを確認後に適用します。カメラは停止画像を校正します。画像変更で校正を消去し、ROI・パラメータ変更で計算を無効化します。強度は DN・相対応答であり lux や W/m² ではありません。多点写像は1次元で、透視ホモグラフィではありません。飽和したピークの失われた振幅・信頼できる幅は復元できません。

<!-- section:verification -->
## 検証エビデンス

18 ファイルの source hash を固定し、電卓、ROI、手動・自動定規、プロファイル、シミュレーション、逆算の結果を配列・時刻の正規化後に元コードと完全一致させました。元テストと adapter テストは時刻、エラー、中止、古い校正を確認します。production browser で複数電卓、フォーカス復帰、2点・多点校正、自動検出、逆算、390 px レイアウトを確認します。合成・オフライン経路の証拠であり、物理カメラ、実写真誤差分布、光学計量精度は未測定です。

<!-- section:provenance -->
## 来歴と配布

source 所有者の明示的な収録許可により、自有コードは移行先 MIT を適用します。OCR・HEIC の第三者ライセンスは独立して保持します。HEIC はオプションの遅延読込みで、OCR はエンジン・言語リソースを取得する場合があります。npm registry は未公開です。既存 v0.6.0 の7 Sensor Bundle は不変で、新 toolkit tgz と2つの Sensor Bundle はローカルで作成できます。

[Package API](../packages/fringelab/README.md) · [example](../examples/web-fringelab-toolkit/README.md) · [source](../packages/fringelab/SOURCE.md) · [evidence](../benchmarks/results/fringelab-extraction-2026-10-05.md)

![FringeLab production example, synthetic fixture](assets/fringelab-toolkit.png)
