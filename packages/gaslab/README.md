# GasLab experimental domain package

**English** | [简体中文](README.zh-CN.md) | [日本語](README.ja.md)

`@physics-software-sensors/gaslab` 0.1.0 is a headless, zero-runtime-dependency gas teaching model. It exports `.`, `./core`, `./physics`, `./simulation`, and `./driver` using NodeNext ESM (Node >=22.13). It is not published to npm or included in the immutable v0.6.0 Release.

## Build and install locally

```bash
npm ci --prefix packages/gaslab
npm --prefix packages/gaslab test
npm pack ./packages/gaslab --pack-destination /path/to/output
npm install /path/to/output/physics-software-sensors-gaslab-0.1.0.tgz
```

```ts
import { GasSimulationEngine, GasSimulationDriver } from '@physics-software-sensors/gaslab';
const engine = new GasSimulationEngine({
  particleCount: 200, particleMass: 1, particleRadius: 0.05,
  container: { type: 'cylinder', radius: 1.5, height: 4 },
  initialTemperatureK: 300, randomSeed: 42,
});
const driver = new GasSimulationDriver(engine, 'manual');
const unsubscribe = driver.subscribe((snapshot, meta) => console.log(snapshot.timestamp, meta.mode));
driver.tick(0.016);
unsubscribe();
```

See the [headless example](../../examples/headless-gaslab/README.md), [source record](SOURCE.md), and [intake/review record](../../docs/gaslab-intake.md).

## Model and units

- Maxwell-Boltzmann velocities use independent Gaussian Cartesian components. Speed is chi-distributed with three degrees of freedom; squared normalized speed is chi-squared. Temperature scaling is `sqrt(T2/T1)` with positive kelvin inputs.
- The default `display` calibration uses arbitrary distance/mass/speed units. `microscopicImpulsePressureUnit` is `simulation`, not Pa. `pedagogicalPressureRatio = T/T0` is a theoretical teaching ratio, not an inferred measurement.
- For `unitSystem: 'si'`, supply metres, kg, seconds and positive kelvin; omit `speedCalibration`. RMS speed is derived from `sqrt(3*kB*T/m)`. Pressure is then wall impulse/(wall area * window seconds), labelled Pa. No real-device accuracy has been established.
- Box and cylinder are centered at the origin. `capsule` means a straight cylinder of `cylinderHeight` with one bottom hemisphere and a flat top, not a two-ended capsule. Its area is `2*pi*r*h + 3*pi*r*r`.
- Particles do not collide with each other. Static walls reflect elastically. Adaptive substeps and projection keep particles contained but lose overshoot at collisions; collision timing and impulse statistics are approximations. This is not a general molecular-dynamics solver, moving piston, Boyle-law solver or metrology model.

## Engine and driver behavior

`step(dt)` consumes the full nonnegative duration in seconds; zero is a no-op. Invalid temperature, geometry, mass, duration and calibration throw `RangeError`. Steps exceeding one million internal substeps are rejected; advance high-speed systems in smaller intervals. Returned particle snapshots are independent copies. A seeded `reset()` reproduces initial particles.

`live` readings are supplied by the caller; there is no camera/OCR acquisition in this package. `replay` uses strictly increasing finite timestamps in seconds, starting at the first timestamp, and applies piecewise-constant readings at each recorded boundary. Playback speed scales both replay and simulation elapsed time. `setReplayPaused(true)` stops both. After the final reading the driver holds that input. `seekReplayIndex(i)` changes the input cursor; it does not reconstruct historical particle trajectories. Reset and replay from the beginning for deterministic trajectory reconstruction. Input records are copied.

External kPa readings remain `currentPressureKPa` metadata, separate from simulated wall pressure. `MicroscopicStatisticsAccumulator.compute(..., referencePressureKPa)` can additionally derive `stateEquationPressure`; the engine does not invent a reference sensor pressure. Fixed windows include startup time with no collisions, so early frequency/pressure values are biased low.

## Validation and rollback

Run the pure logic tests and headless example. Synthetic checks exercise speeds, conservation, geometry, time, units and replay; they do not validate a physical apparatus. Uninstall this unreleased package or pin the previous PSS/source commit to roll back. Sensor/Companion Tool counts remain 9/4 (13 total).
