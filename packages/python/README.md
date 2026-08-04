# Python 契约骨架

本目录只提供跨项目可讨论、可类型检查的 Protocol 和数据类型，不包含 OpenCV、YOLO、OCR 或硬件采集实现。

未来适配器应实现 `SourceSensor` 或 `ProcessorSensor`，并以根目录 JSON Schema 作为序列化事实来源。首次迁移不得在适配层顺手改变来源算法。
