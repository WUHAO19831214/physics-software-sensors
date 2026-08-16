# Phase 2 adapter verification — 2026-08-16

## 结论

状态：informational。两个 experimental adapter 的离线测试通过；证据只覆盖合成颜色帧与合成 OCR recorded-result，不覆盖真实摄像头、屏幕或计量精度。

## 环境

- macOS 26.3.1 (25D2128), Apple arm64；
- Python 3.12.13, NumPy 2.5.2, OpenCV 4.14.0.94, pytest 8.4.2；
- Node v24.13.0, npm 11.6.2, TypeScript 5.9.x。

## Color Marker 来源兼容

- source：`audio-visual-soundfield-tracker-stable@85740d686c67452a057540edb564d713e01ccc51`；
- source file：`src/tennis_ball_tracker.py`；
- 命令：`python tools/compare_color_marker_source.py --source-root <fixed-checkout>`；
- 结果：4/4 场景全部 source-native 字段匹配，浮点绝对容差 `1e-6`；
- pytest：25/25 通过（含原 Phase 1 契约测试、golden、Schema、lost、配置、run ID、完整 FramePacket 和完整事件示例）。

## Number OCR replay

- source：多源实验桥 `8bba87d...` 与安培力教师端 `cb073e8...`；
- 结果：7/7 Node tests 通过，覆盖 parser、success、warning/degraded、parse failure、recognizer failure、missing record 和 invalid ROI；
- 失败事件 measurements 为空，没有 mock 或 stale value。

## 尚不能得出的结论

- Color Marker 在真实光照/曝光/背景中的 detection rate、center error、FPS/CPU/内存；
- OCR 对真实屏幕图像的 exact match、numeric error、failure rate 或 latency；
- 像素坐标到物理位移的准确度；
- 任何 `validated` 或 `stable` 成熟度结论。
