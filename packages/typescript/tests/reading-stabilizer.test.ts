import assert from 'node:assert/strict';
import test from 'node:test';

import { ReadingStabilizer } from '../src/index.js';

test('readingStabilizer: initializes and emits fresh valid values', () => {
  const stabilizer = new ReadingStabilizer<number>();
  const initial = stabilizer.getCurrent();
  assert.equal(initial.status, 'uninitialized');
  assert.equal(initial.value, null);

  const sample1 = stabilizer.update({ value: 101.3, confidence: 0.95, timestamp: 1000 });
  assert.equal(sample1.status, 'valid');
  assert.equal(sample1.value, 101.3);
  assert.equal(sample1.isFresh, true);
  assert.equal(sample1.confidence, 0.95);
});

test('readingStabilizer: holds previous reading with decaying confidence upon missing frame', () => {
  const stabilizer = new ReadingStabilizer<number>({
    maxHoldingDurationMs: 2000,
    confidenceDecayRate: 0.9,
    minHoldingConfidence: 0.2,
  });

  stabilizer.update({ value: 102.5, confidence: 0.9, timestamp: 1000 });

  // Missing frame (null reading) at t=1500ms
  const held = stabilizer.update({ value: null, timestamp: 1500 });
  assert.equal(held.status, 'holding');
  assert.equal(held.value, 102.5);
  assert.equal(held.isFresh, false);
  assert.ok(held.confidence < 0.9);
  assert.ok(held.flags.includes('value-holding'));
});

test('readingStabilizer: marks stale when holding exceeds duration', () => {
  const stabilizer = new ReadingStabilizer<number>({
    maxHoldingDurationMs: 1000,
  });

  stabilizer.update({ value: 105.0, confidence: 0.85, timestamp: 1000 });

  // 1500ms later (> maxHoldingDurationMs)
  const stale = stabilizer.update({ value: null, timestamp: 2500 });
  assert.equal(stale.status, 'stale');
  assert.equal(stale.confidence, 0);
  assert.ok(stale.flags.includes('timeout-stale'));
});

test('readingStabilizer: rejects anomalous sudden spikes', () => {
  const stabilizer = new ReadingStabilizer<number>({
    maxAllowedSpikeRatio: 0.5, // 50% max deviation
  });

  stabilizer.update({ value: 100.0, timestamp: 1000 });

  // Spurious reading jumping from 100 to 250 (150% jump)
  const spiked = stabilizer.update({ value: 250.0, timestamp: 1500 });
  assert.equal(spiked.status, 'holding');
  assert.equal(spiked.value, 100.0); // Held previous valid value
  assert.ok(spiked.flags.includes('spike-rejected'));
});

test('nonfinite values cannot become valid measurements', () => {
  const stabilizer = new ReadingStabilizer();
  assert.equal(stabilizer.update({ value: NaN, timestamp: 1 }).status, 'uninitialized');
  stabilizer.update({ value: 100, confidence: 0.1, timestamp: 2 });
  const held = stabilizer.update({ value: Infinity, timestamp: 3 });
  assert.equal(held.value, 100);
  assert.equal(held.status, 'holding');
  assert.ok(held.confidence <= 0.1);
  assert.throws(() => stabilizer.update({ value: 2, timestamp: NaN }), RangeError);
});

test('out-of-order updates do not replace readings and a stale stream can recover', () => {
  const stabilizer = new ReadingStabilizer({ maxHoldingDurationMs: 100, maxAllowedSpikeRatio: 0.2 });
  stabilizer.update({ value: 100, timestamp: 1000 });
  assert.equal(stabilizer.update({ value: 120, timestamp: 900 }).value, 100);
  assert.equal(stabilizer.update({ value: 300, timestamp: 1200 }).status, 'valid');
});
