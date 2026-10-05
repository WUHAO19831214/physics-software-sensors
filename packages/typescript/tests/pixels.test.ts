import assert from 'node:assert/strict';
import test from 'node:test';

import {
  cropNormalizedRoi,
  preprocessForNumberRecognition,
  validateRgbaImage,
  type RgbaImage,
} from '../src/index.js';

function image(width: number, height: number): RgbaImage {
  const data = new Uint8ClampedArray(width * height * 4);
  for (let index = 0; index < data.length; index += 4) {
    const pixel = index / 4;
    data[index] = pixel;
    data[index + 1] = pixel;
    data[index + 2] = pixel;
    data[index + 3] = 255;
  }
  return { width, height, data };
}

test('normalized ROI crop copies the exact RGBA pixel rectangle', () => {
  const cropped = cropNormalizedRoi(image(4, 4), { x: 0.25, y: 0.25, width: 0.5, height: 0.5 });
  assert.deepEqual(cropped.rect, { x: 1, y: 1, width: 2, height: 2 });
  assert.deepEqual(
    [cropped.image.data[0], cropped.image.data[4], cropped.image.data[8], cropped.image.data[12]],
    [5, 6, 9, 10],
  );
});

test('number preprocessing scales pixels and emits binary RGB', () => {
  const input: RgbaImage = {
    width: 2,
    height: 1,
    data: new Uint8ClampedArray([0, 0, 0, 255, 255, 255, 255, 255]),
  };
  const processed = preprocessForNumberRecognition(input, { scale: 2, threshold: 150, removeNoise: false });
  assert.equal(processed.width, 4);
  assert.equal(processed.height, 2);
  assert.deepEqual(Array.from(processed.data.slice(0, 16)), [0, 0, 0, 255, 0, 0, 0, 255, 255, 255, 255, 255, 255, 255, 255, 255]);
});

test('invalid RGBA buffer length is rejected', () => {
  assert.throws(
    () => validateRgbaImage({ width: 2, height: 2, data: new Uint8ClampedArray(3) }),
    /data length/,
  );
});

test('adaptive OCR padding preserves source pixels and opaque border alpha', async () => {
  const { addRgbaPadding, resolveOptimalScale } = await import('../src/index.js');
  const input = { width: 1, height: 1, data: new Uint8ClampedArray([25, 50, 75, 255]) };
  const padded = addRgbaPadding(input, 1, 0);
  assert.deepEqual([...padded.data.slice(16, 20)], [25, 50, 75, 255]);
  assert.deepEqual([...padded.data.slice(0, 4)], [0, 0, 0, 255]);
  assert.equal(resolveOptimalScale(30), 4);
  assert.equal(resolveOptimalScale(60), 2);
  assert.throws(() => resolveOptimalScale(60, NaN), RangeError);
});
