# Independent FringeLab toolkit example

The app imports only published package entry points; it does not import the historical source project or access its state. Both batches are available: calculators, ROI, manual/automatic/multi-point ruler, local image/HEIC import, OCR candidates, camera, relative profile/features, optical inversion and export.

## Run

From the repository root, build packages/typescript and packages/fringelab with npm ci and npm run build. Then:

```sh
npm --prefix examples/web-fringelab-toolkit ci
npm --prefix examples/web-fringelab-toolkit run dev
```

Open http://127.0.0.1:4173. For production: npm run build, then npm run preview in this directory. The reproducible sample uses 650 nm, d=0.25 mm, L=1.5 m, a=0.04 mm and 25 px/mm. It is explicitly synthetic.

## Manual route

Select manual ruler, drag endpoints to two actual scale ticks, enter the known length and origin in mm, then click 核对并应用尺标. Check a/d/L before computing. The sample ruler is already aligned for convenience but still requires explicit confirmation.

## Multi-point route

Select 多点尺标. Enter the next true reading in mm and click its actual scale tick; add at least three points, edit/remove mistakes, then confirm. Readings must be distinct and the ruler axis should be parallel to the profile axis. Use the same screen plane; verify independent ticks.

## Automatic / OCR route

Click 自动检测刻线; if detection fails, use 框选实物尺 and click two opposite corners, retry or use manual scale. Detection creates candidates, not applied scale. OCR uses centimetre digit labels, converts to mm, matches nearby detected ticks and populates editable drafts. It never auto-applies. First OCR run may download trained data; photographs are not uploaded. Worker cancellation/source revision prevents old detection results from applying to new images.

## Camera and invalidation

Start only on HTTPS/localhost. Choose a device, optionally attempt setting locks, then freeze before calibration/computation. Returning to live capture or changing source invalidates calibration. Requested sampling and actual device settings are separate. No simulated output is substituted for denied camera permission.

Changes to ROI/channel/smoothing/optical parameters invalidate old computation. JSON keeps original DN profile, pixel axis, confirmed calibration, quality and optional computed result. CSV exports pixel/DN profile without display normalization.

Two floating calculators demonstrate unique IDs, independent expressions and focus behavior. Both are non-modal; the title handle can be dragged or moved with arrow keys. ROI/ruler operations also have numeric controls. Mobile layouts retain 16px fields.

[Toolkit guide](../../docs/fringelab-toolkit.md) · [Source record](../../packages/fringelab/SOURCE.md) · [Verification](../../benchmarks/results/fringelab-extraction-2026-10-05.md)
