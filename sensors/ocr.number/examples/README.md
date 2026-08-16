# Number OCR 示例

确定性测试继续使用 recorded result：

```ts
const recognizer = new RecordedNumberRecognizer(recordedResults);
const sensor = new NumberOCRSensor(recognizer);
sensor.configure({ roiId: 'force-y', roi, unit: 'N' });
const event = await sensor.processFrame(framePacket);
```

`RecordedNumberRecognizer` 不生成随机或模拟数值；找不到对应 frame/ROI 时返回明确 failure。

真实像素路径位于 [`examples/web-number-ocr`](../../../examples/web-number-ocr/README.md)。它读取 synthetic PNG，执行 RGBA crop、来源兼容预处理和 Tesseract.js，最后输出 SensorEvent 与 pixel-stage PNG，不需要 React 或原实验项目。
