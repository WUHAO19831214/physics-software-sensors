# Confirmed two-point and piecewise local scale

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

`calibration.scale-1d` · `0.1.0` · experimental · unreleased

<!-- section:name -->
## Name

Confirmed two-point and piecewise local scale

<!-- section:purpose -->
## Purpose

Confirmed two-point and piecewise local scale; operates on existing observations, creates no new direct observation.

<!-- section:boundary -->
## Boundary

Confirmed two-point and piecewise local scale; operates on existing observations, creates no new direct observation.

<!-- section:source -->
## Source

https://github.com/WUHAO19831214/webcam-laser-fringelab · `37a8b3996791790a22980b0d562996a65a3a65ef` · lib/ruler.ts, lib/spatial.ts

<!-- section:input -->
## Input

pixel points + known mm readings + source/calibration IDs

<!-- section:output -->
## Output

position mm, extrapolation and stale status

<!-- section:example -->
## Example

```ts
import { confirmTwoPointCalibration, calibratedPosition,
  confirmMultiPointCalibration } from '@physics-software-sensors/fringelab';
const scale = confirmTwoPointCalibration({ start: { x: 20, y: 40 },
  end: { x: 120, y: 40 }, knownLengthMm: 10 }, 'photo:1', 'scale:1');
const position = calibratedPosition({ x: 70, y: 40 }, scale, 'photo:1');
// position.valueMm === 5; a different source key returns stale/null.
const localScale = confirmMultiPointCalibration([
  { x: 0, y: 0, mm: 0 }, { x: 100, y: 0, mm: 10 },
  { x: 220, y: 0, mm: 20 }
], 'photo:1', 'scale:2');
```

[Runnable example](../../examples/web-fringelab-toolkit/README.md)

<!-- section:quality -->
## Quality

Preserve clipping, confirmation, source revision and input uncertainty; stale data must not become current measurement.

<!-- section:coordinates -->
## Coordinates

Original-image pixels, mm calibration and metre-based optics. No implied 2D homography.

<!-- section:demo -->
## Demo

Standalone browser runtime; all images stay local. [Demo](../../examples/web-fringelab-toolkit/README.md)

<!-- section:status -->
## Status

experimental; evidence does not imply metrological validation. Version 0.1.0, unreleased; v0.6.0 unchanged.

<!-- section:limitations -->
## Limitations

No lux/W/m². Keep channel, source clipping and sample coverage. Millimetre tick model; possible period ambiguity; OCR/scale require human confirmation. One-dimensional calibration is not homography.

<!-- section:provenance -->
## Provenance

[SOURCE.md](SOURCE.md)
