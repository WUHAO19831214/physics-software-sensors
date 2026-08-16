# Number OCR recorded replay 示例

本轮示例证明 OCR adapter 离开 React UI 后可以独立处理来源格式的固定识别结果：

```ts
const recognizer = new RecordedNumberRecognizer(recordedResults);
const sensor = new NumberOCRSensor(recognizer);
sensor.configure({ roiId: 'force-y', roi, unit: 'N' });
const event = await sensor.processFrame(framePacket);
```

`RecordedNumberRecognizer` 不生成随机或模拟数值；找不到对应 frame/ROI 时返回明确 failure。后续 `examples/web-number-ocr/` 将在真实 Tesseract backend 完成后加入一个小型页面。
