# TypeScript package

Phase 2 保持一个 monorepo 内 package：`@physics-software-sensors/core`。当前 `0.2.0` 包含公共生命周期类型、Number OCR parser、统一事件 adapter 和确定性的 recorded-result replay recognizer。

```bash
cd packages/typescript
npm install
npm test
```

真实 Tesseract.js、Canvas/ImageData 预处理和屏幕 UI 尚未迁移；recorded replay 不应被描述为真实 OCR。JSON 输出仍以根目录 Schema 为准。
