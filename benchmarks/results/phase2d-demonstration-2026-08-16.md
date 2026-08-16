# Phase 2D demonstration verification — 2026-08-16

## Scope

本结果只覆盖 standalone synthetic fixtures 和 clean-install smoke test，不代表真实摄像头、真实设备屏幕或物理测量精度。

## Color Marker

- standalone sequence：`ok → lost → ok`；
- 生成 overview、processing、lost/reacquire PNG 和三个完整 SensorEvent；
- 固定来源比较仍为 4/4，绝对容差 `1e-6`；
- demo 中像素尺明确标注不是物理标定。

## Number OCR

环境：Node.js `24.13.0`、Tesseract.js `7.0.0`，synthetic PNG，`eng`、`SINGLE_WORD`、whitelist `0123456789.+-`。

| Case group | Result |
| --- | --- |
| `+1.25`, `-2.33`, `0.00` | 3/3 parsed value exact match |
| blank, alphabetic | 2/2 explicit `OCR_PARSE_FAILED`, no measurement |
| controlled encoder failure | 1/1 explicit `OCR_RECOGNITION_FAILED`, no measurement |

一次示例运行记录的端到端识别耗时为 224/65/63 ms；它包含首个 worker warm-up，且仅用于复现本机运行，不作为性能承诺。

## Packaging

- Python wheel 在新 venv 中安装，`ColorMarkerSensor` import 和处理 smoke test 通过；
- TypeScript `.tgz` 在新 npm consumer 中安装，`NumberOCRSensor` 与 `TesseractJsRecognizer` package import 及像素 OCR smoke test 通过；
- 未发布 PyPI、npm registry 或 GitHub Release。

## Repository regression

- repository validation：23 个受版本控制 JSON、7 个 Sensor Page/manifest、pilot assets 与本地链接通过；
- Python：27/27 tests passed；
- TypeScript/Node：13/13 tests passed，其中包含真实 Tesseract.js pixel integration；
- source comparison：4/4 cases matched，绝对容差 `1e-6`。
