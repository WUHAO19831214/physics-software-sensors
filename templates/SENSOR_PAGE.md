# <English Sensor Name>

## <中文名称>

> 一句话说明普通物理教师能理解的直接观测能力。

**状态：** contract-only / experimental / validated / stable
**Sensor ID：** `<sensor-id>`
**实现版本：** `<version>`

## 典型物理实验用途

说明真实来源项目中的实验情境、图像直接观测量，以及标定后才能得到的物理量。明确写出不能从直接观测推出的结论。

## 来源项目

| 项目 | 仓库 | commit | 原实现文件 | 原始类/函数 | 用途 |
| --- | --- | --- | --- | --- | --- |
|  |  | 完整 40 位 SHA |  |  |  |

## 工作原理

```text
输入 → 处理步骤 → 质量判断 → SensorEvent
```

用非程序员也能理解的语言解释每一步。

## 输入

- 输入帧/数据；
- ROI、阈值、模板或模型等配置；
- 颜色空间、坐标和时间假设。

## 输出

列出核心 measurement、payload、状态和质量标志，并给一个真实契约 JSON 示例。

## 使用效果

优先引用 `assets/` 内有完整来源记录的真实图片；没有时明确写 `demo asset pending`，不要伪造。

## 最小调用示例

示例必须与成熟度一致；未实现的 API 必须标注“目标 API，不可运行”。

## 当前成熟度

解释页面完整度与实现/验证成熟度的区别。

## 已知限制

列出测量语义、环境依赖、时间/坐标、算法失效和验证证据边界。

## Benchmark

链接本目录 `benchmarks/README.md`。

## Provenance

链接 `SOURCE.md` 和机器可读 `sensor.json`。
