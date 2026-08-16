# Number OCR 演示资产

本目录资产由 standalone example 的真实 Tesseract.js pixel path 产生。输入为 synthetic generic screen frame，不是朗威设备截图或实验数据。

```bash
python examples/web-number-ocr/generate_samples.py
npm --prefix packages/typescript run build
node examples/web-number-ocr/run.mjs
python examples/web-number-ocr/build_demo_assets.py
```

| Asset | Purpose | SHA-256 |
| --- | --- | --- |
| `overview.png` | synthetic 屏幕帧、实际 pixel ROI、rawText 和 parsed value | `f6f325c02a51d4cd592df5ac83e1732a713a513771977b4b67c0d10c3ca8eacb` |
| `processing.png` | Original → ROI crop → preprocessing → Tesseract.js → value | `57f1dac3ee56ad72c59190d11782c1ccaa7b520e888e8cef3156bf80268c1000` |
| `demo-result.json` | `-2.33` 图片对应的实际 SensorEvent 和 pixel ROI | `75a63f251ddf7173fabd6853d3049fbccabfa3e504ba373af3d4da1ab2910e8d` |

图片只证明固定 synthetic fixture 的端到端软件路径可运行，不提供真实设备 OCR 准确率。
