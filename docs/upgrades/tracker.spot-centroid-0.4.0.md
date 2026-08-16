# 传感器升级记录：tracker.spot-centroid 0.1.0 → 0.4.0

- 日期/负责人：2026-08-16 / WUHAO19831214
- 变更：首次来源兼容 Python 算法与 SensorEvent adapter
- 目标成熟度：incubating / experimental
- Contract：FramePacket 与 SensorEvent `1.0.0` 均未改变
- Source anchors：两个固定 `app.js::rgbToHsv/trackRedSpot`，详见 [`SOURCE.md`](../../sensors/tracker.spot-centroid/SOURCE.md)
- 保持：red hue/RGB threshold、brightness weight、step、strict locked threshold、centroid/radius
- 新增：配置对象、normalized ROI、diagnostic fields/flags、lifecycle、health、provenance payload
- 科学边界：只输出 image centroid pixel；不输出 displacement、amplitude、period 或 frequency；confidence 为 null
- Verification：6/6 source detection/lost agreement，max centroid error 0.0 px，Camera composition，Schema、standalone 与 clean wheel smoke
- Rollback：pin Python package `0.3.0` 或继续使用未修改来源应用；当前无下游 migration
- Pending：来源许可、真实摄像头/光路 L2、CPU/memory、计量不确定度和下游试点
