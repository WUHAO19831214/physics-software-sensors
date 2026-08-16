# 传感器升级记录：tracker.yolo 0.1.0 → 0.5.0

Date: 2026-08-16. Status: experimental / incubating.

## 变更范围

`0.1.0` 只有契约；`0.5.0` 新增 Python adapter、multi-target payload、`ModelArtifact`、recorded/Yolo/HOG backends、class filters、ByteTrack/fallback metadata、centroid association、source golden、example/assets 和 benchmark。SensorEvent 与 FramePacket Schema 均未升级。

## 来源

- Repository: `WUHAO19831214/audio-visual-soundfield-tracker-stable`
- Commit: `85740d686c67452a057540edb564d713e01ccc51`
- Files: `src/detector.py`, `src/camera_processor.py`, requirements/config/model setup/tests
- Extraction: behavior-preserving adapter with dependency injection and source-output replay; no source repository modification

## 算法与契约差异

- 保留来源 YOLO predict/ByteTrack 参数、HOG person fallback、centroid lifecycle；
- 新增显式 local artifact + SHA/license/runtime fields，取代来源项目目录扫描；
- 新增 all/ID/name filters；来源 `person_only` 可由 ID/name filter 表达；
- 多目标保存在 `payload.detections[]`，不改变主 Schema；
- detector score 不提升为顶层 confidence 或物理 uncertainty；
- backend/fallback/native ID 均进入事件，避免把 HOG/centroid 冒充 YOLO/ByteTrack。

## 验证结果

- source-generated zero/single/move/two/lost/reappear/missing-ID fixture；
- class filter 3/3，status + ID lifecycle 10/10；
- HOG blank-frame offline smoke；CameraSource composition；
- 500 次 mapping microbenchmark：single median 0.099937 ms，multi median 0.110354 ms；
- real inference：not executed；没有 approved local artifact，禁止联网下载；
- accuracy：not measured；没有 labelled evaluation set。

## 兼容、升级与回退

这是新增 API，没有下游迁移或数据变更。回退只需继续使用 manifest `0.1.0` 契约状态或不实例化新 adapter；来源项目保持原状。模型 artifact 不随版本打包，因此回退不删除/替换任何权重。

## Remaining gates

来源许可确认、artifact-specific weight review、固定 runtime/device 的真实 inference、真实 ByteTrack benchmark、标注数据集、真实摄像头 L2、下游 feature-flag pilot。未完成前不得提升 stable/validated。
