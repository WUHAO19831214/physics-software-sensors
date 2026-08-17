# 安装

[English](installation.md) | **简体中文** | [日本語](installation.ja.md)

<!-- section:prerequisites -->
## 前置条件

- Python 包需要 Python 3.11+。
- TypeScript 包需要 Node.js 18+。
- 从 [`v0.6.0` Experimental](https://github.com/WUHAO19831214/physics-software-sensors/releases/tag/v0.6.0) 下载 artifact；本项目没有 registry 包。

<!-- section:python -->
## Python

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install ./physics_software_sensors-0.5.0-py3-none-any.whl
```

只安装实际需要的 extra：

```bash
python -m pip install './physics_software_sensors-0.5.0-py3-none-any.whl[color-marker]'
python -m pip install './physics_software_sensors-0.5.0-py3-none-any.whl[camera-opencv]'
python -m pip install './physics_software_sensors-0.5.0-py3-none-any.whl[classical-trackers]'
python -m pip install './physics_software_sensors-0.5.0-py3-none-any.whl[yolo-recorded]'
```

`yolo-runtime` 只应在完成许可证审查后安装可选的 Ultralytics/`lap`。它不会提供、选择或下载模型；调用方必须提供已审核的本地 `ModelArtifact` 路径、SHA-256 和许可证状态。

<!-- section:typescript -->
## TypeScript

```bash
npm install ./physics-software-sensors-core-0.3.0.tgz
```

```ts
import { ScreenCaptureSource, BrowserScreenBackend, NumberOCRSensor } from '@physics-software-sensors/core';
```

浏览器采集需要安全上下文、用户操作和明确授权。真实 Tesseract.js 可能获取/缓存语言数据；tgz 不捆绑 traineddata。

<!-- section:verification -->
## 验证安装来源

安装前先校验 SHA-256。本版本不要把 `pip install physics-software-sensors` 或 `npm install @physics-software-sensors/core` 当作 registry 安装命令。参阅[下载传感器](downloading-sensors.zh-CN.md)。
