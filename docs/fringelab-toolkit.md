[English](fringelab-toolkit.md) | [简体中文](fringelab-toolkit.zh-CN.md) | [日本語](fringelab-toolkit.ja.md)

<!-- section:overview -->
## FringeLab reusable components

Both batches are collected in `@physics-software-sensors/fringelab` 0.1.0. Fixed source: `webcam-laser-fringelab@37a8b3996791790a22980b0d562996a65a3a65ef`. The source application is unchanged. The calculator, overlays and image/camera utilities can be reused separately; no Next.js dependency is required.

<!-- section:catalog -->
## What is reusable

Calculator: pure arithmetic parser plus movable React floating panel. ROI: native-pixel geometry, rotation/resize and contain viewport mapping. Virtual ruler: endpoint/body movement, angle snapping, magnetic alignment, millimetre ticks. Calibration: confirmed two-point or piecewise multi-point mapping. Profile: channel selection, relative DN, background subtraction, saturation quality, smoothing, peaks/troughs, subpixel centres, FWHM, autocorrelation. Automatic ruler: existing horizontal/rotated/perspective detection and user-selected region, keeping manual fallback. Browser: local image/HEIC input, on-demand ruler OCR, getUserMedia capture/settings and exports. Optics: interference/diffraction inversion, multi-order regression, uncertainty and deterministic simulation.

<!-- section:run -->
## Run and integrate

Use the commands below from the repository root. For another project, build local tgz artifacts and install both core and FringeLab packages. Pure algorithms, shared-contract Sensors, browser helpers and optional React UI have separate entry points. The complete runnable example shows the wiring.

```sh
npm --prefix packages/typescript ci
npm --prefix packages/typescript run build
npm --prefix packages/fringelab ci
npm --prefix packages/fringelab test
npm --prefix examples/web-fringelab-toolkit ci
npm --prefix examples/web-fringelab-toolkit run dev
# Local artifacts + clean-install smoke test:
python3 tools/build_fringelab_artifacts.py
```

<!-- section:measurement -->
## Measurement decisions

Load the synthetic 650 nm sample, confirm the manual 30 mm ruler, then calculate. Multi-point mode accepts original-image anchors and editable readings. Automatic detection/OCR only populate drafts; verify units and known length before applying. Freeze a camera frame before calibration. Source changes clear calibration; ROI/parameters invalidate computed results. Intensity is DN/relative camera response, not lux or W/m². Multi-point mapping is one-dimensional, not a perspective homography. A clipped peak cannot recover lost amplitude or reliable FWHM.

<!-- section:verification -->
## Verification and reuse evidence

The 18 extracted files have pinned hashes; deterministic calculator, ROI, manual/automatic ruler, profiles, simulation and optical results match the fixed source exactly after normalizing arrays/timestamps. Original tests and adapter tests cover timing, errors, cancellation and stale calibration. A production browser check covers both calculators, focus restoration, manual/multi-point calibration, auto detection, optical inversion and 390 px layout. These are synthetic/offline checks. Physical camera, real-photo error distribution and optical metrology are not measured.

<!-- section:provenance -->
## Provenance and distribution

The source owner explicitly authorized collecting the components into this MIT repository. Extracted owner code uses the destination MIT license; third-party OCR/HEIC licenses remain distinct. HEIC is optional and dynamically loaded; OCR can fetch engine/language resources. No registry publish is performed. The existing v0.6.0 seven Sensor Bundles remain immutable. Two new Sensor Bundles and toolkit tgz are local build artifacts.

[Package API](../packages/fringelab/README.md) · [example](../examples/web-fringelab-toolkit/README.md) · [source](../packages/fringelab/SOURCE.md) · [evidence](../benchmarks/results/fringelab-extraction-2026-10-05.md)

![FringeLab production example, synthetic fixture](assets/fringelab-toolkit.png)
