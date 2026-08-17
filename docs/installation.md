# Installation / 安装

Phase 4A 只准备 GitHub Release 文件，不发布 PyPI 或 npm registry。以下命令都使用已下载到当前目录的本地 artifact。

## Python core and extras

建议在 Python 3.11+ 的新虚拟环境中安装：

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install ./physics_software_sensors-0.5.0-py3-none-any.whl
```

Base wheel 提供 contracts/core；视觉功能按需安装：

```bash
# Color marker
python -m pip install './physics_software_sensors-0.5.0-py3-none-any.whl[color-marker]'

# Camera using OpenCV
python -m pip install './physics_software_sensors-0.5.0-py3-none-any.whl[camera-opencv]'

# Spot centroid and Template tracker
python -m pip install './physics_software_sensors-0.5.0-py3-none-any.whl[classical-trackers]'

# Offline recorded YOLO adapter; installs NumPy but not Ultralytics
python -m pip install './physics_software_sensors-0.5.0-py3-none-any.whl[yolo-recorded]'
```

多个 extra 可合并：

```bash
python -m pip install './physics_software_sensors-0.5.0-py3-none-any.whl[color-marker,camera-opencv,classical-trackers,yolo-recorded]'
```

### Real YOLO runtime boundary

只有在完成 runtime 与模型许可审查后才考虑：

```bash
python -m pip install './physics_software_sensors-0.5.0-py3-none-any.whl[yolo-runtime]'
```

这个 extra 会安装 Ultralytics/`lap`，但本仓库仍不会提供、选择或自动下载模型。调用者必须提供本地 `ModelArtifact` 路径、SHA-256 和许可证状态。GitHub Release 不包含 `.pt`、`.onnx`、`.engine` 或第三方权重。

## TypeScript package

Node 18+ 项目中使用本地 tgz：

```bash
npm install ./physics-software-sensors-core-0.3.0.tgz
```

```ts
import {
  ScreenCaptureSource,
  BrowserScreenBackend,
  NumberOCRSensor,
} from '@physics-software-sensors/core';
```

`ScreenCaptureSource` 的 recorded backend 可在 Node 中回放；真实 `getDisplayMedia` 需要支持该 API 的安全浏览器上下文、瞬时用户操作和用户授权。`TesseractJsRecognizer` 的真实 worker 可能获取或缓存语言数据，tgz 本身不捆绑 traineddata。

## Verify the install source

不要在本阶段运行 registry 命令 `pip install physics-software-sensors` 或 `npm install @physics-software-sensors/core`；那会表达尚未提供的 registry 分发。请先按 [download guide](downloading-sensors.md) 校验本地文件 SHA-256，再从本地 wheel/tgz 安装。
