# 新規 Sensor Intake ワークフロー

[English](sensor-intake.md) | [简体中文](sensor-intake.zh-CN.md) | **日本語**

<!-- section:purpose -->
## 目的

プロジェクト内で成熟した sensing 機能を、ソースプロジェクトを壊さず本 repository に移す再現可能な手順です。同時に、無関係な utils の集合になることを防ぎます。

<!-- section:qualification -->
## Sensor に値する条件

実プロジェクトでの利用、明確な input/output/boundary、UI・business state からの分離、複数 project での価値、決定的 test、完全な来歴、合法的に扱える依存・asset、物理実験の sensing/observation との直接関係、の多くを満たす必要があります。

Layout、授業専用 button/text、chart UI、単一 project の store/database、device workflow orchestration、独立 test できない helper、無関係な utility は対象外です。

<!-- section:decision -->
## Intake decision

- `ACCEPT`: boundary、reuse、provenance、legal/test path が抽出に十分。
- `DEFER`: 有用だが source behavior、evidence、license、boundary が未成熟。
- `REJECT`: Sensor ではない、再利用・test 不可、または本 repository に不適切。理由を記録する。

<!-- section:lifecycle -->
## ライフサイクル

```text
candidate → accepted → contract-only → incubating → experimental
          → validated → stable → deprecated
```

`candidate/accepted` は intake state、後続は既存 contract/maturity field への mapping です。現 schema enum は変更せず、Evidence E0–E5 も別に扱います。

<!-- section:workflow -->
## 標準手順

1. [`SENSOR_PROPOSAL.md`](../templates/SENSOR_PROPOSAL.md) を記入。
2. Repository、完全 commit SHA、path/symbol、実際の物理用途、license state を固定。
3. `ACCEPT`、`DEFER`、`REJECT` と理由を決定。
4. ACCEPT の場合のみ `tools/new_sensor.py` で正直な TODO scaffold を作成。
5. 共通 core の背後へ adapter を抽出し、元 UI/business behavior は変更しない。
6. L0 contract、L1 deterministic fixture、L2 source golden/replay、必要な L3/L4 を追加し、結果を捏造しない。
7. EN/ZH-CN/JA page、example、実 demo または pending、benchmark、dependency/license audit、clean install、bundle、CHANGELOG を揃える。
8. [Evidence and Maturity](evidence-and-maturity.ja.md) gate のみで昇格し、下流 rollback を残す。

<!-- section:observation-boundary -->
## 直接観測と導出物理量

Proposal は `camera frame`、`screen pixels`、`OCR text`、`pixel centroid`、`bbox` と、変位、速度、力、振幅、周波数、角度を分離します。Sensor 名だけで derivation、unit、校正、不確かさを成立させません。

<!-- section:required-deliverables -->
## experimental 前の必須成果

EN/ZH/JA Sensor Page、`sensor.json`、`SOURCE.md` と source commit、standalone adapter、deterministic/golden replay test、example、捏造しない demo evidence、benchmark、evidence/maturity、dependency/license audit、clean install、Sensor Bundle、CHANGELOG。欠落があれば Phase complete としません。

<!-- section:handoff -->
## Agent handoff

Intake 中は `.agent-handoff/latest.json` に candidate ID、decision/reason、source repository/SHA の `sensor_intake` を追加できます。Intake がない場合は backward-compatible な `null` とします。
