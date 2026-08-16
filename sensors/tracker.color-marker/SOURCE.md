# 来源与抽取记录：tracker.color-marker

## 来源锚点

| 项目 | 仓库 | commit | 文件 | 类/函数 | 原用途 |
| --- | --- | --- | --- | --- | --- |
| 声音—视觉同步采集稳定版 | `WUHAO19831214/audio-visual-soundfield-tracker-stable` | `85740d686c67452a057540edb564d713e01ccc51` | `src/tennis_ball_tracker.py` | `make_tennis_mask`、`find_ball_candidates`、`choose_best_candidate`、`estimate_hsv_range_from_roi`、`TennisBallTracker.update` | 从 BGR 帧追踪网球色标记，向同步采集链路提供中心、bbox 和质量字段 |
| 同上 | 同上 | 同上 | `tests/test_tennis_ball_tracker.py` | 7 个测试及 `tennis_frame` 合成输入 | 验证 mask、候选、ROI、平滑、lost 状态 |
| 多源实验桥 | `WUHAO19831214/physics-experiment-bridge-mvp` | `8bba87df6475cae1e595fc925551db8bea83fb68` | `src/vision/ColorTrackingAnalyzer.ts` | `ColorTrackingAnalyzer.analyze` | 浏览器视觉分析；本轮仅记录，不进入 Python adapter |
| 多源实验桥 | 同上 | 同上 | `src/vision/MarkerTrackingAnalyzer.ts` | `MarkerTrackingAnalyzer.analyze` | 浏览器标记分析；本轮仅记录，不进入 Python adapter |

## 抽取方式

- 方式：根据固定 source commit 做行为保持的 Python 模块抽取与统一接口包装；
- 来源文件没有整体复制到本仓库，也没有引入 Streamlit、本机采集、融合或绘图代码；
- 算法步骤保持：BGR→HSV、阈值、5×5 椭圆核 opening/closing、外轮廓、面积/圆度过滤、连续性选择、指数平滑；
- `TennisBallTracker` 泛化命名为 `ColorMarkerTracker`，默认配置和 source-native 输出键保持兼容；
- `ColorMarkerSensor` 新增生命周期、FramePacket runtime 绑定、SensorEvent 映射、健康计数和耗时记录。

## 来源到新实现映射

| Source file/function | New file/symbol | Extraction |
| --- | --- | --- |
| `src/tennis_ball_tracker.py::make_tennis_mask` | `packages/python/src/physics_sensors/tracking/color_marker.py::make_color_mask` | 行为保持、泛化命名 |
| `find_ball_candidates` | 同文件 `find_color_candidates` | 保留 contour geometry/source keys |
| `choose_best_candidate` | 同文件 `choose_best_candidate` | 保留首次与连续帧排序公式 |
| `estimate_hsv_range_from_roi` | 同文件同名函数 | 保留 median/margin/clamp 行为 |
| `TennisBallTracker.update` | `ColorMarkerTracker.update` | 保留 tracking/lost/smoothing；类型化结果 |
| 无统一接口 | `ColorMarkerSensor.process_frame/process` | 新增 FramePacket/SensorEvent adapter，不改变算法输出 |

## 算法与行为差异

| 项目 | 来源 | 新实现 | 原因 |
| --- | --- | --- | --- |
| 类名 | `TennisBallTracker` | `ColorMarkerTracker` | 去除特定实验对象命名；默认 class/mode 仍保持来源值 |
| 原始结果 | 普通 dict | `ColorMarkerResult` + `to_source_dict()` | 类型化，同时完整保留 source-native 键 |
| 统一输出 | 无 | `SensorEvent`，原始 dict 位于 `payload.source_raw` | 与仓库契约对齐 |
| 输入 | BGR NumPy frame | `RuntimeFrame(metadata FramePacket + BGR pixels)` | 让时间、frame ID 和坐标可追溯 |
| 异常/丢失 | nonfatal lost dict | 保持 lost；事件增加 `target-lost` | 不伪造位置 |
| `max_lost_frames` | 配置存在但不改变 update 行为 | 保持同样行为 | 首次抽取不修算法；后续另开升级记录 |

没有改变阈值默认值、轮廓计算、候选排序或平滑公式。

## 来源兼容验证

- 同一输入：测试代码生成的确定性 BGR 圆形帧和空白帧；
- 来源运行：`tools/compare_color_marker_source.py --source-root <checkout>` 动态加载上述固定 commit 的 `tennis_ball_tracker.py`；
- 新实现运行：同一进程、同一 NumPy frame、相同配置；
- 比较字段：`ok`、状态、track ID、中心、bbox、半径、面积、圆度、lost count；
- 数值容差：绝对误差 `1e-6`；
- 固定回归：来源输出记录在 `tests/fixtures/color_marker/golden.json`，普通 pytest 不需要来源仓库；
- 当前结论：仅证明合成帧上的来源输出兼容，不证明真实相机精度。

## 许可证与资产

固定 source commit 没有 LICENSE/COPYING/NOTICE，GitHub license metadata 为 `NOASSERTION`。本轮由仓库维护者明确要求进行抽取，但 `license_review` 仍保持 `pending`，在 stable 发布前应给来源仓库补充明确许可证或书面归属记录。

来源 commit 没有可复用演示图片，因此没有复制来源图片。Phase 2D 的 demo 由 `examples/python-color-marker/run.py` 创建 synthetic BGR 帧、调用真实 adapter，再根据 `payload.source_raw`、实际 HSV mask 和事件状态生成。生成资产及 SHA-256 见 [assets/README.md](assets/README.md)；这不是来源项目或真实实验截图。
