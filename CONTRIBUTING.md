# 贡献指南

## 变更类型

- **文档/契约**：澄清接口、字段、语义或验证规则；
- **传感器适配器**：把来源仓库的现有实现包在统一接口之后；
- **算法升级**：改变检测、追踪、OCR 或采集行为；
- **基准数据/结果**：增加可复现数据集、真值、运行记录或报告。

## 必须遵守

1. 不直接修改本仓库之外的来源项目。
2. 不复制来源代码，除非已核查许可证并在升级记录中注明来源 commit 和文件。
3. mock 或占位实现不得输出 `status: "ok"` 的正式测量事件。
4. 原始值、后处理值和物理换算值使用不同 measurement 名称并记录处理链。
5. 二进制数据默认使用 URI + SHA-256 引用，不嵌入事件 JSON。
6. 新增或改变公开契约时，更新版本、示例、Schema、测试和升级记录。

## 提交前检查

```bash
python3 tools/validate_repo.py
pytest
npm --prefix packages/typescript test
```

算法或适配器变更还应附上：

- 完整来源 commit；
- 适用设备与环境；
- 基准协议与结果；
- 行为变化和回退方式；
- 隐私、许可证与模型权重说明。

模板位于 [`templates/`](templates/README.md)。

## Adding a new Sensor

普通 bugfix、文档修正和现有 adapter 的兼容性修复不需要完整 intake。新增 Sensor 或重大可复用能力必须先走标准流程：

1. 阅读 [Sensor Intake](docs/sensor-intake.md) 和 [Sensor ID naming](docs/sensor-naming.md)。
2. 填写 [Sensor Proposal](templates/SENSOR_PROPOSAL.md)，固定完整来源 commit、文件/符号、物理用途、直接观测与派生物理量。
3. 记录 `ACCEPT`、`DEFER` 或 `REJECT`；只有 ACCEPT 才进入 scaffold/extraction。
4. 遵守 [i18n style guide](docs/i18n/style-guide.md) 与 [terminology](docs/i18n/terminology.md)，提供 EN/ZH-CN/JA Sensor Page。
5. 按 [benchmarking](docs/benchmarking.md)、[evidence/maturity](docs/evidence-and-maturity.md) 和 [licensing/provenance](docs/licensing-and-provenance.md) 完成证据门禁。
6. 使用 `python tools/new_sensor.py --help` 生成 TODO 骨架；generator 不会替代来源审查，也不会把候选能力自动提升为 experimental。

给 Codex 的完整执行顺序见 [add-new-sensor recipe](docs/agent-recipes/add-new-sensor.md)，可复制提示词见 [ADD_SENSOR_PROMPT](templates/ADD_SENSOR_PROMPT.md)。
