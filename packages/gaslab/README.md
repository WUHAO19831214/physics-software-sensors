# @physics-software-sensors/gaslab

Reusable gas kinetics, Maxwell-Boltzmann velocity sampling, container boundary collisions, and thermodynamic simulation driver.

## Features

- **Maxwell-Boltzmann Sampling & Scaling**:
  - Exact 3D Gaussian velocity sampling with customizable calibrations (SI units or visual simulation scale).
  - Exact speed PDF and characteristic speeds ($v_p, \bar{v}, v_{\text{rms}}$).
  - Continuous temperature scaling preserving velocity distribution: $v \leftarrow v \sqrt{T_2 / T_1}$.
- **Container Geometry & Elastic Collisions**:
  - Box, Cylinder, and Capsule (cylinder with hemispherical cap) bounding volumes.
  - Energy-conserving specular reflections and impulse tracking.
  - Boundary penetration clamping to prevent numerical tunneling.
- **Physical Statistics Accumulator**:
  - Sliding-window collision frequency ($f \propto \sqrt{T}$).
  - Microscopic impulse pressure $p_{\text{micro}} = \frac{\sum 2m|v_n|}{A \cdot \Delta t}$.
  - Educational pressure ratio $R_p = \frac{f}{f_0} \cdot \frac{\bar{I}}{\bar{I}_0} = \frac{T}{T_0}$.
- **Decoupled Simulation Driver**:
  - Zero dependencies on React, Three.js, Canvas, or the DOM.
  - Three driver modes: `live` (sensor input), `replay` (recorded dataset), and `manual` (interactive slider).
  - Deterministic pseudo-random number generator for reproducible experiment runs and unit tests.

## Installation

```bash
npm install @physics-software-sensors/gaslab
```

## Basic Usage

```ts
import { GasSimulationEngine, GasSimulationDriver } from '@physics-software-sensors/gaslab';

const engine = new GasSimulationEngine({
  particleCount: 200,
  particleMass: 1.0,
  container: { type: 'cylinder', radius: 1.5, height: 4.0 },
  initialTemperatureK: 300,
  randomSeed: 42,
});

// Advance one simulation step
const snapshot = engine.step(0.016);
console.log('Mean speed:', snapshot.statistics.meanSpeed);
console.log('Collision frequency:', snapshot.statistics.collisionFrequencyHz);
```
