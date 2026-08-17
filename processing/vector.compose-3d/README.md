# 3D Vector Composition & Reconstruction

**English** | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

<!-- section:name -->
## Name

`vector.compose-3d` · 3D Vector Composition & Reconstruction · version `0.1.0` · `experimental`

This is a **Companion Processing Tool**, not a Sensor.

<!-- section:purpose -->
## Purpose

Combine three scalar components into a traceable 3D vector with magnitude, normalized direction, azimuth and elevation. It is useful after OCR or other scalar measurements in force, magnetic-field, acceleration, velocity, and other experiments.

<!-- section:boundary -->
## Observation boundary

The tool makes no new direct observation. `screen.capture` observes screen pixels; `ocr.number` derives scalar readings; this tool processes those existing readings. A constrained component is never presented as an observed value.

<!-- section:source -->
## Source behavior

The Yan'an Ampere-force project historically treated F1/F2/F3 as x/y/z orthogonal scalar components. Current main observes Fy and Fz through OCR and explicitly constrains Fx to zero. The [Git history study](../../docs/research/yanan-vector-reconstruction-history.md) separates these two behaviors.

<!-- section:input -->
## Input

Each x/y/z component carries a finite value when available, one of `observed | derived | constrained | default | missing`, an optional timestamp in milliseconds, and its own confidence, uncertainty, warnings and errors. Quantity, unit and coordinate-system names are caller metadata, so the core is not force-specific.

<!-- section:output -->
## Output

`Vector3Measurement` contains components, magnitude, normalized vector, direction, latest component timestamp, component skew, status and unmerged per-component quality. Azimuth is degrees in `[0, 360)`, from +x toward +y in the x-y plane. Elevation is degrees in `[-90, 90]`, above the x-y plane toward +z. A zero vector has `normalized: null` and `direction: null`.

<!-- section:example -->
## Minimal example

```ts
import { Vector3Assembler } from '@physics-software-sensors/core';

const result = new Vector3Assembler({ maxComponentSkewMs: 150 }).compose({
  quantity: 'force',
  unit: 'N',
  coordinateSystem: 'classroom-x-y-z',
  components: {
    x: { value: 0, source: 'constrained' },
    y: { value: 1.2, source: 'observed', timestampMs: 1000 },
    z: { value: -0.8, source: 'observed', timestampMs: 1040 },
  },
});
```

An OCR error should be converted to `{ source: 'missing' }`; the result then remains `incomplete` and contains no invented vector.

<!-- section:quality -->
## Time and quality

If timestamp spread exceeds `maxComponentSkewMs`, the result is retained with `component-time-skew` and warning status. Component confidence is preserved separately; the tool never averages confidence and calls it vector accuracy.

<!-- section:coordinates -->
## Coordinates and optional renderer

Core mathematics uses the caller's x/y/z system. `CoordinateTransform3` is a separate matrix adapter. The Yan'an opt-in mapping is classroom `(x,y,z)` → Three.js scene `(-x,z,y)`. `createVector3RenderModel` emits axes/component/resultant arrow data without taking ownership of Three.js or application UI.

<!-- section:demo -->
## Demo and tests

Run the [small browser demo](../../examples/web-vector-compose-3d/README.md) in manual or recorded-OCR mode. Source golden, math, component-source, skew, coordinate and OCR-composition coverage is described in [benchmarks](benchmarks/README.md).

<!-- section:status -->
## Status and distribution

The tool is `experimental`, version `0.1.0`, and is available from the unreleased TypeScript source tree. It is not included in immutable Release `v0.6.0`, no `v0.7.0` has been published, and the repository still contains exactly seven Sensors.

<!-- section:limitations -->
## Known limitations

- No real-time downstream Yan'an integration has been performed.
- No physical calibration or metrological uncertainty is inferred.
- There is no Three.js dependency or full 3D scene renderer; the adapter emits renderer-neutral arrows.
- Caller-provided timestamps must share a clock domain.
- Performance across browsers and operating systems is not yet benchmarked.

<!-- section:provenance -->
## Provenance

See [SOURCE.md](SOURCE.md) for commit/file/symbol anchors and the clean-rewrite license decision. No code or assets were copied from the source repository.
