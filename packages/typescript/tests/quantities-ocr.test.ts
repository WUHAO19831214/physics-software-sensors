import assert from 'node:assert/strict';
import test from 'node:test';

import {
  extractQuantities,
  normalizeQuantityText,
  GAS_LAB_QUANTITY_SPECS,
  type QuantitySpec,
} from '../src/index.js';

test('quantities OCR: text normalization preserves unit symbols', () => {
  const normalized = normalizeQuantityText('P: 1O3.2 kPa, T: 298.9 K');
  assert.match(normalized, /103\.2\s*kPa/i);
  assert.match(normalized, /298\.9\s*K/i);
});

test('quantities OCR: extracts pressure and temperature with unit anchoring', () => {
  const specs: QuantitySpec[] = [GAS_LAB_QUANTITY_SPECS.pressure, GAS_LAB_QUANTITY_SPECS.temperature];

  const text1 = '当前压强: 103.2 kPa 当前温度: 293.8 K';
  const res1 = extractQuantities(text1, specs);
  assert.equal(res1.quantities.pressure?.value, 103.2);
  assert.equal(res1.quantities.pressure?.unit, 'kPa');
  assert.equal(res1.quantities.temperature?.value, 293.8);
  assert.equal(res1.quantities.temperature?.unit, 'K');

  const text2 = '105.0 kPa S188: 298.9 K R=,';
  const res2 = extractQuantities(text2, specs);
  assert.equal(res2.quantities.pressure?.value, 105.0);
  assert.equal(res2.quantities.pressure?.unit, 'kPa');
  assert.equal(res2.quantities.temperature?.value, 298.9);
  assert.equal(res2.quantities.temperature?.unit, 'K');
});

test('quantities OCR: converts Pa to kPa when configured', () => {
  const specs: QuantitySpec[] = [GAS_LAB_QUANTITY_SPECS.pressure];
  const res = extractQuantities('Atmospheric pressure: 101325 Pa', specs);
  assert.equal(res.quantities.pressure?.value, 101.33);
});

test('quantities OCR: extracts Celsius degrees properly', () => {
  const specs: QuantitySpec[] = [GAS_LAB_QUANTITY_SPECS.temperature];
  const res = extractQuantities('环境温度: 24.5 ℃ 湿度: 50%', specs);
  assert.equal(res.quantities.temperature?.value, 24.5);
  assert.equal(res.quantities.temperature?.unit, '℃');
});

test('quantities OCR: rejects out-of-range false alarms', () => {
  const specs: QuantitySpec[] = [GAS_LAB_QUANTITY_SPECS.pressure];
  // 12.0 kPa is outside standard 50~300 kPa gas experiment range
  const res = extractQuantities('Residual: 12.0 kPa', specs);
  assert.equal(res.quantities.pressure, undefined);
});

test('quantity candidates preserve negative signs, source units and converted units', () => {
  const cold = extractQuantities('温度: −20 ℃', [GAS_LAB_QUANTITY_SPECS.temperature]);
  assert.equal(cold.quantities.temperature?.value, -20);
  assert.equal(cold.quantities.temperature?.unit, '℃');
  const pressure = extractQuantities('101325 PA', [GAS_LAB_QUANTITY_SPECS.pressure]);
  assert.equal(pressure.quantities.pressure?.value, 101.33);
  assert.equal(pressure.quantities.pressure?.unit, 'kPa');
  assert.equal(pressure.quantities.pressure?.sourceUnit, 'PA');
});

test('mixed instrument text never promotes another quantity, noise or rejected units', () => {
  const specs = Object.values(GAS_LAB_QUANTITY_SPECS);
  assert.equal(extractQuantities('293.8 K', specs).quantities.pressure, undefined);
  assert.equal(extractQuantities('S188 serial number', specs).quantities.pressure, undefined);
  assert.equal(extractQuantities('温度: 900 K', specs).quantities.temperature, undefined);
  assert.equal(extractQuantities('压强: 101325 unknownUnit', specs).quantities.pressure, undefined);
  assert.equal(extractQuantities('temperature missing; pressure 101.3 kPa', specs).quantities.temperature, undefined);
});

test('unitless numeric ROI requires explicit opt in and claims spans, not numeric values', () => {
  assert.deepEqual(extractQuantities('100 100', Object.values(GAS_LAB_QUANTITY_SPECS)).quantities, {});
  const result = extractQuantities('100 100', [
    { ...GAS_LAB_QUANTITY_SPECS.pressure, allowUnitless: true },
    { ...GAS_LAB_QUANTITY_SPECS.temperature, allowUnitless: true },
  ]);
  assert.equal(result.quantities.pressure?.value, 100);
  assert.equal(result.quantities.temperature?.value, 100);
  assert.equal(result.quantities.temperature?.unit, null);
});

test('absolute Kelvin bounds do not admit negative Celsius-like values', () => {
  assert.equal(extractQuantities('-20 K', [GAS_LAB_QUANTITY_SPECS.temperature]).quantities.temperature, undefined);
  assert.equal(extractQuantities('温度: -20', [GAS_LAB_QUANTITY_SPECS.temperature]).quantities.temperature, undefined);
  assert.equal(extractQuantities('-20 ℃', [GAS_LAB_QUANTITY_SPECS.temperature]).quantities.temperature?.value, -20);
});
