# FringeLab reusable toolkit

Experimental 0.1.0. Both extraction batches are implemented: arithmetic calculator; ROI/viewport; virtual/manual ruler; confirmed two-point/multi-point calibration; relative RGBA profile and signal features; automatic ruler ticks; local ruler-number OCR; browser camera; optics regression/uncertainty and diffraction simulation. React UI and browser backends are separate subpath entry points; pure core does not import React or DOM state.

## Build and verify

```sh
npm --prefix packages/typescript ci
npm --prefix packages/typescript run build
npm --prefix packages/fringelab ci
npm --prefix packages/fringelab test
npm --prefix examples/web-fringelab-toolkit ci
npm --prefix examples/web-fringelab-toolkit run build
npm --prefix examples/web-fringelab-toolkit run dev
```

## Pure algorithms

```ts
import { Signal, Roi, Ruler, Optics, Simulator, calculateExpression,
  confirmTwoPointCalibration, calibratedPosition } from '@physics-software-sensors/fringelab';
const value = calculateExpression('2^-2 + 1e-3');
const strip = Signal.extractStripProfile(rgba, { channel: 'auto', roi });
const smooth = Signal.gaussianSmooth(strip.profile, 1.8);
const peaks = Signal.detectPeaks(smooth, { minProminence: 2 });
const calibration = confirmTwoPointCalibration(ruler, 'photo:revision-1', 'calibration-1');
const location = calibratedPosition({ x: 100, y: 50 }, calibration, 'photo:revision-1');
```

`rgba`, `roi` and `ruler` are caller inputs in original-image pixels. Units are explicit: ruler mm, optics metres, simulator documented mm/nm/m fields. Core subpaths such as `/core/signal` allow narrower imports.

## Sensors

```ts
import { StripProfileSensor, RulerTicksSensor } from '@physics-software-sensors/fringelab/sensors';
const sensor = new StripProfileSensor();
sensor.configure({ channel: 'r', roi });
await sensor.start({ runId: frame.runId });
for await (const event of sensor.process(frame)) console.log(event);
await sensor.stop();
```

Consumes shared RuntimeFramePacket with original RGBA pixels. Parent-frame time is preserved; emitted time is separate. Zero coverage/not-found is lost; errors contain no measurements. Ruler detections are always unconfirmed candidates, never applied scale.

## Browser and React

```tsx
import { FloatingCalculator, RoiOverlay, RulerOverlay } from '@physics-software-sensors/fringelab/react';
import '@physics-software-sensors/fringelab/styles.css';
// Inside a browser/client component:
<FloatingCalculator onResult={(value, expression) => console.log(value, expression)} />
<RoiOverlay roi={roi} size={imageSize} onChange={setRoi} />
<RulerOverlay ruler={ruler} size={imageSize} onChange={setRuler} />
```

UI is controlled and can be placed over any image/Canvas. Overlays use original-image SVG coordinates. ROI supports move, rotate and four-corner resize. Ruler supports endpoints, moving, Shift angle snapping and Alt magnetic bypass. Floating calculators can be instantiated multiple times, moved by pointer/arrow keys, closed with Esc, and restore trigger focus.

Browser entry point exports `BrowserCameraSource`, source camera helpers, `RulerDetectionRunner`, `recognizeRulerReadings`, image decoding and CSV/download helpers. Call `runner.cancel()` on source changes and `camera.stop()` on unmount. Camera defaults to 250 ms sampling, separately from requested device FPS, and marks hardware-drop counts as unavailable. Permission failure never falls back to invented camera data.

## Distribution

Build `packages/typescript` and this package, then use `python3 tools/build_fringelab_artifacts.py` for both tgz files, two new Sensor Bundles and a clean-install/SSR/type check (outputs under `build/fringelab`). You can also run `npm pack` each into an artifact directory. Consumers install the two tgz files; React is optional for algorithm users. Nothing is published to npm. HEIC is optional; OCR is on-demand and may fetch trained data. Existing Release v0.6.0 is unchanged.

See [SOURCE.md](SOURCE.md), [third-party notices](THIRD_PARTY_NOTICES.md), [full toolkit guide](../../docs/fringelab-toolkit.md) and [browser example](../../examples/web-fringelab-toolkit/README.md).

## Measurement boundaries

DN/relative response is not lux or W/m². Clipped peaks cannot yield recovered amplitude/FWHM. Colored-fringe auto-channel logic is a named optics strategy, not a universal radiometry estimator. Multi-point calibration is 1D piecewise mapping, not a 2D homography. Known length, units, same plane and axis direction require user verification. Invalid/stale calibration or changed processing must invalidate calculation snapshots. Automatic ruler confidence is algorithm confidence, not physical accuracy. Optics core preserves source defaults; applications must explicitly pass measurementReady and their actual error inputs.
