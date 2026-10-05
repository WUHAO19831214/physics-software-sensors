// Compare fixed historical formula/output with the reviewed package; never execute working-tree source.
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import ts from '../packages/gaslab/node_modules/typescript/lib/typescript.js';
import {
  calculateRmsSpeed, calculateMostProbableSpeed, calculateMeanSpeed,
  maxwellBoltzmannSpeedPdf, sampleMaxwellVelocity, createSeededRandom,
} from '../packages/gaslab/dist/src/index.js';
const sourceRoot = process.argv[2];
if (!sourceRoot) throw new Error('Usage: node tools/compare_gaslab_source.mjs /path/to/charles-law-isochoric-lab');
const manifest = JSON.parse(readFileSync(new URL('../packages/gaslab/source-files.json', import.meta.url), 'utf8'));
const source = execFileSync('git', ['show', `${manifest.commit}:src/simulation/maxwellBoltzmann.ts`], { cwd: sourceRoot, encoding: 'utf8' });
const compiled = ts.transpileModule(source, { compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.CommonJS } }).outputText;
const exports = {};
const historicalMath = Object.create(Math);
const context = vm.createContext({ exports, Math: historicalMath });
vm.runInContext(compiled, context);
const calibration = { referenceTemperatureK: 300, referenceRmsSpeed: Math.sqrt(3) * 1.6 };
let comparisons = 0;
const close = (a, b) => { assert.ok(Math.abs(a - b) < 1e-12, `${a} != ${b}`); comparisons++; };
for (const temperature of [200, 300, 600]) {
  close(calculateRmsSpeed(temperature, calibration), exports.getTheoreticalVrms(temperature));
  close(calculateMostProbableSpeed(temperature, calibration), exports.getTheoreticalVp(temperature));
  close(calculateMeanSpeed(temperature, calibration), exports.getTheoreticalVavg(temperature));
  for (const speed of [0, 1, 2, 5]) close(maxwellBoltzmannSpeedPdf(speed, temperature, calibration), exports.maxwellPdf(speed, temperature));
  historicalMath.random = createSeededRandom(123);
  const rng = createSeededRandom(123);
  for (let i = 0; i < 100; i++) {
    const old = exports.sampleMaxwellVelocity(temperature);
    const current = sampleMaxwellVelocity(temperature, calibration, rng);
    close(current.x, old[0]); close(current.y, old[1]); close(current.z, old[2]);
  }
}
console.log(JSON.stringify({ sourceCommit: manifest.commit, sourcePath: 'src/simulation/maxwellBoltzmann.ts', comparisons, tolerance: 1e-12, calibration, status: 'pass' }));
