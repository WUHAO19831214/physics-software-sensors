# Python Color Marker 独立示例

安装：

```bash
python -m pip install -e 'packages/python[color-marker]'
python examples/python-color-marker/run.py
```

示例不访问摄像头，也不依赖来源项目。它生成明确标记为 synthetic 的代表性 BGR 帧，实际调用 `ColorMarkerSensor`，输出三个 SensorEvent、HSV mask、检测标注和 lost/reacquire 图。

默认输出位于 `examples/python-color-marker/output/`。用于公开 Sensor Page 的审核副本由以下命令产生：

```bash
python examples/python-color-marker/run.py --output sensors/tracker.color-marker/assets
```

这些图片证明 standalone adapter 可运行，不代表真实实验精度或物理标定结果。
