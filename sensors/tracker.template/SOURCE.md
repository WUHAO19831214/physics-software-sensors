# 来源与抽取记录：tracker.template

## 固定来源与本轮范围

| Repository | Commit | Path | Symbol / responsibility | Actual use |
| --- | --- | --- | --- | --- |
| `WUHAO19831214/audio-visual-soundfield-tracker-stable` | `85740d686c67452a057540edb564d713e01ccc51` | `src/object_template_tracker.py` | `TRACKER_FALLBACK_ORDER`；`validate_bbox`；`scale_bbox_to_frame`；`create_opencv_tracker`；`ObjectTemplateTracker.initialize/update/reset` | 用户首帧 ROI 初始化后的 OpenCV 单目标追踪；输出 bbox/center/lost |
| 同上 | 同上 | `tests/test_object_template_tracker.py` | bbox validation、tracker availability、init failure、pre-init lost、integer ROI、capability report | 固定来源测试边界 |
| `WUHAO19831214/physics-experiment-bridge-mvp` | `8bba87df6475cae1e595fc925551db8bea83fb68` | `src/vision/TemplateMatchingAnalyzer.ts` | browser template matching analyzer | 相关但不同 profile；Phase 3B 未抽取、未用于本轮 golden |

本轮事实来源仅为稳定版 Python `ObjectTemplateTracker`。Sensor ID 继续使用 `tracker.template`，公开名称改为“Template / Single-object Tracker”以明确它不是静态模板匹配。

## 来源行为基线

- fallback 固定为 `CSRT → KCF → MIL`；若请求 KCF，则从 KCF 开始；
- 初始化 ROI 经边界校验并四舍五入为整数后传给 OpenCV；
- backend factory 不可用、抛异常或 `init()` 明确返回 `False` 时尝试下一 backend；`None` 被视为 OpenCV Python binding 的成功返回；
- update 前未初始化、update 返回 false/None、update 抛异常或 bbox 越界都产生 lost；
- successful result 输出 bbox corners/size、center、`track_id=1`、`class_name=custom_object`；
- OpenCV API 没有 confidence，来源值为 `None`；reinitialize 会 reset counters。

## 本仓库实现映射

| New file / symbol | Extraction method | Algorithm change |
| --- | --- | --- |
| `packages/python/src/physics_sensors/tracking/template.py::TemplateTracker` | UI/业务无关的低层 ROI tracker | 保留 bbox validation、整数 ROI、fallback、lost counters、reinitialize 和 source projection；错误文字改为英文诊断，不改变结构/数值语义 |
| 同文件 `create_opencv_tracker` | modern / `cv2.legacy` factory seam | 保留来源顺序；明确依赖 `opencv-contrib-python-headless` extra |
| 同文件 `TemplateTrackerSensor` | FramePacket/SensorEvent adapter | 新增 lifecycle、`initialize_target`、实际 backend/fallback payload、image-pixel coordinate；没有修改全局 ProcessorSensor contract |

`template_asset_uri` 只记录 reference-image provenance；它不替代 initialization ROI，也不触发静态 template matching。

## 来源执行型 golden / replay

`tools/generate_template_tracker_golden.py` 必须指向处于精确 SHA 的来源 checkout。它直接 import 来源 `src/object_template_tracker.py`，以 deterministic scripted backend 运行：

1. CSRT unavailable；
2. KCF init false；
3. MIL init success（fallback）；
4. target move；
5. disappear；
6. update exception；
7. reinitialize 与后续 move；
8. all backends unavailable。

生成的七个状态快照位于 `tests/fixtures/template_tracker/golden.json`，记录 Python、OpenCV、platform。`tests/test_template_tracker.py` 比对 stable output status/numeric fields，容差 `1e-9 px`；诊断 error prose 可本地化，要求非空但不要求中文字面一致。

真实 backend replay 另用 OpenCV 4.14.0 contrib CSRT 跑 synthetic textured target：初始化成功、3/3 移动帧 tracking、空白帧 lost，最大已知 synthetic center error 1.0 px。它是环境固定的软件回放，不是跨平台精度承诺。

## 演示资产

`examples/python-template-tracker/run.py` 实际运行 `ImageSequenceCameraBackend → CameraSource → TemplateTrackerSensor`，使用 contrib factory 选中 CSRT，并生成 `assets/overview.png`、`initialization.png`、`tracking.png`、`lost.png` 和事件记录。全部输入明确为 synthetic；详细 SHA-256 见 [assets/README.md](assets/README.md)。

## 许可证边界

来源固定 commit 没有 `LICENSE*`，GitHub metadata 为 `NOASSERTION`，所以 manifest 保持 `license_review: pending`。本轮不复制来源图片、UI 或整个模块；在 stable/发布前仍须完成来源代码许可确认。OpenCV contrib wheel 使用其自身许可证，package extra 只声明依赖，不提交二进制。
