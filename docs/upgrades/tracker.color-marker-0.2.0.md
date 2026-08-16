# 传感器升级记录：tracker.color-marker 0.1.0 → 0.2.0

## 基本信息

- 负责人：WUHAO19831214；
- 日期：2026-08-16；
- 变更类型：首次行为适配 + 统一事件包装；
- 目标成熟度：incubating / experimental；
- 契约版本：SensorEvent `1.0.0`（未改变）。

## 来源锚点

- 来源：`WUHAO19831214/audio-visual-soundfield-tracker-stable`；
- 完整 commit：`85740d686c67452a057540edb564d713e01ccc51`；
- 实现文件：`src/tennis_ball_tracker.py`；
- 原始函数/类：`make_tennis_mask`、`find_ball_candidates`、`choose_best_candidate`、`estimate_hsv_range_from_roi`、`TennisBallTracker.update`；
- 原始测试：`tests/test_tennis_ball_tracker.py`；
- 许可证：source commit 为 `NOASSERTION`，审核 pending；stable 前必须明确。

## 行为变化

- `TennisBallTracker` 泛化命名为 `ColorMarkerTracker`；
- HSV、morphology、候选、圆度、连续性和平滑算法未改变；
- source-native dict 由 `ColorMarkerResult.to_source_dict()` 保留；
- 新增 `ColorMarkerSensor` 生命周期、RuntimeFrame、SensorEvent、健康计数和 latency；
- 平滑后的中心在 measurement 中标为 `filtered`；
- 丢失事件不携带上次位置。

## 验证证据

- L0：Schema、配置、生命周期、lost semantics；
- L1：4 个确定性合成帧；
- 来源对照：固定 source checkout 与新 tracker 同进程、同帧、同配置；
- 结果：4/4 全字段匹配，浮点绝对误差 ≤ `1e-6`；
- fixture：`color-marker-synthetic-golden@0.1.0`；
- standalone demo：`ok → lost → ok`，生成实际 mask、SensorEvent 和 annotated assets；
- 报告：[`benchmarks/results/phase2-adapter-verification-2026-08-16.md`](../../benchmarks/results/phase2-adapter-verification-2026-08-16.md)。

## 兼容与迁移

- 没有要求来源项目改用本包；
- 新 import 为 `physics_sensors.tracking`；
- Phase 1 `physics_software_sensors` core import 暂保留兼容；
- 来源业务可继续使用原 `TennisBallTracker`。

## 回退

- 本仓库回退到 manifest `0.1.0` 即只保留契约；
- 来源项目完全未修改，因此无需数据或代码回退；
- 下游尚未接入。

## 未完成门禁

- [ ] source 许可证明确
- [ ] 真实摄像头数据集与性能基准
- [ ] L2 定位/丢失/光照验证
- [ ] 下游试点与回退演练
