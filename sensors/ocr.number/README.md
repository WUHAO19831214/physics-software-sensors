# Number OCR Sensor

## 数字 OCR 软件传感器

> 从用户授权的屏幕或录制图像中裁定一个数字区域，保留 OCR 原文并解析出数值，用于读取实验设备原软件已经显示在屏幕上的读数。

**状态：experimental**
**Sensor ID：** `ocr.number`
**实现版本：** `0.2.0`

## 典型物理实验用途

多源实验桥和安培力教师端使用浏览器 `getDisplayMedia` 获取用户选择的实验软件窗口，再对力传感器通道 ROI 运行 Tesseract.js。它的真实链路是：

```text
力传感器 → 原设备/软件 → 屏幕显示 → 用户授权的屏幕像素 → OCR → 数值
```

因此本传感器直接观测的是**屏幕 ROI 中的数字图像和 OCR 文本**，不是朗威 DIS 或其他设备 SDK 的内部数据。单位、通道含义、零点和物理范围由调用方配置并验证。

## 来源项目

| 项目 | 仓库 | commit | 原实现文件 | 原始类/函数 | 用途 |
| --- | --- | --- | --- | --- | --- |
| 多源实验桥 | [`physics-experiment-bridge-mvp`](https://github.com/WUHAO19831214/physics-experiment-bridge-mvp) | `8bba87df6475cae1e595fc925551db8bea83fb68` | `src/recognizers/TesseractRecognizer.ts` | `TesseractRecognizer.recognize` | 对屏幕 OCR ROI 运行本地 Tesseract.js，保留 rawText/value/confidence/duration/warning |
| 同上 | 同上 | 同上 | `src/utils/extractNumber.ts` | `normalizeOcrText`、`extractNumberFromText` | OCR 易混字符归一化与普通十进制解析 |
| 同上 | 同上 | 同上 | `src/utils/imagePreprocess.ts`、`ocrPreprocess.ts` | `cropRoiFromVideo`、`preprocessForNumberRecognition`、`preprocessForLangweiNumber` | ROI 裁剪、放大、灰度/阈值和去噪 |
| 同上 | 同上 | 同上 | `src/screen/ScreenCapturePanel.tsx` | `ScreenCapturePanel` 内采样循环 | 屏幕授权、ROI、OCR、过滤和 store 的原业务编排 |
| 安培力教师端 | [`ampere-force-visualizer-teacher-yanan`](https://github.com/WUHAO19831214/ampere-force-visualizer-teacher-yanan) | `cb073e89d6d87129287030f1df08bd540504eb39` | 同名 recognizer/utils/screen 文件 | 同上 | 读取 Fy/Fz 屏幕显示并服务教师端可视化 |

两个来源 commit 中五个核心 OCR/解析/预处理文件的 SHA-256 完全一致，详见 [SOURCE.md](SOURCE.md)。

## 工作原理

```text
recorded FramePacket / 以后接入 screen FramePacket
  ↓
验证归一化 OCR ROI 和帧尺寸
  ↓
Recognizer seam（本轮：固定 recorded result 回放；后续：Tesseract.js）
  ↓
保留 rawText、confidence、duration、warning/error
  ↓
按来源规则归一化易混字符并提取普通十进制
  ↓
成功：measurement + SensorEvent
失败：空 measurements + error，绝不回退 mock 数字
```

本轮故意不碰 React UI、`getDisplayMedia` 或真实 Tesseract worker。先把 ROI→recognizer→parse→event 的可测试边界固定下来。

## 输入

- recorded/screen/image `FramePacket` 的 ID、run ID、观测时间、单调时间、尺寸和 artifact URI；
- `[0,1]` 归一化 OCR ROI；
- 通道名称、符号和单位；
- 实现 `NumberRecognizer` 的识别后端；
- 本轮测试后端为 `RecordedNumberRecognizer`，按 frame/ROI 回放已记录的 raw OCR 结果。

真实 Tesseract 后端未来还需要 ImageData 裁剪、预处理、worker 生命周期和语言/model artifact 记录。

## 输出

成功事件至少保留：

- measurement：`recognized_value`；
- `payload.raw_text` 与 `payload.normalized_text`；
- `payload.confidence`、`payload.duration_ms`、`payload.warning`；
- ROI、recognizer ID 和 frame parent ID。

```json
{
  "sensor": {"id": "ocr.number", "version": "0.2.0", "category": "processor"},
  "status": "ok",
  "quality": {"confidence": 0.94, "latency_ms": 42, "flags": ["recorded-replay"], "dropped_since_last": 0},
  "measurements": [
    {"name": "recognized_value", "value": -2.33, "value_type": "number", "unit": "N", "role": "derived", "uncertainty": null}
  ],
  "payload": {"raw_text": "-2.33", "normalized_text": "-2.33", "recognizer": "tesseract"}
}
```

若 rawText 无法解析，输出 `status: "error"`、`OCR_PARSE_FAILED` 和 `ocr-parse-failed`；如果 recognizer 本身失败，输出 `OCR_RECOGNITION_FAILED`。两种情况都没有数值 measurement。

完整、通过 SensorEvent Schema 的 replay 输出见 [`examples/recorded-success-event.json`](examples/recorded-success-event.json)。

## 使用效果

**Demo asset pending。** 两个来源 commit 没有提交屏幕/OCR 截图；本轮没有复制校徽或伪造实验软件界面。后续应在用户授权的真实屏幕采集流程中生成“屏幕帧 / ROI / 预处理 / OCR 调试结果”组合图。见 [assets/README.md](assets/README.md)。

## 最小调用示例

```ts
import { NumberOCRSensor, RecordedNumberRecognizer } from '@physics-software-sensors/core';

const recognizer = new RecordedNumberRecognizer(recordedResults);
const sensor = new NumberOCRSensor(recognizer);
sensor.configure({ roiId: 'force-y', roi: { x: 0.36, y: 0.535, width: 0.28, height: 0.05 }, unit: 'N' });
await sensor.start({ runId: 'experiment-001' });

const event = await sensor.processFrame(recordedFramePacket);
console.log(event.payload.raw_text, event.measurements);
await sensor.stop();
```

这段示例在 Phase 2C 的 recorded replay 范围内可运行；真实 `TesseractJsRecognizer` 尚未迁入新包。见 [examples/README.md](examples/README.md)。

## 当前成熟度

`experimental` / manifest `incubating`：解析规则、ROI 验证、统一事件映射和 recorded-result replay 已可独立测试；真正的像素裁剪/预处理/Tesseract.js backend、浏览器兼容和准确率数据尚未迁移，因此不能声称新包已经完成 OCR。

## 已知限制

- 当前新包只回放已记录 recognizer 结果，不执行真实 Tesseract 推理；
- 来源 whitelist 为 `0123456789.-`，不支持科学计数法；
- 来源易混字符规则会把单词中的 `o/O` 变成 `0`；必须保留 rawText，并用物理范围/上下文防止误接受；
- OCR 置信度是引擎元数据，不是物理测量置信区间；
- 屏幕缩放、字体、背景线、颜色和刷新方式会影响真实识别；
- OCR 后处理误差必须与设备传感器本身误差分开报告；
- 失败不会自动回退到 mock，也不会沿用上次有效数值作为当前测量。

## Benchmark

见 [benchmarks/README.md](benchmarks/README.md)。当前只验证 parser/source fixture、事件语义和失败路径；exact match、数值误差与真实 latency 仍待真实 recorded frames。

## Provenance

- [SOURCE.md](SOURCE.md)
- [sensor.json](sensor.json)
- [仓库级来源盘点](../../docs/source-inventory.md)
