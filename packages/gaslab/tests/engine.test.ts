import { test } from 'node:test';
import assert from 'node:assert/strict';
import { GasSimulationEngine } from '../src/simulation/engine.js';
import { DISPLAY_CALIBRATION } from '../src/physics/maxwellBoltzmann.js';

test('GasSimulationEngine initializes particles and advances simulation', () => {
  const engine = new GasSimulationEngine({
    particleCount: 50,
    particleMass: 1.0,
    particleRadius: 0.05,
    container: { type: 'cylinder', radius: 1.5, height: 3.0 },
    initialTemperatureK: 300,
    randomSeed: 777,
  });

  assert.equal(engine.getTemperature(), 300);
  const initialSnapshot = engine.getSnapshot();
  assert.equal(initialSnapshot.particleCount, 50);
  assert.equal(initialSnapshot.stepIndex, 0);

  // Advance 10 steps of dt = 0.016s (~160ms)
  let snapshot = initialSnapshot;
  for (let i = 0; i < 10; i++) {
    snapshot = engine.step(0.016);
  }

  assert.equal(snapshot.stepIndex, 10);
  assert.ok(snapshot.timestamp > 0.15);
  // Speeds should remain close to calibration RMS
  assert.ok(Math.abs(snapshot.statistics.rmsSpeed - DISPLAY_CALIBRATION.referenceRmsSpeed) < 0.5);
  // Some collisions should have occurred
  assert.ok(snapshot.statistics.collisionCountTotal > 0);
  assert.ok(snapshot.statistics.collisionFrequencyHz > 0);
  assert.ok(snapshot.statistics.microscopicImpulsePressure > 0);
});

test('Temperature scaling scales particle speeds predictably', () => {
  const engine = new GasSimulationEngine({
    particleCount: 100,
    particleMass: 1.0,
    container: { type: 'box', width: 2.0, height: 2.0, depth: 2.0 },
    initialTemperatureK: 300,
    randomSeed: 42,
  });

  const vrms0 = engine.getSnapshot().statistics.rmsSpeed;

  // Double temperature to 600K -> v_rms should scale by sqrt(2) ≈ 1.4142
  engine.setTemperature(600);
  const vrms1 = engine.getSnapshot().statistics.rmsSpeed;

  const ratio = vrms1 / vrms0;
  assert.ok(
    Math.abs(ratio - Math.SQRT2) < 0.01,
    `Expected ratio ~ 1.4142, got ${ratio}`
  );
  assert.equal(engine.getTemperature(), 600);
});

test('Engine reset re-establishes initial state', () => {
  const engine = new GasSimulationEngine({
    particleCount: 30,
    particleMass: 1.0,
    container: { type: 'cylinder', radius: 1.0, height: 2.0 },
    initialTemperatureK: 300,
    randomSeed: 999,
  });

  engine.step(0.1);
  engine.setTemperature(400);
  assert.equal(engine.getTemperature(), 400);

  engine.reset();
  assert.equal(engine.getTemperature(), 300);
  const snap = engine.getSnapshot();
  assert.equal(snap.stepIndex, 0);
  assert.equal(snap.timestamp, 0);
  assert.equal(snap.statistics.collisionCountTotal, 0);
});

test('step consumes the requested duration, zero does not advance, snapshots are independent', () => {
  const engine = new GasSimulationEngine({ particleCount: 10, particleMass: 1,
    container: { type: 'box', width: 2, height: 2, depth: 2 }, initialTemperatureK: 300, randomSeed: 42 });
  const initial = engine.getSnapshot();
  const frozen = JSON.stringify(initial);
  assert.equal(engine.step(0).timestamp, 0);
  assert.equal(engine.step(1).timestamp, 1);
  assert.equal(JSON.stringify(initial), frozen);
  initial.particles[0]!.position.x = 1e10;
  assert.ok(Math.abs(engine.getSnapshot().particles[0]!.position.x) < 1);
  assert.throws(() => engine.step(NaN), RangeError);
  assert.throws(() => engine.step(-1), RangeError);
});

test('seeded reset reproduces the same particle state and protects configuration', () => {
  const config = { particleCount: 10, particleMass: 1, container: { type: 'cylinder' as const, radius: 1, height: 3 }, initialTemperatureK: 300, randomSeed: 7 };
  const engine = new GasSimulationEngine(config);
  const initial = engine.getSnapshot();
  config.container.radius = 1000;
  assert.equal(engine.config.container.type === 'cylinder' && engine.config.container.radius, 1);
  engine.step(1);
  engine.reset();
  assert.deepEqual(engine.getSnapshot(), initial);
});

test('SI mode derives nitrogen speeds from mass and labels pressure; display is distinct', () => {
  const config = { particleCount: 1000, particleMass: 4.65e-26, particleRadius: 0,
    container: { type: 'box' as const, width: 1, height: 1, depth: 1 }, initialTemperatureK: 300, randomSeed: 32 };
  const si = new GasSimulationEngine({ ...config, unitSystem: 'si' });
  assert.equal(si.getSnapshot().statistics.microscopicImpulsePressureUnit, 'Pa');
  assert.ok(Math.abs(si.getSnapshot().statistics.rmsSpeed / 516.9 - 1) < 0.04);
  assert.equal(new GasSimulationEngine(config).getSnapshot().statistics.microscopicImpulsePressureUnit, 'simulation');
  assert.throws(() => new GasSimulationEngine({ ...config, initialTemperatureK: -1 }), RangeError);
});

test('SI box wall pressure has the expected ideal-gas order of magnitude', () => {
  const engine = new GasSimulationEngine({ particleCount: 200, particleMass: 4.65e-26, particleRadius: 0,
    container: { type: 'box', width: 1, height: 1, depth: 1 }, initialTemperatureK: 300,
    randomSeed: 42, unitSystem: 'si', frequencyWindowSeconds: 0.1 });
  for (let i = 0; i < 30; i++) engine.step(0.01);
  const expected = 200 * 1.380649e-23 * 300; // N kB T / V, V=1 m^3
  const measured = engine.getSnapshot().statistics.microscopicImpulsePressure;
  // Finite sample + projected collision timing; coarse synthetic sanity, not metrology.
  assert.ok(Math.abs(measured / expected - 1) < 0.15);
});
