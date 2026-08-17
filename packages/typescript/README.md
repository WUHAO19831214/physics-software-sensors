# TypeScript package

继续保持一个 monorepo 内 package：`@physics-software-sensors/core`。当前 `0.3.0` 新增 `ScreenCaptureSource`、`BrowserScreenBackend`、`RecordedScreenBackend` 与 FramePacket serializer，并保留 Phase 2 的 Number OCR/Tesseract 能力。

```bash
cd packages/typescript
npm install
npm test
```

```ts
import { ScreenCaptureSource, BrowserScreenBackend, NumberOCRSensor } from '@physics-software-sensors/core';
```

Browser source 只在用户调用 `start()` 时请求 `getDisplayMedia`；React、ROI、OCR、物理单位、屏幕授权 UI 与业务 store 都不属于 capture。`TesseractJsRecognizer` 首次可能获取 `eng` traineddata，模型数据不包含在 tarball。JSON 输出仍以根目录 Schema 为准。

Phase 4A 仅通过 GitHub Release tgz 分发，不发布 npm registry。参见 [installation](../../docs/installation.md)。
