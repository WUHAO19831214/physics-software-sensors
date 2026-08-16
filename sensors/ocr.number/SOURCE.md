# 来源与抽取记录：ocr.number

## 来源锚点

| 项目 | 仓库 | commit | 文件 | 类/函数 | 原用途 |
| --- | --- | --- | --- | --- | --- |
| 多源实验桥 | `WUHAO19831214/physics-experiment-bridge-mvp` | `8bba87df6475cae1e595fc925551db8bea83fb68` | `src/recognizers/TesseractRecognizer.ts` | `TesseractRecognizer.recognize`、worker helpers | Tesseract.js 本地识别、runtime 状态、队列和调试字段 |
| 同上 | 同上 | 同上 | `src/utils/extractNumber.ts` | `normalizeOcrText`、`extractNumberFromText` | 易混字符归一化和普通十进制解析 |
| 同上 | 同上 | 同上 | `src/utils/imagePreprocess.ts` | `cropRoiFromVideo`、`preprocessForNumberRecognition` | ROI 裁剪、4×放大、灰度/对比度/阈值、孤立点去噪 |
| 同上 | 同上 | 同上 | `src/utils/ocrPreprocess.ts` | `preprocessForLangweiNumber` | 朗威数字的模式选择、锐化/颜色数字提取 |
| 同上 | 同上 | 同上 | `src/utils/numberPostprocess.ts` | `normalizeRecognizedNumber` | round/truncate 与显示小数位 |
| 同上 | 同上 | 同上 | `src/screen/ScreenCapturePanel.tsx` | `ScreenCapturePanel` 内 `startCapture`、采样 effect | getDisplayMedia、ROI→预处理→识别→过滤→store |
| 安培力教师端 | `WUHAO19831214/ampere-force-visualizer-teacher-yanan` | `cb073e89d6d87129287030f1df08bd540504eb39` | 上述同名五个核心 OCR/utility 文件 | 同名类/函数 | 教师端 Fy/Fz 屏幕识别 |

## 文件一致性证据

两个来源 commit 中以下文件 SHA-256 相同：

| 文件 | SHA-256 |
| --- | --- |
| `src/recognizers/TesseractRecognizer.ts` | `17befc069b705f55f630a6c01464518ae650690da1ef2eda8c4360a177fdb0f3` |
| `src/utils/extractNumber.ts` | `2561092caedbe2ebaf796e2e0b0cbbb1c7c258ea7a87f02be7670a22ce405374` |
| `src/utils/ocrPreprocess.ts` | `5a9be895ffff9c26989262973fd257b810b1da870a37dbd789b4e161dd3f1ef9` |
| `src/utils/imagePreprocess.ts` | `95f20e44a8246e4832f5b112c0a4d3400a8c943bd51f39a483b0efc78a6890b9` |
| `src/utils/numberPostprocess.ts` | `79ca6812805a71c794334d11878836afa78d31fbb84cb2706ea7c29adfa6161f` |

## 本轮抽取方式

- 方式：TypeScript 行为适配与 recognizer dependency injection；
- 已抽取：来源 `normalizeOcrText` / `extractNumberFromText` 的可测试行为、RGBA normalized ROI crop、nearest-neighbor 4× scaling、灰度/对比度/阈值/去噪预处理、Tesseract.js worker lifecycle、recognizer result 结构、failure/warning 保留、SensorEvent 映射；
- 新增：`RecordedNumberRecognizer`，只按 frame ID + ROI ID 回放来源格式的固定结果；它不是 mock 数字生成器；
- 新增：`TesseractJsRecognizer`，以 `NumberRecognizer` seam 接收 runtime RGBA pixels，在浏览器使用 Canvas、在 Node 使用 PNG buffer；
- 未抽取：React screen UI、`getDisplayMedia`、采样/物理过滤 store；
- 不存在 OCR 失败→mock 回退路径。

## 来源到新实现映射

