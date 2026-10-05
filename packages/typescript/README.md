# TypeScript package

继续保持一个 monorepo 内 package：`@physics-software-sensors/core`。当前未发布源码版本为 `0.3.1`，增加 experimental Vector3 与通用支持函数；不可变 v0.6.0 Release 仍分发旧 `0.3.0` tgz。Screen Capture、Number OCR/Tesseract 与 7 个 Sensor 的版本事实不变。

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

## Core 0.3.1 support utilities (unreleased)

`extractQuantities` parses configured unit/keyword candidates. Converted values use the primary unit and preserve `sourceUnit`; Celsius stays Celsius, not automatically kelvin. Keyword-only values assume the configured primary unit; bare values require `allowUnitless: true` in a dedicated numeric ROI. Parsing does not establish sensor accuracy.

`calculateLinearFit`/`extrapolateX` require a valid finite fit; origin-constrained centered R² can be negative. `ReadingStabilizer` rejects nonfinite numeric readings and out-of-order timestamps; held values are marked `isFresh: false` and stale samples must not be recorded as new observations. It can accept a new baseline after its holding interval expires.

`preprocessForNumberRecognition` keeps the existing default behavior; `padding` and `autoScale` are opt-in. These are support APIs, not new Sensor catalog entries. [Provenance](../gaslab/SOURCE.md) · [review](../../docs/gaslab-intake.md).
