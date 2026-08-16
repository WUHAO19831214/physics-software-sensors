# Color Marker Tracker 演示资产

本目录资产由 standalone example 的真实 `ColorMarkerSensor` 运行生成。输入场景是 synthetic，不是来源项目截图或真实实验数据。

```bash
python examples/python-color-marker/run.py --output sensors/tracker.color-marker/assets
```

| Asset | Purpose | SHA-256 |
| --- | --- | --- |
| `overview.png` | 输入、实际检测中心、geometry 与状态 | `9b4b39f84d15167e032685de94efa47c78f688d186f8db45bcf673e8730da489` |
| `processing.png` | Original / actual HSV mask / Sensor detection | `b28345d75ca1abaa8c48247145d67284b4cf4df9d5d129e62aadd140b6ae013b` |
| `lost-reacquire.png` | 同一 sensor 实例的 tracking / lost / reacquired | `05e14d69147ede84634fc253f1786eb8e49a07383328625bb0b058e0bbb23d20` |
像素尺仅为视觉辅助，图片已明确注明 `not a physical calibration`。这些资产证明 adapter 可独立运行，不证明真实相机精度。
