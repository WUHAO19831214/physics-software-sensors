import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  calculateRmsSpeed,
  calculateMostProbableSpeed,
  calculateMeanSpeed,
  maxwellBoltzmannSpeedPdf,
  sampleMaxwellVelocity,
  calculateTemperatureScaling,
  DISPLAY_CALIBRATION,
  SI_CALIBRATION_NITROGEN,
} from '../src/physics/maxwellBoltzmann.js';
import { createSeededRandom } from '../src/core/prng.js';
import { lengthVector3D } from '../src/core/vector3d.js';

test('Maxwell-Boltzmann characteristic speed ordering and relations', () => {
  const T = 300;
  const vp = calculateMostProbableSpeed(T, DISPLAY_CALIBRATION);
  const vbar = calculateMeanSpeed(T, DISPLAY_CALIBRATION);
  const vrms = calculateRmsSpeed(T, DISPLAY_CALIBRATION);

  // Theoretical physics relation: v_p < v_bar < v_rms
  assert.ok(vp < vbar, `Expected v_p (${vp}) < v_bar (${vbar})`);
  assert.ok(vbar < vrms, `Expected v_bar (${vbar}) < v_rms (${vrms})`);

  // Exact analytical ratios
  assert.ok(Math.abs(vp / vrms - Math.sqrt(2 / 3)) < 1e-6);
  assert.ok(Math.abs(vbar / vrms - Math.sqrt(8 / (3 * Math.PI))) < 1e-6);
  assert.equal(vrms, 2.5); // reference at 300K
});

test('Maxwell-Boltzmann SI units for Nitrogen (N2)', () => {
  const T = 300;
  const vrms = calculateRmsSpeed(T, SI_CALIBRATION_NITROGEN);
  // Nitrogen at 300K has v_rms ≈ 516.8 m/s
  assert.ok(Math.abs(vrms - 516.82) < 0.1);
});

test('Maxwell-Boltzmann speed PDF properties', () => {
  const T = 300;
  const vp = calculateMostProbableSpeed(T, DISPLAY_CALIBRATION);
  const vrms = calculateRmsSpeed(T, DISPLAY_CALIBRATION);

  const pdfAtZero = maxwellBoltzmannSpeedPdf(0, T, DISPLAY_CALIBRATION);
  const pdfAtVp = maxwellBoltzmannSpeedPdf(vp, T, DISPLAY_CALIBRATION);
  const pdfAtFar = maxwellBoltzmannSpeedPdf(4 * vrms, T, DISPLAY_CALIBRATION);

  assert.equal(pdfAtZero, 0);
  assert.ok(pdfAtVp > 0);
  assert.ok(pdfAtVp > pdfAtFar);
});

test('Velocity sampling convergence with deterministic PRNG', () => {
  const T = 300;
  const rng = createSeededRandom(42);
  const N = 10000;
  let sumV2 = 0;
  let sumVx = 0;

  for (let i = 0; i < N; i++) {
    const v = sampleMaxwellVelocity(T, DISPLAY_CALIBRATION, rng);
    sumVx += v.x;
    const speed = lengthVector3D(v);
    sumV2 += speed * speed;
  }

  const sampleVrms = Math.sqrt(sumV2 / N);
  const theoreticalVrms = calculateRmsSpeed(T, DISPLAY_CALIBRATION);

  // Mean drift velocity along x should be close to 0 (isotropic)
  const meanVx = sumVx / N;
  assert.ok(Math.abs(meanVx) < 0.05, `Expected mean vx near 0, got ${meanVx}`);

  // Sample v_rms should match theoretical v_rms within 1.5%
  const relError = Math.abs(sampleVrms - theoreticalVrms) / theoreticalVrms;
  assert.ok(relError < 0.015, `v_rms error ${relError * 100}% exceeds 1.5%`);
});

test('Temperature scaling factor preserves relation', () => {
  const T1 = 300;
  const T2 = 373.15;
  const factor = calculateTemperatureScaling(T1, T2);
  const expectedFactor = Math.sqrt(373.15 / 300);
  assert.ok(Math.abs(factor - expectedFactor) < 1e-6);
});
