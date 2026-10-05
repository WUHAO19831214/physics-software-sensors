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
