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
- 已抽取：来源 `normalizeOcrText` / `extractNumberFromText` 的可测试行为、ROI 验证、recognizer result 结构、failure/warning 保留、SensorEvent 映射；
- 新增：`RecordedNumberRecognizer`，只按 frame ID + ROI ID 回放来源格式的固定结果；它不是 mock 数字生成器；
- 未抽取：真实 `Tesseract.createWorker`、Canvas/ImageData 裁剪和预处理、React screen UI、采样/物理过滤 store；
- 不存在 OCR 失败→mock 回退路径。

## 差异

| 项目 | 来源 | 新实现 | 原因 |
| --- | --- | --- | --- |
| 运行输入 | browser video/ImageData | recorded FramePacket metadata + injected result | 先固定确定性回放边界，不触碰 UI |
| 识别后端 | Tesseract.js | 本轮仅 `RecordedNumberRecognizer` | 避免网络语言数据和浏览器调度破坏 L1 确定性 |
| parser | 同步 utility | 同语义独立 utility | 可在 Node 测试 |
| 失败 | value null + warning/error | error SensorEvent、空 measurements | 对齐统一契约，禁止假值 |
| 后处理 | UI sampling 层 round/filter | 未进入核心 OCR measurement | 保持 raw OCR 与应用物理过滤分离 |

## 来源兼容验证

- `tests/fixtures/ocr-number/recorded-results.json` 固定 rawText、source parsed value、confidence、duration、warning/error；
- TypeScript 测试对来源 parser 行为逐项比较，数值使用严格相等（普通 IEEE-754 parse）；
- replay 测试覆盖成功、有 warning、无法解析和 recognizer failure；
- 当前没有来源真实屏幕图片，因此不比较 Tesseract 像素输出，也不声称 OCR exact-match 精度。

## 许可证与资产

两个来源 commit 均未声明仓库许可证，GitHub metadata 为 `NOASSERTION`。本轮不复制 UI 文件或图片；只实现明确记录的适配边界。`license_review` 保持 `pending`，真实 Tesseract/预处理代码迁移前必须完成授权/许可证记录。
