# Companion Tool カタログ

[English](tool-catalog.md) | [简体中文](tool-catalog.zh-CN.md) | **日本語**

<!-- section:catalog -->
## カタログ

Companion Tool（補助処理ツール）は既存の観測・測定値を処理します。新しい直接観測を作らず、Sensor 数にも含めません。

| Tool | 用途 | 言語 | 状態 | ソース | Example | 文書 |
| --- | --- | --- | --- | --- | --- | --- |
| [`vector.compose-3d`](../processing/vector.compose-3d/README.ja.md) | source 情報を持つ x/y/z スカラー成分から3次元ベクトルと任意の render model を構成 | TypeScript | `experimental` `0.1.0` | 延安アンペール力教師用アプリ | [Web demo](../examples/web-vector-compose-3d/README.md) | [来歴](../processing/vector.compose-3d/SOURCE.md) |
| [`calibration.scale-1d`](../processing/calibration.scale-1d/README.ja.md) | 人が確認する2点・区分多点1次元校正 | TypeScript | experimental 0.1.0 | FringeLab | [Web demo](../examples/web-fringelab-toolkit/README.md) | [Source](../processing/calibration.scale-1d/SOURCE.md) |
| [`signal.profile-features`](../processing/signal.profile-features/README.ja.md) | 平滑化、背景減算、ピーク幅・周期解析 | TypeScript | experimental 0.1.0 | FringeLab | [Web demo](../examples/web-fringelab-toolkit/README.md) | [Source](../processing/signal.profile-features/SOURCE.md) |
| [`optics.fringe-wavelength`](../processing/optics.fringe-wavelength/README.ja.md) | 干渉・回折の波長逆算、回帰と不確かさ | TypeScript | experimental 0.1.0 | FringeLab | [Web demo](../examples/web-fringelab-toolkit/README.md) | [Source](../processing/optics.fringe-wavelength/SOURCE.md) |

<!-- section:status -->
## 状態境界

リポジトリ構成は **9 Sensor · 4 Companion Tool** です。本ツールは不変の `v0.6.0` 以降の未リリース開発であり、その Release には含まれず、Sensor の maturity や evidence も変更しません。
