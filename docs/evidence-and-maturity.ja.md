# エビデンスレベルと成熟度

[English](evidence-and-maturity.md) | [简体中文](evidence-and-maturity.zh-CN.md) | **日本語**

<!-- section:evidence -->
## エビデンスレベル

| Level | 意味 |
| --- | --- |
| E0 | 契約・Schema のみ |
| E1 | 決定的な synthetic / recorded replay |
| E2 | 固定ソースとの互換性・golden 比較 |
| E3 | 制御された pixel 上で実 OCR/CV/runtime を実行 |
| E4 | 特定した実機・実験室条件と再現可能 dataset |
| E5 | rollback を備えた下流 project の version 固定統合 |

Recorded output は実 runtime ではなく、synthetic pixels は実機ではありません。未取得の証拠はゼロではなく `not measured` とします。

<!-- section:maturity -->
## 成熟度

- `contract-only`: 本 repository の実装は必須ではない。
- `experimental`: adapter と決定的テストはあるが、重要な検証が未完の場合がある。
- `validated`: 対象となる実環境、指標、対応経路のライセンス gate を通過済み。
- `stable`: validated public API に加え、下流での version 固定再利用、rollback、互換性を保証。

<!-- section:separation -->
## Evidence Level ≠ Maturity

エビデンスは「実行した経路」、成熟度は実装・再現性・指標・ライセンス・文書・再利用を含む release 判断です。E3 や E5 だけで validated にはなりません。現在の 7 Sensor はすべて experimental のままです。`tracker.spot-centroid` には E5 の下流再利用エビデンスがありますが、E4 の実機・実験室エビデンスを持つ Sensor はありません。

保守者向け詳細: [Evidence Levels](evidence-levels.md) · [Maturity Gates](maturity-gates.md)。
