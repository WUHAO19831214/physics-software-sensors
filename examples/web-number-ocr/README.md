# Web Number OCR 示例

这个 Node fixture runner 使用与浏览器相同的纯 RGBA ROI/preprocess 层，并实际启动 Tesseract.js worker。输入是明确标记为 synthetic 的屏幕帧，不是朗威设备截图或实验数据。

```bash
npm --prefix packages/typescript install
npm --prefix packages/typescript run build
python examples/web-number-ocr/generate_samples.py
node examples/web-number-ocr/run.mjs
```

覆盖 `+1.25`、`-2.33`、`0.00`、空白 parse failure、非数字 parse failure，以及一个明确标记的 controlled recognizer failure。前三项走完整像素→ROI→预处理→Tesseract.js→parser→SensorEvent 路径。

实际 OCR 可能首次下载并缓存 `eng` traineddata；runner 将缓存放在系统临时目录。运行输出位于 `examples/web-number-ocr/output/`。

公开页面组合图由真实输出生成：

```bash
python examples/web-number-ocr/build_demo_assets.py
```
