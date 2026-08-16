import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';

import { PNG } from 'pngjs';

import {
  NumberOCRSensor,
  TesseractJsRecognizer,
  type RgbaImage,
  type RuntimeFramePacket,
} from '../src/index.js';

const SAMPLE_ROOT = path.resolve(process.cwd(), '..', '..', 'examples', 'web-number-ocr', 'sample');
const MANIFEST = JSON.parse(readFileSync(path.join(SAMPLE_ROOT, 'manifest.json'), 'utf8')) as {
  roi: { x: number; y: number; width: number; height: number };
  cases: Array<{ id: string; file: string; expectedValue: number | null; expectedOutcome: string }>;
};

function pixels(filename: string): RgbaImage {
  const png = PNG.sync.read(readFileSync(path.join(SAMPLE_ROOT, filename)));
  return { width: png.width, height: png.height, data: new Uint8ClampedArray(png.data) };
}

function frame(caseId: string, image: RgbaImage, sequence: number): RuntimeFramePacket {
  return {
    frameId: `50000000-0000-4000-8000-${String(sequence).padStart(12, '0')}`,
    runId: 'tesseract-pixel-integration',
    sequence,
    observedAt: `2026-08-16T11:00:${String(sequence).padStart(2, '0')}.000Z`,
    monotonicNs: 3_000_000_000 + sequence,
    sourceSensorId: 'screen.capture',
    media: {
      kind: 'screen-frame',
      width: image.width,
      height: image.height,
      mediaType: 'image/png',
      colorSpace: 'RGBA',
    },
    artifactUri: `file://synthetic/number-ocr/${caseId}.png`,
    pixels: image,
  };
}

async function sensor(recognizer: TesseractJsRecognizer): Promise<NumberOCRSensor> {
  const instance = new NumberOCRSensor(recognizer);
  instance.configure({ roiId: 'display-value', roi: MANIFEST.roi, unit: '1' });
  await instance.start({ runId: 'tesseract-pixel-integration' });
  return instance;
}

test('Tesseract.js recognizes three synthetic numeric pixel frames and reports blank parse failure', async () => {
  const recognizer = new TesseractJsRecognizer({
    psmMode: 'SINGLE_WORD',
    whitelist: '0123456789.+-',
    workerOptions: { cachePath: path.join(os.tmpdir(), 'physics-software-sensors-tesseract-cache') },
  });
  const instance = await sensor(recognizer);
  try {
    const cases = MANIFEST.cases.filter((item) => ['positive', 'negative', 'zero', 'blank'].includes(item.id));
    for (const [sequence, item] of cases.entries()) {
      const event = await instance.processFrame(frame(item.id, pixels(item.file), sequence));
      if (item.expectedOutcome === 'success') {
        assert.equal(event.status, 'ok', item.id);
        const measurements = event.measurements as Array<Record<string, unknown>>;
        assert.equal(measurements[0]?.value, item.expectedValue, item.id);
      } else {
        assert.equal(event.status, 'error', item.id);
        assert.deepEqual(event.measurements, [], item.id);
        assert.equal((event.error as Record<string, unknown>).code, 'OCR_PARSE_FAILED', item.id);
      }
      assert.ok(recognizer.lastArtifacts(), `${item.id} must retain ROI/preprocessed artifacts`);
    }
  } finally {
    await instance.stop();
  }
});

test('Tesseract.js encoder failure becomes an explicit OCR failure event', async () => {
  const item = MANIFEST.cases.find((candidate) => candidate.id === 'engine-failure');
  assert.ok(item);
  const recognizer = new TesseractJsRecognizer({
    imageEncoder: async () => {
      throw new Error('intentional integration-test encoder failure');
    },
  });
  const instance = await sensor(recognizer);
  const event = await instance.processFrame(frame(item.id, pixels(item.file), 20));
  await instance.stop();
  assert.equal(event.status, 'error');
  assert.deepEqual(event.measurements, []);
  assert.equal((event.error as Record<string, unknown>).code, 'OCR_RECOGNITION_FAILED');
});
