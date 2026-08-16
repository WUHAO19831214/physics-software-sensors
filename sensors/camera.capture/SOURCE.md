# 来源与抽取记录：camera.capture

## 固定来源

| 仓库/commit | 文件与原始符号 | 原用途 |
| --- | --- | --- |
| `audio-visual-soundfield-tracker-stable@85740d686c67452a057540edb564d713e01ccc51` | `src/camera_devices.py::camera_backends/open_camera/read_camera_preview/list_available_cameras` | 选择 OpenCV backend、请求宽高、读帧、释放设备 |
| 同上 | `src/local_capture.py::LocalCameraWorker.start/_run/stop`、`LocalFusionWorker._run` | 后台连续读帧；失败计数；墙钟/会话时钟；交给检测/同步业务 |
| 同上 | `src/browser_capture.py::LiveCountingProcessor.recv/FusionVideoProcessor.recv` | WebRTC `VideoFrame → BGR ndarray` 后交给 processor |
| 同上 | `src/camera_processor.py::CameraProcessor.process_frame` | 证明采集之后的检测/追踪是下游 processor，不属于 capture |
| `spot-vibration-tracking-system-20260508-171952@7f0d91cc73afafaecc54acc46b2b9d69375d994a` | `app.js::requestCamera/stopCamera/populateCameras/startTrackingLoop/trackRedSpot` | 用户授权、设备切换、video/canvas 与光斑处理 |
| `forced-vibration-af-analyzer-20260502-122715@c3f58175a09ff29cacdfb976a5055758c4eff619` | `app.js::requestCamera/stopCamera/populateCameras/trackRedSpot` | 受迫振动光斑视频输入 |
| `physics-experiment-bridge-mvp@8bba87df6475cae1e595fc925551db8bea83fb68` | `src/camera/CameraCapturePanel.tsx`、`src/utils/cameraUtils.ts` | 浏览器 video/canvas 采样后进入 vision analyzer |
| `ampere-force-visualizer-teacher-yanan@cb073e89d6d87129287030f1df08bd540504eb39` | `src/camera/CameraCapturePanel.tsx`、`src/utils/cameraUtils.ts` | 相同边界在教师端实际使用 |

## 抽取位置与方式

- 新实现：`packages/python/src/physics_sensors/capture/camera.py`；
- 公共 API：`CameraSource`、`CameraBackend`、`ImageSequenceCameraBackend`、`OpenCVCameraBackend`；
- 抽取方式：行为重写/adapter，不复制来源文件；
- 保留：后端可替换、请求宽高/FPS、逐帧 read、失败显式化、stop/release；
- 移除：Streamlit/React UI、线程共享预览、音频同步、Detector、YOLO、颜色/模板/光斑处理和实验 store；
- 新增：Schema-valid FramePacket、run/frame/sequence ID、wall/monotonic/source 三类时间、artifact SHA-256、requested/nominal/measured rate 分离、deterministic replay、health/drop counters；
- 算法修改：capture 没有测量算法。设备打开策略没有逐行复刻 macOS AVFoundation fallback；调用方可显式传 `api_preference`，后续真实设备矩阵再决定默认策略。

## 一致性与验证

来源层没有可公开 recorded camera dataset，因此本阶段不能做“同一真实帧逐输出” golden-master。采用保守的边界验证：

1. `ImageSequenceCameraBackend` 固定三帧与固定时间，验证完整 FramePacket Schema；
2. 请求 30 FPS、backend nominal 20 FPS、时间间隔实测 20 FPS 三者分别断言；
3. backend 的 dropped count 原样进入 quality 与 health；
4. `OpenCVCameraBackend` API 可独立导入，真实打开只由显式 `--device` smoke 触发；
5. 来源五仓库保持原 commit 与 clean，未写入任何文件。

真实设备一致性、AVFoundation/DirectShow/V4L2 backend、断流恢复与长期采集仍是 L2 TODO。

## 资产来源

`assets/captured-frame.png`、`frame-packet-metadata.png`、`backend-information.png` 和 `replay-frame-packets.json` 均由 `examples/python-camera-capture/run.py --publish-assets` 在本仓库生成。输入为 synthetic recorded frames；没有复制来源仓库或第三方图片。

## 许可证

本 adapter 为本仓库 MIT 代码。五个固定来源 commit 均无可识别 LICENSE（`NOASSERTION`），所以只记录行为与符号，不复制来源代码/资产；`license_review` 继续为 `pending`。
