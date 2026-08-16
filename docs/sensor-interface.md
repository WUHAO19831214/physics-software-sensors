# 统一传感器接口

## 1. 生命周期

所有语言实现都要表达以下逻辑接口：

```text
describe() -> SensorDescriptor
configure(config) -> ConfigResult
start(context) -> None
read() / process(input) -> AsyncIterator[SensorEvent]
health() -> HealthSnapshot
stop() -> None
```

状态机：

```text
created → configured → running → stopping → stopped
             │           │
             └──────────► error
```

### `describe`

纯函数式返回传感器 ID、版本、类别、输入/输出类型、配置 Schema 版本、能力、实现/模型来源和证据等级。不得触发设备权限或加载大型模型。

### `configure`

验证配置并生成不可变的有效配置快照。必须拒绝未知必需字段、越界 ROI 和不支持的模式。敏感字段不得写入普通日志。

### `start`

获取资源并进入 `running`。浏览器屏幕捕获必须由用户动作触发权限；不得声称可静默读取桌面。模型加载失败时应返回明确错误或声明过的降级后端。

### `read` / `process`

- SourceSensor 使用 `read()` 主动产生事件；
- ProcessorSensor 使用 `process(input)` 消费帧；
- 结果应可取消，且不保证硬实时；
- 单次失败应产生 `degraded`、`lost` 或 `error`，不得以 mock 伪装成功。

### `health`

至少返回生命周期状态、最近错误、处理计数、丢失/丢帧计数、实际吞吐率和延迟摘要。健康信息不等于测量事件。

### `stop`

必须幂等，释放摄像头、屏幕流、音频流、线程、worker 和模型资源。停止后不得继续产生新事件。

## 2. 统一上下文

`SensorContext` 至少包含：

| 字段 | 含义 |
| --- | --- |
| `run_id` | 一次实验/基准运行的唯一 ID |
| `clock` | 共享时钟与时间域说明 |
| `artifact_store` | 帧、模型、调试图等外部对象的引用存储 |
| `logger` | 结构化日志接口 |
| `cancellation` | 取消信号 |

## 3. 并发与背压

- 默认单个实例按输入顺序输出，`sequence` 单调递增；
- 实现必须声明队列上限和满队列策略：`block`、`drop-oldest` 或 `drop-newest`；
- 发生丢帧时增加计数并设置 `quality.flags`，不能静默忽略；
- 并行批处理可以改变完成顺序，但输出必须保留输入引用与原始序号。

## 4. 错误模型

| 类别 | 事件状态 | 示例 |
| --- | --- | --- |
| 暂时无目标 | `lost` | 标记离开 ROI |
| 可继续的降级 | `degraded` | YOLO 权重不可用，使用已声明 HOG 回退 |
| 当前样本无效 | `error` | OCR 解析失败、帧损坏 |
| 实例不可运行 | 生命周期 `error` | 权限拒绝、模型无法加载 |

错误至少包含稳定的 `code`、可读 `message`、是否可重试和原因链；不得只依赖异常文本进行程序判断。

## 5. 坐标与 ROI

- ROI 默认使用左上角原点的归一化矩形 `[0,1]`；
- 算法输出像素点时记录图像宽高和方向；
- 镜像预览不应悄悄改变原始测量坐标；
- 物理坐标需要独立标定 ID、单位、变换版本和不确定度；
- `max(y)-min(y)` 应命名为峰—峰范围，不得直接命名为单边振幅。

## 6. 语言骨架

- Python：[`packages/python/src/physics_sensors/core/`](../packages/python/src/physics_sensors/core/)
- TypeScript：[`packages/typescript/src/core/`](../packages/typescript/src/core/)

Phase 1 的 Python `physics_software_sensors` 名称只保留兼容 re-export；新代码使用 `physics_sensors`。语言接口与实验性实现都必须服从 [`contracts/schemas/`](../contracts/schemas/)，不能单独改变公开语义。
