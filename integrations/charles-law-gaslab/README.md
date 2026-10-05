# Charles-law local consumer evidence

Source repository: https://github.com/WUHAO19831214/charles-law-isochoric-lab. Historical source commit and paths are pinned in [GasLab provenance](../../packages/gaslab/SOURCE.md).

Status: **local uncommitted adaptation**, not a remotely merged integration. The source package.json references local Core 0.3.0 and gaslab 0.1.0 tarballs. Imports in `src/simulation/maxwellBoltzmann.ts` delegate sampling, temperature scaling and PDF functions. The Claude model re-exports that adapter; `src/utils/mathFitting.ts`, `src/sensors/ocrRecognizer.ts`, and App's stabilizers import Core. Rendered molecular engines and replay UI remain local. Merely exercising GasSimulationEngine in a script does not migrate the live UI to it.

The source checkout's 7 verification groups and production build were rerun successfully. Updated reviewed tarballs (Core 0.3.1, gaslab 0.1.0) are installed and tested in a temporary copy of those current source files; its working checkout and local package tarballs are not replaced. See [verification record](../../benchmarks/results/gaslab-intake.json).

Scope: no real camera/screen/OCR device acquisition was exercised. Static preview HTTP 200 alone does not establish functional browser or physics correctness. No feature-flag live migration/rollback comparison has been completed, so E5 evidence remains unchanged.

Next downstream work: commit the app's adaptation, pin reviewed tarball hashes, and validate the actual rendered/replay flows before replacing its full engines. Rollback uses the source git baseline and previous tarballs. PSS original transfer branches remain available. No source application is copied into this repository.
