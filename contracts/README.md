# 机器可读契约

## Schema

| 文件 | 用途 |
| --- | --- |
| `sensor-event.schema.json` | 所有测量/追踪/OCR 结果的统一事件信封 |
| `frame-packet.schema.json` | 摄像头、屏幕等采集源的帧引用 |
| `sensor-manifest.schema.json` | `sensors/*/sensor.json` 能力与来源清单 |
| `benchmark-result.schema.json` | 基准运行摘要 |

当前 Schema 版本均从 `1.0.0` 开始并保持不变；实现包按独立 SemVer 演进（Python 当前 `0.4.0`，TypeScript 当前 `0.3.0`）。Schema 使用 JSON Schema Draft 2020-12。

## 兼容性

- 生产者必须写出所有必需字段；
- 消费者应容忍当前 MAJOR 中新增的可选字段；
- `additionalProperties: false` 的稳定结构不能私自增加字段；算法调试扩展放入 `payload`；
- 二进制内容通过 artifact 引用，不直接写 base64；
- 示例必须通过对应 Schema。

## 示例

- [`spot-centroid-event.json`](examples/spot-centroid-event.json)
- [`screen-frame-packet.json`](examples/screen-frame-packet.json)
- [`benchmark-result.json`](examples/benchmark-result.json)
