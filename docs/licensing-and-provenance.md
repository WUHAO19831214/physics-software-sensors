# 许可证与来源边界

本页记录当前技术和仓库事实，不替代法律意见。代码“由同一 GitHub 账号维护”不能自动补足一个缺失的开源许可证。

## A. 本仓库

`physics-software-sensors` 根目录包含 MIT License，版权行为 `Copyright (c) 2026 WUHAO19831214`。README 的许可证说明与该文件一致。本仓库中新写且由仓库维护者有权许可的代码、文档和 synthetic fixtures 按该 MIT License 分发。

## B. 五个历史来源仓库

| Repository | Audited commit | Repository license file | GitHub license metadata |
| --- | --- | --- | --- |
| `audio-visual-soundfield-tracker-stable` | `85740d686c67452a057540edb564d713e01ccc51` | 未发现 | `NOASSERTION` |
| `spot-vibration-tracking-system-20260508-171952` | `7f0d91cc73afafaecc54acc46b2b9d69375d994a` | 未发现 | `NOASSERTION` |
| `forced-vibration-af-analyzer-20260502-122715` | `c3f58175a09ff29cacdfb976a5055758c4eff619` | 未发现 | `NOASSERTION` |
| `physics-experiment-bridge-mvp` | `8bba87df6475cae1e595fc925551db8bea83fb68` | 未发现 | `NOASSERTION` |
| `ampere-force-visualizer-teacher-yanan` | `cb073e89d6d87129287030f1df08bd540504eb39` | 未发现 | `NOASSERTION` |

五个仓库均位于 `WUHAO19831214` GitHub namespace，当前仓库也由同一账号维护；这是 provenance 事实，不是旧代码许可证的技术推断。本轮没有修改这些仓库，也没有给它们自动添加许可证。

## C. 本仓库中新写的 adapter

- `physics_sensors.core`、`ModelArtifact`、`CameraSource`、`ColorMarkerSensor`、`SpotCentroidSensor`、`TemplateTrackerSensor`、`YoloTrackerSensor`、TypeScript pixel runtime、`ScreenCaptureSource`、`NumberOCRSensor` 的统一适配层是在本仓库中新写；
- 新写部分随本仓库 MIT License 分发；
- 文件头、Sensor Page 和 SOURCE.md 仍保留历史算法来源，以免“新写 adapter”被误解为没有上游影响。

## D. 根据来源逻辑迁移或重构的部分

- Color Marker 的 HSV/morphology/contour/smoothing 行为锚定 `tennis_ball_tracker.py`；
- OCR parser、ROI rounding、nearest-neighbor scaling、阈值和 Tesseract worker 参数锚定两个 OCR 来源仓库；
- Camera/Screen source 的设备/权限/视频/停止边界锚定五个来源仓库；capture 不复制 UI、检测或 OCR 业务；
- Spot Centroid 的 red threshold、brightness weighting、locked threshold 和 centroid 行为锚定光斑/受迫振动两个 `app.js`；物理派生分析没有迁入 sensor；
- Template Tracker 的 ROI validation、CSRT→KCF→MIL、lost/reinitialize 行为锚定稳定版 `object_template_tracker.py`；browser 静态 template matching 没有迁入本 profile；
- YOLO Tracker 的 predict/track 参数、box/ID projection、HOG fallback 和 centroid lifecycle 锚定稳定版 `detector.py` / `camera_processor.py`；模型权重与 runtime 不进入 library artifact；
- 这些实现不是无来源的全新算法。即使代码为重新组织或重写，也必须继续保留 commit/file/function 追溯；
- 在来源许可证澄清前，`license_review` 保持 `pending`，不得把传感器提升为 stable 或声称来源代码已被普遍授权再分发。

## E. Fixture 与 demo asset

- Color Marker PNG 由 `examples/python-color-marker/run.py` 生成，并由真实 `ColorMarkerSensor` 输出驱动标注；
- OCR PNG 输入由 `examples/web-number-ocr/generate_samples.py` 生成，demo 图由真实 Tesseract.js 结果和 pixel stages 组合；
- Camera 与 Screen PNG 由 Phase 3A standalone replay 生成，分别来自实际 `CameraSource` / `ScreenCaptureSource` output；
- Spot 与 Template PNG 由 Phase 3B standalone replay 生成，分别来自实际 `SpotCentroidSensor` 和 OpenCV contrib `TemplateTrackerSensor` output；
- YOLO PNG/JSON 由 Phase 3C standalone recorded replay 生成，来自 fixed source-executed numeric fixture 和实际 adapter output，不含真实模型或人物图像；
- 它们都是 synthetic test fixtures，不是来源项目截图、真实设备画面或实验精度证据；
- 图片不包含个人信息、学校标识、第三方 UI 或模型权重；
- 生成脚本和审定后的资产随本仓库 MIT License 分发。

## 第三方运行依赖

| Dependency | Resolved version | Upstream license | Bundled artifact policy |
| --- | --- | --- | --- |
| `tesseract.js` | `7.0.0` | Apache-2.0 | npm 依赖；本仓库不复制其源码或 worker artifact |
| `pngjs` | `7.0.0` | MIT | npm 依赖，用于 Node PNG 编解码 |
| Tesseract `eng` traineddata | 运行时获取/缓存 | 以下载来源许可为准 | 不提交到仓库或 npm tarball |
| OpenCV / NumPy | 由 Python extra 安装 | 以上游包元数据为准 | 不 vendoring |
| Ultralytics YOLO | 未安装；source range `>=8.2,<9` | AGPL-3.0 / Enterprise 路径，须按实际用途复核 | optional extra；不 vendoring、不默认安装、不自动下载 |
| YOLO model weights | 未提供 | 必须逐 artifact 确认 | 不提交、不打包、不重新分发 |
| ByteTrack / HOG | runtime tracker config / OpenCV 4.x | 分别核对 Ultralytics integration、original ByteTrack MIT、OpenCV Apache-2.0 | 只声明运行时依赖；见 [专项审查](yolo-model-and-license-review.md) |

## 给维护者的明确建议

建议维护者逐个审查五个来源仓库中的自有代码、第三方资产、模型和依赖，然后为确认有权许可的内容补充明确 `LICENSE`。如果选择 MIT，应由维护者在各来源仓库单独提交，不能由本仓库的 MIT 文件替代，也不应把未知权利的第三方图片或模型一并视为 MIT。
