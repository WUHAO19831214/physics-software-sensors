/** Smoke test copied into a clean npm consumer after installing the package tgz. */

import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';

import { PNG } from 'pngjs';
import {
  NumberOCRSensor,
  RecordedScreenBackend,
  ScreenCaptureSource,
  TesseractJsRecognizer,
} from '@physics-software-sensors/core';

const samplePath = process.argv[2];
if (!samplePath) throw new Error('usage: node smoke.mjs /absolute/path/to/negative.png');
const png = PNG.sync.read(await readFile(samplePath));
const pixels = { width: png.width, height: png.height, data: new Uint8ClampedArray(png.data) };
const recognizer = new TesseractJsRecognizer({
  psmMode: 'SINGLE_WORD',
  whitelist: '0123456789.+-',
  workerOptions: { cachePath: path.join(os.tmpdir(), 'physics-software-sensors-tesseract-cache') },
});
const sensor = new NumberOCRSensor(recognizer);
sensor.configure({ roiId: 'display-value', roi: { x: 0.33, y: 0.39, width: 0.34, height: 0.31 }, unit: '1' });
await sensor.start({ runId: 'clean-tgz-smoke' });
const source = new ScreenCaptureSource(new RecordedScreenBackend([{
  pixels,
  observedAt: '2026-08-16T12:30:00.000Z',
  monotonicNs: 1,
  artifactUri: 'file://synthetic/number-ocr/negative.png',
}]));
await source.start({ runId: 'clean-tgz-smoke' });
const frame = await source.readOne();
assert.ok(frame);
const event = await sensor.processFrame(frame);
await source.stop();
await sensor.stop();
assert.equal(event.status, 'ok');
assert.equal(event.measurements[0].value, -2.33);
console.log('PASS clean tgz ScreenCaptureSource -> real-pixel TesseractJsRecognizer composition');
