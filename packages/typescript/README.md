# TypeScript package

继续保持一个 monorepo 内 package：`@physics-software-sensors/core`。当前未发布源码在 `0.3.0` package baseline 上增加 experimental `Vector3Assembler` Companion Tool；正式 package version 留待后续 Release 决策。Screen Capture、Number OCR/Tesseract 与 7 个 Sensor 的版本事实不变。

```bash
cd packages/typescript
npm install
npm test
```

```ts
import { ScreenCaptureSource, NumberOCRSensor, Vector3Assembler } from '@physics-software-sensors/core';
```

Browser source 只在用户调用 `start()` 时请求 `getDisplayMedia`；React、ROI、OCR、物理单位、屏幕授权 UI 与业务 store 都不属于 capture。`TesseractJsRecognizer` 首次可能获取 `eng` traineddata，模型数据不包含在 tarball。JSON 输出仍以根目录 Schema 为准。

Phase 4A 仅通过 GitHub Release tgz 分发，不发布 npm registry。参见 [installation](../../docs/installation.md)。

`Vector3Assembler` 处理已有标量 measurement，不产生直接观测，也不实现 Sensor 生命周期。其分量来源、时间差、坐标变换和 OCR composition 见 [`vector.compose-3d`](../../processing/vector.compose-3d/README.zh-CN.md)。该工具不在不可变的 `v0.6.0` tgz 中。
