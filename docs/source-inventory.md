# 已有项目能力盘点

盘点日期：2026-08-04。以下结论来自公开仓库在所列 commit 的 README、文档、源码和测试；本次盘点未修改任何来源仓库，也未重新完成真实硬件实验。

## 1. 优先仓库与版本锚点

| 用户所指项目 | GitHub 仓库 | 盘点 commit |
| --- | --- | --- |
| 声音—视觉同步采集稳定版 | [`audio-visual-soundfield-tracker-stable`](https://github.com/WUHAO19831214/audio-visual-soundfield-tracker-stable) | `85740d686c67452a057540edb564d713e01ccc51` |
| 光斑追踪系统 | [`spot-vibration-tracking-system-20260508-171952`](https://github.com/WUHAO19831214/spot-vibration-tracking-system-20260508-171952) | `7f0d91cc73afafaecc54acc46b2b9d69375d994a` |
| 受迫振动系统 | [`forced-vibration-af-analyzer-20260502-122715`](https://github.com/WUHAO19831214/forced-vibration-af-analyzer-20260502-122715) | `c3f58175a09ff29cacdfb976a5055758c4eff619` |
| 多源实验桥 | [`physics-experiment-bridge-mvp`](https://github.com/WUHAO19831214/physics-experiment-bridge-mvp) | `8bba87df6475cae1e595fc925551db8bea83fb68` |
| 安培力教师端 | [`ampere-force-visualizer-teacher-yanan`](https://github.com/WUHAO19831214/ampere-force-visualizer-teacher-yanan) | `cb073e89d6d87129287030f1df08bd540504eb39` |

注意：声音—视觉稳定仓库的 README 还记录了更早的“稳定基线来源 commit” `6c5c6b7ca23155db58b63794993322fbdeb8f868`。本盘点锚定的是仓库当前公开 HEAD；未来适配算法时必须进一步区分“实现来源 commit”和“文档盘点 commit”。

## 2. 能力—来源矩阵

| 能力 | 主要来源与代码位置 | 当前证据 | 抽象时要保留的边界 |
| --- | --- | --- | --- |
| 摄像头采集 | 稳定版 `src/browser_capture.py`、`src/local_capture.py`；光斑/受迫振动 `app.js`；实验桥/教师端 camera 目录 | 稳定版有自动测试；浏览器项目为可运行原型 | 浏览器与 OpenCV 两种后端；权限、设备枚举、实际 FPS、镜像与时间戳分开 |
| 屏幕采集 | 实验桥/教师端 `src/screen/ScreenCapturePanel.tsx`、`screenCaptureRuntime.ts` | `getDisplayMedia` 真实路径，文档明确权限/失败边界 | 是用户授权的像素流，不是设备 SDK；刷新后需重新授权 |
| 数字 OCR | 实验桥/教师端 `TesseractRecognizer.ts` 与 OCR/ROI 工具 | Tesseract.js 已接入；template-digit、cnn-onnx 仍为占位 | rawText、解析值、置信度、耗时、调试图与后处理分别记录；禁止失败后伪造 mock |
| 颜色标记追踪 | 稳定版 `src/tennis_ball_tracker.py`；实验桥/教师端 `ColorTrackingAnalyzer.ts`、`MarkerTrackingAnalyzer.ts` | Python 路径有自动测试；浏览器分析器成熟度各异 | HSV 范围、形态学、面积、圆度、平滑、丢失计数和回退行为显式配置 |
| YOLO 追踪 | 稳定版 `src/detector.py`、`src/camera_processor.py` | YOLO + ByteTrack 优先，HOG 回退；有 detector/tracking 测试 | 权重和后端版本、类别过滤、track ID 可用性、回退原因必须进入描述/质量信息 |
| 模板/单目标追踪 | 稳定版 `src/object_template_tracker.py`；实验桥/教师端 `TemplateMatchingAnalyzer.ts` | OpenCV CSRT→KCF→MIL 路径有自动测试；浏览器模板分析器需单独验证 | 初始化 ROI 与模板资产不是同一概念；后端回退、丢失率和重初始化策略必须可见 |
| 光斑重心 | 光斑与受迫振动项目 `app.js` | 固定红色阈值 + 加权重心可运行；仓库明确“尚待计量验证” | 输出是图像光斑重心，不是本体位移；阈值、权重、ROI、曝光、丢失和标定必须记录 |
| 时间融合 | 稳定版 `src/sync_clock.py`、`src/fusion.py` | 共享时钟与最近邻融合已有测试 | 0.15 s 是实现策略；保留 `time_diff`、未匹配记录与时钟域，不宣称硬件同步 |

## 3. 可直接复用的设计知识

### 声音—视觉稳定版

- 一个共享 `SyncClock` 同时提供易导出的墙钟与稳定的会话 elapsed；
- 融合以音频事件为输出节奏，在容差内选择最近视觉记录；
- 追踪输出已包含 bbox、中心、模式、类别、状态、标记几何与丢失帧；
- 文档明确 `center_x/y` 是像素，`db` 是 dBFS，插值不等于实测；
- 自动测试记录为 64 passed，但硬件可用性仍需独立验证。

### 多源实验桥与安培力教师端

- `VisionAnalyzer.analyze(imageData, roiConfig)` 已形成初步策略接口；
- 屏幕 ROI 与摄像头 ROI 是两套不同概念；
- OCR 已区分 rawText、value、confidence、durationMs、warning 和调试图；
- 实际采样率受 OCR 耗时与浏览器调度影响，配置频率不等于达到的频率；
- 安培力教师端再次确认链路是“设备原软件显示 → 屏幕像素 → OCR”。

### 光斑与受迫振动项目

- 直接观测是红色候选像素加权重心 `(x,y)`；
- `max(y)-min(y)` 是窗口内峰—峰光斑范围，不是机械本体单边振幅；
- 程序频率是 Web Audio 设定值，不是独立实测频率；
- 缺少逐帧等间隔时间序列时，不能宣称实现可信 FFT 或相位差；
- 仓库已有静态定位、空间标定、动态位移、频率链路和人工视频对照的验证建议。

## 4. 差距与风险

| 差距 | 影响 | 第一阶段处理 |
| --- | --- | --- |
| Python 与 TypeScript 各自定义结果结构 | 下游耦合、字段漂移 | 统一 JSON Schema 与双语言类型骨架 |
| 来源许可证不完全一致或未显式记录 | 未来复制代码风险 | 本阶段只引用，不复制；迁移前做许可证核查 |
| 正式标注/回放集不足 | 无法比较升级前后精度 | 定义数据集卡和分层基准协议 |
| 配置频率与实测吞吐率混用 | 性能结论失真 | 事件与健康快照分别记录配置值、实测值 |
| 像素、归一化、标定物理量混用风险 | 物理意义错误 | 强制 coordinate frame 与 measurement role |
| mock/占位/真实路径并存 | 容易误报能力 | 清单记录实现状态与证据等级 |
| 模型、模板、浏览器资源版本未统一 | 难以复现 | 描述符记录 artifact URI、SHA-256 和运行时版本 |

## 5. 推荐抽取顺序

1. 先固定事件、ROI、时间、坐标和健康契约；
2. 以稳定版中已有 pytest 的颜色标记、模板追踪、YOLO 输出适配为首批 Python 试点；
3. 以预录帧回放方式适配浏览器 OCR、屏幕采集和光斑重心；
4. 对同一输入运行“来源实现 vs 新适配器”黄金主测试，要求输出在既定容差内一致；
5. 再选择一个下游仓库进行可回退接入，不同时迁移五个项目。

## 6. Phase 2 抽取状态（2026-08-16）

- `tracker.color-marker`：Python 行为保持抽取和 SensorEvent adapter 已进入 incubating；来源同帧合成对照见 [`SOURCE.md`](../sensors/tracker.color-marker/SOURCE.md)；
- `ocr.number`：TypeScript parser、recognizer seam、recorded replay、纯 RGBA ROI/preprocess 和真实 Tesseract.js backend 已进入 incubating，见 [`SOURCE.md`](../sensors/ocr.number/SOURCE.md)；
- 两个 standalone examples 已用明确标记的 synthetic input 生成当前 adapter demo；它们不是来源项目截图或真实实验验证；
- 五个来源仓库在固定 commit 没有可用演示截图，且许可证 metadata 均为 `NOASSERTION`；详见 [资产盘点](asset-inventory.md)和[许可证边界](licensing-and-provenance.md)；
- 本轮没有修改任何来源仓库。

## 7. Phase 3A Capture 抽取状态（2026-08-16）

- `camera.capture`：从五仓 camera path 中抽离 Python backend/read/time/release 边界，加入 OpenCV 与 deterministic image-sequence backend；检测、追踪、同步与 UI 未迁入；
- `screen.capture`：从实验桥/教师端 `startCapture/stopCapture` 抽离 TypeScript permission/video/canvas/stop 边界，OCR、ROI、过滤与 store 留在下游；
- 两项均使用 FramePacket Schema `1.0.0`；requested、nominal、measured rate 不混写；
- replay 结果和真实 Tesseract composition 已自动验证，但未运行真实 camera/browser smoke；
- 五个来源仓库仍停留在表中完整 commit 且 clean，没有任何修改。

## 8. Phase 3B Classical Tracker 抽取状态（2026-08-16）

- `tracker.spot-centroid`：从光斑和受迫振动两个固定 `app.js::rgbToHsv/trackRedSpot` 抽取 red threshold、brightness weighting、locked 和 centroid；`getAmplitudeFrom`、校准与扫频业务不进入 sensor；
- `tracker.template`：从稳定版 `src/object_template_tracker.py::ObjectTemplateTracker` 抽取 ROI validation、`CSRT→KCF→MIL`、lost/reinitialize；实验桥静态 template matching 仍是不同、未抽取 profile；
- 两项都有来源执行型 golden、synthetic replay、CameraSource composition 和 explicit null confidence；
- FramePacket Schema 仍为 `1.0.0`，统一 ProcessorSensor interface 未改；
- 五个来源仓库仍在表中 SHA 且 clean，没有任何修改。

## 9. Phase 3C YOLO Tracker 抽取状态（2026-08-16）

- `tracker.yolo`：从稳定版 `src/detector.py::Detector` 和 `src/camera_processor.py::CentroidTracker` 抽离 detection/ByteTrack 调用、multi-target projection、HOG fallback 和 centroid lifecycle；
- 新增显式 `ModelArtifact`，不扫描来源项目、不自动下载、不提交权重；
- 来源执行型 golden 固定 zero/single/move/two/lost/reappear/missing-ID 和 centroid reset；recorded replay、fake runtime seam 与实际 HOG blank-frame smoke 全部离线；
- 真实 Ultralytics inference 未执行，因为没有经维护者批准的本地 artifact 且当前环境未安装 runtime；模型/追踪 accuracy 均未测量；
- FramePacket Schema 仍为 `1.0.0`，SensorEvent 主 Schema 未改；五个来源仓库继续停留在表中 SHA 且 clean。
