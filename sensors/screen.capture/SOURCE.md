# 来源与抽取记录：screen.capture

## 固定来源

| 仓库/commit | 文件与原始符号 | 原用途 |
| --- | --- | --- |
| `physics-experiment-bridge-mvp@8bba87df6475cae1e595fc925551db8bea83fb68` | `src/screen/ScreenCapturePanel.tsx::startCapture`（`getDisplayMedia`，约 169 行）、`stopCapture`（约 190 行）、sampling interval（约 222 行） | 用户选择共享源、video 流、定时 ROI/OCR |
| 同上 | `src/screen/screenCaptureRuntime.ts::setScreenCaptureVideoElement/getScreenCaptureVideoElement` | UI 与识别器之间共享 video element |
| 同上 | `docs/SCREEN_CAPTURE_PIPELINE.md` | 明确网页不能静默读桌面或访问实验软件内部数据 |
| `ampere-force-visualizer-teacher-yanan@cb073e89d6d87129287030f1df08bd540504eb39` | `src/screen/ScreenCapturePanel.tsx::startCapture`（约 152 行）、`stopCapture`（约 173 行）、sampling interval（约 205 行） | 教师端授权屏幕流进入 OCR |
| 同上 | `src/utils/imagePreprocess.ts::cropRoiFromVideo`、`docs/SENSOR_INTEGRATION.md`、`docs/DATA_PIPELINE.md` | video/canvas/ROI 与 OCR/物理业务边界 |

## 抽取位置与方式

- 新实现：`packages/typescript/src/capture/screen.ts`；
- 公共 API：`ScreenCaptureSource`、`BrowserScreenBackend`、`MediaDevicesScreenDriver`、`RecordedScreenBackend`、`serializeRuntimeFramePacket`；
- 抽取方式：行为重写/adapter，不复制 React component；
- 保留：显式 `getDisplayMedia`、video/canvas RGBA、track ended、stop 全 tracks、请求采样间隔；
- 移除：React UI、ROI、recognizer 选择、OCR、number parser、过滤、单位、experiment/classroom store 和可视化；
- 新增：统一 lifecycle、FramePacket、runtime pixel binding、artifact hash、wall/monotonic/source time、requested/measured interval 分离、稳定 error codes、deterministic replay；
- 行为变化：来源将采集与 OCR 放在同一 panel；新库强制拆成可组合 source 与 processor。浏览器拒绝/结束不再只表现为 UI 状态，而是显式错误。

## 一致性与验证

1. fake browser driver 断言构造/configure 不触发权限，只有 `start()` 请求一次；
2. permission denial 保留 `SCREEN_CAPTURE_PERMISSION_DENIED`，不伪装设备故障；
3. 两帧 recorded replay 断言 requested 100 ms 与 measured 250 ms 分离，并保留 dropped count；
4. 实际 serialized output 通过 FramePacket JSON Schema；
5. recorded ScreenCaptureSource frame 既通过 recorded recognizer composition，也通过真实 Tesseract.js `-2.33` pixel composition；
6. 未运行/声称浏览器或真实屏幕人工 smoke；人工入口已在 example 提供。

## 资产来源

`assets/captured-screen-frame.png`、`frame-packet-metadata.png`、`permission-boundary.png`、`replay-frame-packet.json` 由 `examples/web-screen-capture/` 生成。输入是本仓库 synthetic shared-window pixels；没有复制来源仓库或第三方图片。

## 许可证

本 adapter 为本仓库 MIT 代码。两个来源固定 commit 无可识别 LICENSE（`NOASSERTION`），因此不复制原实现或截图；`license_review` 继续为 `pending`。
