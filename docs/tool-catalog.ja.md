# Companion Tool カタログ

[English](tool-catalog.md) | [简体中文](tool-catalog.zh-CN.md) | **日本語**

<!-- section:catalog -->
## カタログ

Companion Tool（補助処理ツール）は既存の観測・測定値を処理します。新しい直接観測を作らず、Sensor 数にも含めません。

| Tool | 用途 | 言語 | 状態 | ソース | Example | 文書 |
| --- | --- | --- | --- | --- | --- | --- |
| [`vector.compose-3d`](../processing/vector.compose-3d/README.ja.md) | source 情報を持つ x/y/z スカラー成分から3次元ベクトルと任意の render model を構成 | TypeScript | `experimental` `0.1.0` | 延安アンペール力教師用アプリ | [Web demo](../examples/web-vector-compose-3d/README.md) | [来歴](../processing/vector.compose-3d/SOURCE.md) |

<!-- section:status -->
## 状態境界

リポジトリ構成は **7 Sensor · 1 Companion Tool** です。本ツールは不変の `v0.6.0` 以降の未リリース開発であり、その Release には含まれず、Sensor の maturity や evidence も変更しません。
