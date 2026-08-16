# Screen capture → Number OCR

这个组合示例证明两个独立传感器可以直接串联：

```text
RecordedScreenBackend → ScreenCaptureSource → RuntimeFramePacket → NumberOCRSensor → SensorEvent
```

```bash
python examples/web-screen-capture/generate_sample.py
npm --prefix packages/typescript run build
node examples/web-screen-to-ocr/run.mjs
```

输入是明确标记的 synthetic recorded screen pixels；OCR 使用真实 Tesseract.js。它不是设备 SDK，也不证明真实实验软件字体/缩放兼容。
