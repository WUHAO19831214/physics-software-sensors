# Getting Started

[English](getting-started.md) | [简体中文](getting-started.zh-CN.md) | **日本語**

<!-- section:choose -->
## 1. 直接観測を選ぶ

pixel には camera/screen capture、表示文字列には OCR、画像上の位置・bbox には tracker を選びます。変位、力、周波数、角度が必要なら、下流の校正・導出 chain を別途記録します。

<!-- section:download -->
## 2. ダウンロードして確認する

[`v0.6.0` Experimental Release](https://github.com/WUHAO19831214/physics-software-sensors/releases/tag/v0.6.0) を取得し、`SHA256SUMS` を確認してから[インストール](installation.ja.md)します。registry package はありません。

<!-- section:run -->
## 3. 独立 example を実行する

対象の [Sensor Page](sensor-catalog.ja.md) を開き、宣言された依存関係だけを導入して小さな example を実行します。Recorded/synthetic example は元アプリからの分離を示しますが、実機精度の証拠ではありません。

### センシング後：測定値を処理する

導出表現が必要な場合は、独立した [Companion Tool Catalog](tool-catalog.ja.md)へ進みます。例として、`screen.capture → ocr.number → vector.compose-3d` は画面表示のスカラー成分から追跡可能な3次元合成ベクトルを構成します。この Tool は新しい観測を作らず、現在の未リリース Tool source は `v0.6.0` に含まれません。

<!-- section:interpret -->
## 4. 保守的に解釈する

統合前に Evidence、Maturity、Known Limitations、Benchmark、Provenance を確認します。下流比較が成功するまで、ソースプロジェクトの旧経路と rollback を残します。
