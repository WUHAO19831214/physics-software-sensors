# Compatibility matrix

Every cell uses one of three support labels: **tested**, **expected but unverified**, or **unsupported**. “Expected” is not a compatibility claim.

The repository includes a reviewed CI template, but it is not enabled because the current GitHub OAuth token lacks `workflow` scope.

## Package/runtime compatibility

| Surface | macOS 26.3.1 arm64 | Linux | Windows | Notes |
| --- | --- | --- | --- | --- |
| Python 3.12.13 / NumPy 2.5.2 / OpenCV 4.14.0 | tested | expected but unverified (CI template only) | expected but unverified | headless OpenCV; no camera device |
| Python wheel `0.5.0` | tested | expected but unverified (CI template only) | expected but unverified | optional YOLO runtime excluded |
| Node 24.13.0 / TypeScript 5.9.3 | tested | expected but unverified (Node 22 template) | expected but unverified | npm engine floor is Node 18 |
| npm tgz `0.3.0` | tested | expected but unverified (CI template only) | expected but unverified | package remains `private: true`; not published |

## Device/browser compatibility

| Capability | Chrome | Edge | Firefox | Safari | Native device |
| --- | --- | --- | --- | --- | --- |
| `screen.capture` recorded backend | tested in Node | expected but unverified | expected but unverified | expected but unverified | unsupported |
| real `getDisplayMedia` chooser/capture | expected but unverified | expected but unverified | expected but unverified | expected but unverified | unsupported |
| `camera.capture` image sequence | unsupported | unsupported | unsupported | unsupported | tested synthetic |
| real camera permission/resolution/FPS | unsupported | unsupported | unsupported | unsupported | expected but unverified |

## Sensor-specific dependencies

| Sensor | Dependency | Status |
| --- | --- | --- |
| Color/Spot/Template and optional Camera | NumPy + `opencv-contrib-python-headless` | tested on macOS arm64 |
| Number OCR | Tesseract.js 7 + pngjs | tested on Node 24/macOS; browser runtime expected but unverified |
| YOLO recorded adapter | NumPy only | tested |
| YOLO real backend | Ultralytics + optional `lap` + approved local model | expected but unverified; model download unsupported by CI/release scripts |

Browser screen capture requires a secure context, transient user activation and renewed user permission; automation cannot silently grant it. See the [MDN `getDisplayMedia` reference](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getDisplayMedia).
