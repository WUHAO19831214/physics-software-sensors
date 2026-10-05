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
