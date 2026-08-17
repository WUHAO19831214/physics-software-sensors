# 最初の完全な再利用ループ

[English](first-reuse-loop.md) | [简体中文](first-reuse-loop.zh-CN.md) | **日本語**

<!-- section:loop -->
## ループ

```text
光スポット振動 project
      ↓
trackRedSpot の source behavior
      ↓
tracker.spot-centroid
      ↓
Physics Software Sensors v0.6.0
      ↓
公開 wheel
      ↓
merge 済みの光スポット振動 project 統合
      ↓
legacy/library 比較 + rollback
      ↓
E5 の下流再利用を実証
```

<!-- section:meaning -->
## 実証したこと

物理 project で実際に使われた能力を、固定した provenance に基づいて抽出・公開し、version 固定された依存関係と rollback 可能な adapter により source project で再利用しました。Merge 後も既定経路は `legacy` で、`library` と `compare` は明示的に選択する offline replay mode です。

Historical source commit `7f0d91cc73afafaecc54acc46b2b9d69375d994a` はアルゴリズムの由来を示し、downstream merge commit `172429fae463274ee354e54d56400096c2c6d375` は公開 library の再利用先を示します。この二つは異なるエビデンスです。

<!-- section:boundary -->
## 科学的な境界

これは**ソフトウェア再利用ループ**であり、物理計測精度の検証ではありません。7 個の synthetic same-frame case、下流計算の回帰、rollback は通過しました。実 camera、制御された光学変位、exposure robustness、repeatability、不確かさは E4 の課題として残るため、E5 があっても `tracker.spot-centroid` の maturity は `experimental` のままです。

詳細: [光スポット振動 integration record](../integrations/spot-vibration/README.md)。
