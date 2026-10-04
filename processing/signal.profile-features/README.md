# One-dimensional profile features

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

`signal.profile-features` · `0.1.0` · experimental · unreleased

<!-- section:name -->
## Name

One-dimensional profile features

<!-- section:purpose -->
## Purpose

One-dimensional profile features; operates on existing observations, creates no new direct observation.

<!-- section:boundary -->
## Boundary

One-dimensional profile features; operates on existing observations, creates no new direct observation.

<!-- section:source -->
## Source

https://github.com/WUHAO19831214/webcam-laser-fringelab · `37a8b3996791790a22980b0d562996a65a3a65ef` · lib/signal.ts

<!-- section:input -->
## Input

finite signal array + axis/sample semantics + processing options

<!-- section:output -->
## Output

processed profile, peak/trough centers, widths and periods

<!-- section:example -->
## Example

```ts
import { Signal } from '@physics-software-sensors/fringelab';
const samples = Float64Array.from([0, 1, 3, 8, 13, 8, 3, 1, 0]);
const smoothed = Signal.gaussianSmooth(samples, 0.8);
const peaks = Signal.detectPeaks(smoothed, { minProminence: 2, minDistance: 3 });
const period = Signal.estimatePeriodAutocorrelation(smoothed);
// A short signal need not contain a measurable period. Widths are in samples;
// convert using the original pixel axis and confirmed scale, not display size.
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
