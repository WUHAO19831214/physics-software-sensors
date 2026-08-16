# Dataset Card：OCR Number Synthetic Pixels

## Identity

- dataset ID：`ocr-number-synthetic-pixels`
- generator：`examples/web-number-ocr/generate_samples.py`
- manifest：`examples/web-number-ocr/sample/manifest.json`
- samples：6 个 PNG；800×300 RGBA 解码输入
- privacy：无人物、无设备数据、无学校标识

## Purpose

证明独立包可以完成 pixel frame → normalized ROI crop → preprocessing → Tesseract.js → parse → SensorEvent，并覆盖正数、负数、零、parse failure 和 controlled recognizer failure。

## Evidence boundary

所有图片均为 synthetic generic screen frames，不是朗威设备截图或真实实验测量。3/3 数字成功率只能描述这三个固定 fixture，不能外推成 OCR 准确率或设备兼容性。

## Cases

| ID | Visible content | Expected outcome | PNG SHA-256 |
| --- | --- | --- | --- |
| `positive` | `+1.25` | value `1.25` | `d8ad43b58e98ad64d0dc0fadf0e9b7c2085f469a28d5c310cdf9c118e0764ba3` |
| `negative` | `-2.33` | value `-2.33` | `8c2c36dcacf483ee7404754c23008108faa21da1e9396e15ef3af9e2c5b58ed8` |
| `zero` | `0.00` | value `0` | `bc5fce29d06f5fa3246822858a5c4773c5e07005cb2238f9d916f2a1044ab749` |
| `blank` | empty display | `OCR_PARSE_FAILED` | `187df67dde35f293787cf7501717d994f9fe6ff133fc748b57484f20cc6f5aec` |
| `alphabetic` | `READY` | `OCR_PARSE_FAILED` | `0671d5c201299b143b3547f0243d206f6b59e0ecacce434a3fe7e85c9513a965` |
| `engine-failure` | `9.99` | controlled encoder failure → `OCR_RECOGNITION_FAILED` | `ea2451b02b945ccd171f88f9e84bcf6cc563e0551dcd79631e9cf2584d3edaf3` |

## Reproduction

```bash
python examples/web-number-ocr/generate_samples.py
npm --prefix packages/typescript run build
node examples/web-number-ocr/run.mjs
```
