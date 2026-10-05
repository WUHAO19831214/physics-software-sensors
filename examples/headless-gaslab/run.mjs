import { GasSimulationEngine, GasSimulationDriver } from '../../packages/gaslab/dist/src/index.js';
const engine = new GasSimulationEngine({
  particleCount: 20, particleMass: 1, particleRadius: 0.05,
  container: { type: 'box', width: 2, height: 2, depth: 2 },
  initialTemperatureK: 300, randomSeed: 42,
});
const driver = new GasSimulationDriver(engine, 'replay');
driver.loadReplayData([
  { timestamp: 10, temperatureK: 300, pressureKPa: 100 },
  { timestamp: 10.5, temperatureK: 600, pressureKPa: 200 },
]);
const states = [];
driver.subscribe((snapshot, meta) => states.push({
  simulationSeconds: snapshot.timestamp, inputSeconds: meta.replayTimeSeconds,
  temperatureK: snapshot.temperatureK, externalPressureKPa: meta.currentPressureKPa,
  simulatedPressure: snapshot.statistics.microscopicImpulsePressure,
  simulatedPressureUnit: snapshot.statistics.microscopicImpulsePressureUnit,
}));
driver.tick(0.25);
driver.tick(0.25);
driver.setReplayPaused(true);
driver.tick(1);
console.log(JSON.stringify({ model: 'synthetic teaching replay', catalogCountDelta: 0, states }, null, 2));
