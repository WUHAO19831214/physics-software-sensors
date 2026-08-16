# 传感器升级记录：tracker.template 0.1.0 → 0.4.0

- 日期/负责人：2026-08-16 / WUHAO19831214
- 变更：首次 ROI-initialized OpenCV Python adapter
- 目标成熟度：incubating / experimental
- Contract：FramePacket 与 SensorEvent `1.0.0` 未改变；只增加专用 `initialize_target` 方法
- Source anchor：`audio-visual-soundfield-tracker-stable@85740d686c67452a057540edb564d713e01ccc51:src/object_template_tracker.py::ObjectTemplateTracker`，详见 [`SOURCE.md`](../../sensors/tracker.template/SOURCE.md)
- 保持：ROI validation/int rounding、CSRT→KCF→MIL、lost counters、reinitialize、confidence null
- 新增：requested/actual backend 和 fallback payload/flag、FramePacket adapter、template asset provenance metadata
- 依赖：OpenCV 相关 extras 统一使用 contrib headless，避免 regular/contrib wheel 同装冲突；未 vendor 二进制
- 语义澄清：本 profile 是 single-object tracker；initialization ROI 不等于 static template image
- Verification：固定来源七个 scripted snapshots；fallback、move、lost、exception、reinitialize、unavailable；真实 CSRT synthetic replay；Camera composition；clean wheel smoke
- Rollback：pin Python package `0.3.0` 或继续使用未修改来源应用；当前无下游 migration
- Pending：来源许可、真实目标/相机 L2、跨 OpenCV/platform、CPU/memory 和下游试点