| Source file/function | New file/symbol | Extraction |
| --- | --- | --- |
| `src/utils/extractNumber.ts::{normalizeOcrText,extractNumberFromText}` | `packages/typescript/src/ocr/number.ts` 同名函数 | parser 行为保持 |
| `src/utils/imagePreprocess.ts::cropRoiFromVideo` | `src/core/pixels.ts::cropNormalizedRoi` | 去 DOM，保留 normalized×size rounding，输入改为 RGBA |
| `preprocessForNumberRecognition` | `src/ocr/preprocess.ts` 同名函数 | 去 Canvas，保留 4× nearest、gray/contrast/threshold/noise 语义 |
| `src/utils/ocrPreprocess.ts::preprocessForLangweiNumber` | `src/ocr/preprocess.ts` 同名函数 | 保留 mode 参数与阈值 |
| `src/recognizers/TesseractRecognizer.ts::TesseractRecognizer` | `src/ocr/tesseract.ts::TesseractJsRecognizer` | worker/queue/parameters 保留，生命周期改为实例所有且可 close |
| 来源 `NumberRecognizer` | `src/ocr/number.ts::NumberRecognizer` | seam 保留，并继续支持 recorded backend |
| 来源 UI sampling orchestration | `src/ocr/number.ts::NumberOCRSensor` | 只新增 SensorEvent mapping，不迁入 UI/store/物理过滤 |

## 差异

| 项目 | 来源 | 新实现 | 原因 |
| --- | --- | --- | --- |
| 运行输入 | browser video/ImageData | FramePacket metadata + runtime RGBA pixels；recorded result seam 保留 | 去除 DOM/UI 依赖，保留可测试像素边界 |
| ROI | DOM Canvas `drawImage` | 纯 RGBA row copy，坐标仍按来源 `round(normalized×size)` | Node/browser 共用且确定性 |
| resize | Canvas 且 `imageSmoothingEnabled=false` | 纯数组 nearest-neighbor 4× | 保持像素语义并可单测 |
| 识别后端 | module-global Tesseract worker/queue | 每个 `TesseractJsRecognizer` 持有可关闭 worker/queue | 明确实例生命周期，避免跨 sensor 隐式状态 |
| 图片编码 | Browser Canvas | Browser Canvas；Node 动态 PNG buffer | 支持独立 Node fixture runner，不引入 UI |
| parser | 同步 utility | 同语义独立 utility | 可在 Node 测试 |
| 失败 | value null + warning/error | error SensorEvent、空 measurements | 对齐统一契约，禁止假值 |
| 后处理 | UI sampling 层 round/filter | 未进入核心 OCR measurement | 保持 raw OCR 与应用物理过滤分离 |

## 来源兼容验证

- `tests/fixtures/ocr-number/recorded-results.json` 固定 rawText、source parsed value、confidence、duration、warning/error；
- TypeScript 测试对来源 parser 行为逐项比较，数值使用严格相等（普通 IEEE-754 parse）；
- replay 测试覆盖成功、有 warning、无法解析和 recognizer failure；
- pure pixel tests 覆盖 ROI crop、RGBA 约束和 binary preprocessing；
- synthetic pixel integration 启动真实 Tesseract.js，对 `+1.25/-2.33/0.00` 获得 3/3 固定 fixture exact numeric match，并覆盖 blank parse failure 与 controlled engine failure；
- 当前没有来源真实屏幕图片，因此不声称真实设备 OCR exact-match 精度。

## 许可证与资产

两个来源 commit 均未声明仓库许可证，GitHub metadata 为 `NOASSERTION`。本轮不复制 UI 文件或来源图片；adapter 在本仓库重组实现并保持上述追溯。`license_review` 继续为 `pending`，stable 前仍须由维护者明确来源仓库许可证。详见 [许可证与来源边界](../../docs/licensing-and-provenance.md)。

Phase 2D demo 由本仓库脚本生成 synthetic screen PNG，并用真实 adapter/Tesseract 输出组合；生成命令和 SHA-256 见 [assets/README.md](assets/README.md)。
