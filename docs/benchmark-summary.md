# Benchmark summary

These are the measurements currently supported by committed reports. A low synthetic latency is not a claim about camera capture, OCR on real devices or YOLO inference.

| Sensor | Dataset | Core metric | Median latency | Accuracy/error | Evidence | Limitation |
| --- | --- | --- | --- | --- | --- | --- |
| Camera | capture synthetic replay | 3/3 frames; drop preserved | not measured | fixture jitter 0 ms | E1 | 20 fps is replay rate, not camera ceiling |
| Screen | capture synthetic replay | 2/2 frames; drop preserved | not measured | interval 250 ms | E1 | no browser runtime |
| Number OCR | OCR synthetic pixels | exact numeric 3/3 | not measured | parse failures 2/2 | E3 | samples 224/65/63 ms are not a distribution |
| Color marker | color synthetic golden | source match 4/4 | not measured | tolerance `1e-6`; center error not measured | E2 | no illumination set |
| Spot centroid | source golden + downstream comparison | source 6/6; downstream 7/7 | 0.793 ms source replay | downstream max delta `7.1e-15`; derived range match | E5 | downstream replay is synthetic; no E4 optical/device set |
| Template | scripted + synthetic replay | moving 3/3; lost asserted | 7.722 ms | max center error 1 px | E3 | no blur/occlusion/platform set |
| YOLO | source-recorded replay | filters 3/3; states 10/10 | mapping 0.099937/0.110354 ms | inference accuracy not measured | E2 | mapping is not inference |

All values come from [`benchmarks/results/index.json`](../benchmarks/results/index.json), which also records environment, dataset card, source report and limitations for every sensor. Upgrade comparisons must use the sensor-specific metrics in [benchmarking.md](benchmarking.md), including failure/lost rate and source-output compatibility—not merely “the program did not crash.”
