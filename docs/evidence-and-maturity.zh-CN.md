# 证据等级与成熟度

[English](evidence-and-maturity.md) | **简体中文** | [日本語](evidence-and-maturity.ja.md)

<!-- section:evidence -->
## 证据等级

| 等级 | 含义 |
| --- | --- |
| E0 | 只有契约/Schema |
| E1 | 确定性的 synthetic 或 recorded replay |
| E2 | 固定来源兼容/golden 对比 |
| E3 | 真实 OCR/CV/runtime 在受控像素上运行 |
| E4 | 指明真实设备/实验室设置和可复现数据集 |
| E5 | 下游项目固定版本接入并保留 rollback |

Recorded output 不是真实 runtime；synthetic pixels 不是真实设备。缺失证据写 `not measured`，不能写成零。

<!-- section:maturity -->
## 成熟度

- `contract-only`：不要求本仓库实现。
- `experimental`：已有 adapter 和确定性测试，但重要验证可能仍未完成。
- `validated`：适用的真实环境、指标和支持路径许可证门禁已通过。
- `stable`：validated public API 已具备下游固定版本复用、回退和兼容承诺。

<!-- section:separation -->
## 证据等级 ≠ 成熟度

证据记录“实际跑过什么”；成熟度是实现、可复现性、指标、许可证、文档和复用共同形成的发布决策。E3 或 E5 都不会自动变成 validated。当前七项 Sensor 均为 experimental；`tracker.spot-centroid` 已有 E5 下游复用证据，但所有 Sensor 都还没有 E4 真实设备/实验室证据。

维护者详版：[证据等级](evidence-levels.md) · [成熟度门禁](maturity-gates.md)。
