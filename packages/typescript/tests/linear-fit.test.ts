import assert from 'node:assert/strict';
import test from 'node:test';

import {
  calculateLinearFit,
  extrapolateX,
  calculateNiceStep,
} from '../src/index.js';

test('linearFit: ordinary least-squares regression matches ideal linear points', () => {
  const points = [
    { x: 1, y: 3 },
    { x: 2, y: 5 },
    { x: 3, y: 7 },
    { x: 4, y: 9 },
  ];
  const fit = calculateLinearFit(points);
  assert.equal(fit.valid, true);
  assert.ok(Math.abs(fit.slope - 2.0) < 1e-6);
  assert.ok(Math.abs(fit.intercept - 1.0) < 1e-6);
  assert.ok(Math.abs(fit.rSquared - 1.0) < 1e-6);
});

test('linearFit: Charles law dataset and absolute zero extrapolation', () => {
  // Gas pressure vs Celsius temperature: p = k*t + p0
  // p0 = 101.325 kPa at 0 ℃, k = 101.325 / 273.15 ≈ 0.37095 kPa/℃
  const celsiusData = [
    { x: 0.0, y: 101.325 },
    { x: 20.0, y: 108.744 },
    { x: 40.0, y: 116.163 },
    { x: 60.0, y: 123.582 },
    { x: 80.0, y: 131.001 },
  ];

  const fit = calculateLinearFit(celsiusData);
  assert.equal(fit.valid, true);
  assert.ok(fit.rSquared > 0.9999);

  // Extrapolate to target p = 0 to obtain Absolute Zero
  const t0 = extrapolateX(fit, 0);
  assert.ok(t0 !== null);
  assert.ok(Math.abs(t0 - (-273.15)) < 0.05, `Expected ~ -273.15, got ${t0}`);
});

test('linearFit: origin-constrained regression', () => {
  // p vs T (Kelvin): p = k0 * T
  const kelvinData = [
    { x: 273.15, y: 101.325 },
    { x: 293.15, y: 108.744 },
    { x: 313.15, y: 116.163 },
    { x: 333.15, y: 123.582 },
  ];

  const fit = calculateLinearFit(kelvinData);
  assert.equal(fit.valid, true);
  assert.ok(Math.abs(fit.originSlope - 0.37095) < 0.001);
  assert.ok(fit.originRSquared > 0.9999);
});

test('linearFit: handles empty or singular points gracefully', () => {
  const empty = calculateLinearFit([]);
  assert.equal(empty.valid, false);

  const single = calculateLinearFit([{ x: 10, y: 20 }]);
  assert.equal(single.valid, false);

  const verticalLine = calculateLinearFit([
    { x: 5, y: 1 },
    { x: 5, y: 2 },
  ]);
  assert.equal(verticalLine.valid, false);
});

test('calculateNiceStep: calculates clean scale increments', () => {
  assert.equal(calculateNiceStep(100, 5), 20);
  assert.equal(calculateNiceStep(25, 5), 5);
  assert.equal(calculateNiceStep(350, 7), 50);
  assert.equal(calculateNiceStep(1.2, 6), 0.2);
});
