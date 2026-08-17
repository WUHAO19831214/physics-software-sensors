# 新 Sensor 长期接入流程

[English](sensor-intake.md) | **简体中文** | [日本語](sensor-intake.ja.md)

<!-- section:purpose -->
## 目的

这套可重复流程把项目中成熟的传感能力纳入本仓库，同时不破坏来源项目，也避免仓库变成无边界的 utils 集合。

<!-- section:qualification -->
## 什么值得成为 Sensor？

候选能力应满足多数条件：已在真实项目使用；输入/输出/边界明确；可脱离 UI/业务状态；有跨项目价值；可做确定性测试；能完整追溯；依赖/资产可合法分发；与物理实验传感或观测直接相关。

页面布局、课程按钮/文本、图表、单项目 store/database、设备流程 orchestration、不可独立测试的 helper 和无关通用工具不应进入。

<!-- section:decision -->
## 接入决定

- `ACCEPT`：边界、复用、来源、合法性和测试路径足够，进入 extraction。
- `DEFER`：有价值，但来源行为、证据、许可证或边界尚未成熟。
- `REJECT`：不是 Sensor、不可复用/测试，或不适合本仓库；必须记录原因。

<!-- section:lifecycle -->
## 生命周期

```text
candidate → accepted → contract-only → incubating → experimental
          → validated → stable → deprecated
```

`candidate/accepted` 是 intake 状态；后续状态映射现有 contract/maturity 字段，不修改当前 schema enum。Evidence E0–E5 始终独立。

<!-- section:workflow -->
## 标准流程

1. 填写 [`SENSOR_PROPOSAL.md`](../templates/SENSOR_PROPOSAL.md)。
2. 固定仓库、完整 commit SHA、路径/符号、真实物理用途和许可证状态。
3. 给出 `ACCEPT`、`DEFER` 或 `REJECT` 及理由。
4. 对 ACCEPT 项使用 `tools/new_sensor.py` 只生成诚实的 TODO 骨架。
5. 在公共 core 后抽取 adapter，保持来源 UI/业务行为不变。
6. 建立 L0 contract、L1 deterministic fixture、L2 source golden/replay 和适用 L3/L4，禁止虚构结果。
7. 补齐 EN/ZH-CN/JA 页面、示例、真实 demo 或 pending、benchmark、依赖/许可证审计、clean install、bundle 和 CHANGELOG。
8. 只按[证据与成熟度](evidence-and-maturity.zh-CN.md)门禁升级；下游保留 rollback。

<!-- section:observation-boundary -->
## 直接观测与派生物理量

Proposal 必须把 `camera frame`、`screen pixels`、`OCR text`、`pixel centroid`、`bbox` 等直接观测，与位移、速度、力、振幅、频率、角度等下游物理量分开。不能用 Sensor 名称暗示推导、单位、标定或不确定度已经成立。

<!-- section:required-deliverables -->
## 进入 experimental 前的强制交付

EN/ZH/JA Sensor Page、`sensor.json`、`SOURCE.md` 与来源 commit、独立 adapter、deterministic 与 golden/replay tests、example、非伪造 demo 证据、benchmark、evidence/maturity、依赖/许可证审计、clean install、Sensor Bundle、CHANGELOG。缺项不能宣称 Phase complete。

<!-- section:handoff -->
## Agent Handoff

Intake 期间 `.agent-handoff/latest.json` 可包含 `sensor_intake`：candidate ID、decision/reason、source repository/SHA。没有 intake 时为 `null`，保持向后兼容。
