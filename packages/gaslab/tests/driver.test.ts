import { test } from 'node:test';
import assert from 'node:assert/strict';
import { GasSimulationEngine } from '../src/simulation/engine.js';
import { GasSimulationDriver } from '../src/driver/simulationDriver.js';

test('GasSimulationDriver in live mode responds to sensor readings', () => {
  const engine = new GasSimulationEngine({
    particleCount: 20,
    particleMass: 1.0,
    container: { type: 'cylinder', radius: 1.0, height: 2.0 },
    initialTemperatureK: 300,
    randomSeed: 123,
  });

  const driver = new GasSimulationDriver(engine, 'live');
  let lastMetaTemp = 0;
  let lastPressure: number | undefined;

  driver.subscribe((_snapshot, meta) => {
    lastMetaTemp = meta.currentTemperatureK;
    lastPressure = meta.currentPressureKPa;
  });

  // Sensor updates
  driver.updateLiveReading(350, 115.4);
  driver.tick(0.016);

  assert.equal(engine.getTemperature(), 350);
  assert.equal(lastMetaTemp, 350);
  assert.equal(lastPressure, 115.4);
});

test('GasSimulationDriver in replay mode steps through recorded points', () => {
  const engine = new GasSimulationEngine({
    particleCount: 20,
    particleMass: 1.0,
    container: { type: 'box', width: 2.0, height: 2.0, depth: 2.0 },
    initialTemperatureK: 290,
    randomSeed: 456,
  });

  const driver = new GasSimulationDriver(engine, 'replay');
  const recorded = [
    { timestamp: 0.0, temperatureK: 290, pressureKPa: 100.0 },
    { timestamp: 1.0, temperatureK: 310, pressureKPa: 107.0 },
    { timestamp: 2.0, temperatureK: 330, pressureKPa: 114.0 },
  ];

  driver.loadReplayData(recorded);

  let currentIdx = -1;
  let currentProg = -1;
  driver.subscribe((_snap, meta) => {
    currentIdx = meta.replayIndex ?? -1;
    currentProg = meta.replayProgress ?? -1;
  });

  // At t=0
  driver.tick(0.0);
  assert.equal(currentIdx, 0);
  assert.equal(engine.getTemperature(), 290);

  // Advance by 1.1s -> should transition to index 1
  driver.tick(1.1);
  assert.equal(currentIdx, 1);
  assert.equal(engine.getTemperature(), 310);
  assert.equal(currentProg, 0.5);

  // Seek
  driver.seekReplayIndex(2);
  driver.tick(0.01);
  assert.equal(currentIdx, 2);
  assert.equal(engine.getTemperature(), 330);
  assert.equal(currentProg, 1.0);
});

test('Simulation reproducibility with identical PRNG seeds', () => {
  const config = {
    particleCount: 25,
    particleMass: 1.0,
    container: { type: 'cylinder' as const, radius: 1.2, height: 2.5 },
    initialTemperatureK: 300,
    randomSeed: 5555,
  };

  const engineA = new GasSimulationEngine(config);
  const engineB = new GasSimulationEngine(config);

  for (let step = 0; step < 20; step++) {
    const snapA = engineA.step(0.016);
    const snapB = engineB.step(0.016);

    for (let i = 0; i < snapA.particleCount; i++) {
      const pa = snapA.particles[i]!;
      const pb = snapB.particles[i]!;
      assert.equal(pa.position.x, pb.position.x);
      assert.equal(pa.position.y, pb.position.y);
      assert.equal(pa.position.z, pb.position.z);
      assert.equal(pa.velocity.x, pb.velocity.x);
      assert.equal(pa.velocity.y, pb.velocity.y);
      assert.equal(pa.velocity.z, pb.velocity.z);
    }
  }
});
