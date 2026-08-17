# Terminology / 术语 / 用語

[English](#english) | [简体中文](#简体中文) | [日本語](#日本語)

The machine-readable authority is [`terminology.json`](terminology.json). This page explains the choices most likely to drift; API identifiers, Sensor IDs, versions and algorithm names are never translated.

## English

- Use **Software Sensor** for the reusable sensing abstraction.
- Keep `FramePacket`, `SensorEvent`, `ModelArtifact`, YOLO, ByteTrack, HOG, CSRT, KCF, MIL, Tesseract.js and OpenCV unchanged.
- **Confidence** is not accuracy or uncertainty. **Detection** is not tracking.
- **Template / Single-object Tracker** names the current ROI-initialized OpenCV profile; it is not static template matching.
- **Companion Processing Tool** processes existing observations and is not a Sensor. Use **3D Vector Composition & Reconstruction** for `vector.compose-3d`.

## 简体中文

- Software Sensor 统一为“软件传感器”。
- 首次出现可写“帧数据包（FramePacket）”“传感器事件（SensorEvent）”，技术标识保持英文。
- Confidence 统一为“置信度”，不得写成“准确率”；uncertainty 统一为“不确定度”。
- `tracker.template` 使用“模板 / 单目标视觉追踪器”，并明确当前实现是 ROI 初始化的 CSRT/KCF/MIL 追踪，不是静态模板匹配。
- Companion Processing Tool 统一为“配套处理工具”；3D Vector Composition & Reconstruction 统一为“三维矢量合成与重建”。

## 日本語

- Software Sensor は「ソフトウェアセンサー」とする。
- 初出では「フレームパケット（FramePacket）」「センサーイベント（SensorEvent）」とし、API 識別子は変更しない。
- Spot Centroid は光学・物理の文脈で自然な「光スポット重心（Spot Centroid）」を正式語とする。「光点重心」は採用しない。
- `tracker.template` は「テンプレート／単一物体トラッカー」とし、「テンプレートマッチング」とは呼ばない。
- Confidence は「信頼度」、uncertainty は「不確かさ」とし、精度と混同しない。
- Companion Processing Tool は「補助処理ツール」、3D Vector Composition & Reconstruction は自然な技術表現として「3次元ベクトル合成・再構成」とする。

The complete 54-entry trilingual list, including notes, is validated from JSON.
