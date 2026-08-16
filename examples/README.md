# 最小 Example Apps

Example 只证明传感器离开原实验应用后能够独立调用，不重建大型物理实验 UI。

- [`python-color-marker`](python-color-marker/README.md)：可运行的合成帧颜色追踪；
- [`web-number-ocr`](web-number-ocr/README.md)：可运行的 synthetic RGBA pixels + 真实 Tesseract.js OCR；
- [`python-camera-capture`](python-camera-capture/README.md)：deterministic image sequence 与显式 OpenCV hardware smoke；
- [`web-screen-capture`](web-screen-capture/README.md)：recorded replay 与最小 `getDisplayMedia` 页面；
- [`web-screen-to-ocr`](web-screen-to-ocr/README.md)：统一 Screen FramePacket 直接进入真实 Tesseract OCR；
- [`spot-centroid`](spot-centroid/README.md)：CameraSource → red weighted centroid → image-pixel SensorEvent；
- [`python-template-tracker`](python-template-tracker/README.md)：CameraSource + initialization ROI → real OpenCV tracker → bbox/lost SensorEvent。
