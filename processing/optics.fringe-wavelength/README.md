# Optical fringe wavelength inversion

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

`optics.fringe-wavelength` · `0.1.0` · experimental · unreleased

<!-- section:name -->
## Name

Optical fringe wavelength inversion

<!-- section:purpose -->
## Purpose

Optical fringe wavelength inversion; operates on existing observations, creates no new direct observation.

<!-- section:boundary -->
## Boundary

Optical fringe wavelength inversion; operates on existing observations, creates no new direct observation.

<!-- section:source -->
## Source

https://github.com/WUHAO19831214/webcam-laser-fringelab · `37a8b3996791790a22980b0d562996a65a3a65ef` · lib/physics.ts, lib/analysis.ts

<!-- section:input -->
## Input

calibrated positions, confirmed orders and a/d/L/errors

<!-- section:output -->
## Output

wavelength, regression, method/quality and uncertainty

<!-- section:example -->
## Example

```ts
import { Optics } from '@physics-software-sensors/fringelab';
const fit = Optics.fitDoubleSlitOrders({
  observations: [-2, -1, 0, 1, 2].map(order => ({
    order, screenPositionM: order * 0.0039
  })),
  screenDistanceM: 1.5,
  slitSeparationM: 0.00025,
  centerPositionM: 0
});
// Orders and metre positions must come from an explicitly confirmed workflow.
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
