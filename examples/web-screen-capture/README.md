# Web screen capture

两种证据彼此分开：

1. `generate_sample.py` + `run.mjs`：确定性 recorded screen replay，自动测试 FramePacket；
2. `browser.html`：人工点击后才调用 `getDisplayMedia`，验证真实浏览器权限/结束语义。

```bash
python examples/web-screen-capture/generate_sample.py
npm --prefix packages/typescript run build
node examples/web-screen-capture/run.mjs
python examples/web-screen-capture/build_assets.py --publish-assets
```

人工浏览器 smoke（先完成 TypeScript build）：

```bash
python -m http.server 8000
```

打开 `http://localhost:8000/examples/web-screen-capture/browser.html`，点击“选择屏幕/窗口/标签页”。页面刷新后通常需要重新授权。自动回放不证明浏览器、平台或权限兼容。
