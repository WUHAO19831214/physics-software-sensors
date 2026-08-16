# 统一数据格式

## 1. 格式与编码

- 控制面与事件：UTF-8 JSON；
- 时间：RFC 3339 UTC 字符串 + 会话单调纳秒；
- 表格导出：UTF-8 CSV，列名使用稳定的 snake_case；
- 大型帧、音视频、模型和调试图：外部文件/对象，事件内保存 URI、媒体类型、字节数和 SHA-256；
- 契约版本：`schema_version` 使用 SemVer。

语言运行时可以把实际 pixel buffer 与 FramePacket metadata 临时绑定，但该 buffer 不是 JSON 字段；持久化、跨进程或跨语言传输仍使用 artifact URI/hash。

## 2. `SensorEvent` 信封

| 字段 | 必需 | 说明 |
| --- | --- | --- |
| `schema_version` | 是 | 事件 Schema 版本 |
| `event_id` | 是 | 全局唯一事件 ID |
| `run_id` | 是 | 一次采集/基准运行 ID |
| `sensor` | 是 | ID、实例 ID、版本和类别 |
| `sequence` | 是 | 该实例内单调递增序号 |
| `time` | 是 | 观测、发出、源时间与时钟质量 |
| `status` | 是 | `ok/degraded/lost/error` |
| `quality` | 是 | 置信度、延迟、丢帧、质量标志 |
| `measurements` | 是 | 零个或多个带单位观测值 |
| `coordinate_frame` | 否 | 位置/边界框存在时必需 |
| `artifacts` | 否 | 输入帧、调试图等外部引用 |
| `parent_event_ids` | 否 | 上游事件 ID |
| `payload` | 否 | 算法特有的可扩展元数据 |

完整约束见 [`sensor-event.schema.json`](../contracts/schemas/sensor-event.schema.json)。

## 3. 时间语义

`observed_at` 是观测对应的墙钟时间，`emitted_at` 是处理结果发出时间。`monotonic_ns` 用于同一进程/浏览器会话内稳定计算间隔；它不能直接跨机器比较。

`clock` 必须说明：

- `domain`：`system`、`browser-performance`、`camera-source` 或自定义；
- `sync_status`：`unknown`、`single-clock`、`estimated`、`hardware-synced`；
- `uncertainty_ms`：已知时填写，不知道时不推测。

最近邻融合必须保存 `time_diff_ms` 和容差。稳定采集版当前采用音频节奏、0.15 秒内最近视觉帧的做法，可作为一个适配器策略，但不是统一接口的固定算法。

## 4. Measurement 规则

```json
{
  "name": "centroid_y",
  "value": 241.75,
  "value_type": "number",
  "unit": "px",
  "role": "raw",
  "uncertainty": null
}
```

- `role`: `raw`、`filtered`、`derived`、`calibrated`；
- SI 单位优先；像素用 `px`，无量纲用 `1`；
- dBFS 不得写成 dB SPL；
- 设定频率使用 `frequency_setpoint_hz`，实测频率使用 `frequency_measured_hz`；
- OCR 原文放 `payload.raw_text`，解析后的数值放 measurement；
- 没有有效观测时 measurements 可以为空，但状态不得为 `ok`。

## 5. 坐标系

| `space` | 典型单位 | 说明 |
| --- | --- | --- |
| `image-pixel` | `px` | 原始帧像素坐标，左上为原点 |
| `image-normalized` | `1` | `[0,1]` 归一化坐标 |
| `calibrated-2d` | `m/cm/mm` | 经标定映射的平面坐标 |
| `world-3d` | `m` | 经外参/三角测量得到的世界坐标 |

凡出现 `center_x`、`center_y`、bbox、位移或轨迹，都必须能解析到一个坐标系。二维比例尺仅在标尺与运动同平面、相机固定等假设下有效。

## 6. 状态与质量标志

建议的稳定标志包括：

- `permission-required`
- `frame-dropped`
- `target-lost`
- `low-confidence`
- `fallback-backend`
- `roi-out-of-bounds`
- `ocr-parse-failed`
- `calibration-missing`
- `timestamp-estimated`
- `mock-data`

新增标志必须使用小写 kebab-case，并在版本记录中说明。

## 7. CSV 投影

CSV 是事件的有损投影，不是主契约。导出时至少保留：

```text
schema_version,event_id,run_id,sensor_id,sensor_version,sequence,
observed_at,monotonic_ns,status,quality_confidence,quality_flags,
measurement_name,measurement_value,measurement_unit,measurement_role
```

一个事件含多个 measurement 时采用长表（一项 measurement 一行），避免不同传感器不断扩展宽表列。
