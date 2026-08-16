# TypeScript package

Phase 2 保持一个 monorepo 内 package：`@physics-software-sensors/core`。当前 `0.2.0` 包含公共生命周期类型、RGBA pixel/ROI/preprocess、Number OCR parser、统一事件 adapter、确定性 recorded replay 和真实 `TesseractJsRecognizer`。

```bash
cd packages/typescript
npm install
npm test
```

```ts
import { NumberOCRSensor, TesseractJsRecognizer } from '@physics-software-sensors/core';
```

`TesseractJsRecognizer` 在 Node 使用 PNG buffer、在浏览器使用 Canvas，并复用/关闭自己的 worker。React、屏幕授权 UI 和业务 store 不属于 package。首次真实 OCR 可能获取 `eng` traineddata；模型数据不包含在 tarball。JSON 输出仍以根目录 Schema 为准。
