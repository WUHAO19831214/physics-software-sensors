# 数据集卡：color-marker-synthetic-golden@0.1.0

## 用途与范围

验证 `tracker.color-marker` 首次抽取是否保持固定来源实现对简单合成 BGR 帧的输出。它只用于 L1 regression/golden-master，不适用于真实摄像头精度、光照鲁棒性或物理位移结论。

## 内容

- 清单/结果：`tests/fixtures/color_marker/golden.json`；
- 4 个 160×120 确定性场景：首次圆形标记、移动、空白丢失、重捕获；
- 图像在测试运行时用 OpenCV 绘制，不提交 PNG，也不是 demo 截图。

## 来源真值

真值由 `audio-visual-soundfield-tracker-stable@85740d686c67452a057540edb564d713e01ccc51` 的 `src/tennis_ball_tracker.py::TennisBallTracker.update` 实际运行生成。比较工具会拒绝其他 source commit。

## 文件完整性

`tests/fixtures/color_marker/golden.json`
SHA-256: `32e6438deb85a736d66f385462f0319564d7ed466a64a866899eb6f2865aaceb`

## 环境

生成记录：Python 3.12.13、NumPy 2.5.2、OpenCV 4.14.0.94、macOS 26.3.1 arm64。

## 许可与隐私

合成数据，无人物或个人信息。来源仓库许可证为 `NOASSERTION`，因此本 fixture 只记录数值行为和 source SHA，不复制来源图片或整个源码文件。

## 限制

圆形纯色标记远比真实摄像头画面简单；OpenCV 版本变化可能产生极小轮廓浮点差异，当前绝对容差为 `1e-6`。
