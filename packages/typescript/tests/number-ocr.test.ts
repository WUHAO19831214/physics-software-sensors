import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import test from 'node:test';

import {
  NumberOCRSensor,
  RecordedNumberRecognizer,
  extractNumberFromText,
  normalizeOcrText,
  type RecordedRecognition,
  type RuntimeFramePacket,
} from '../src/index.js';

interface Fixture {
  roi: { x: number; y: number; width: number; height: number };
  parserCases: Array<{ rawText: string; normalizedText: string; sourceValue: number | null }>;
  records: RecordedRecognition[];
}

const fixturePath = path.join(process.cwd(), 'tests', 'fixtures', 'ocr-number', 'recorded-results.json');
const fixture = JSON.parse(readFileSync(fixturePath, 'utf8')) as Fixture;

function frame(frameId: string): RuntimeFramePacket {
  return {
    frameId,
    runId: 'ocr-replay-001',
    sequence: 0,
    observedAt: '2026-08-16T08:00:00.000Z',
    monotonicNs: 1_000_000,
    sourceTimestamp: 1,
    sourceSensorId: 'screen.capture',
    media: {
      kind: 'screen-frame',
      width: 1920,
      height: 1080,
      mediaType: 'image/png',
      colorSpace: 'RGBA',
    },
    artifactUri: `fixture://ocr/${frameId}.png`,
  };
}

async function runningSensor(): Promise<NumberOCRSensor> {
  const sensor = new NumberOCRSensor(new RecordedNumberRecognizer(fixture.records));
  const configured = sensor.configure({
    roiId: 'force-y',
    roi: fixture.roi,
    name: 'Fy',
    symbol: 'Fy',
    unit: 'N',
  });
  assert.equal(configured.accepted, true);
  assert.match(configured.warnings[0] ?? '', /recorded-result replay/);
  await sensor.start({ runId: 'ocr-replay-001' });
  return sensor;
}

test('parser matches source-recorded behavior', () => {
  for (const item of fixture.parserCases) {
    assert.equal(normalizeOcrText(item.rawText), item.normalizedText);
    assert.equal(extractNumberFromText(item.rawText), item.sourceValue);
  }
});

test('recorded replay preserves OCR metadata and emits a measurement', async () => {
  const sensor = await runningSensor();
  const event = await sensor.processFrame(frame(fixture.records[0]!.frameId));
  const measurements = event.measurements as Array<Record<string, unknown>>;
  const payload = event.payload as Record<string, unknown>;
  assert.equal(event.status, 'ok');
  assert.equal(measurements[0]!.value, -2.33);
  assert.equal(measurements[0]!.role, 'derived');
  assert.equal(payload.raw_text, '-2.33');
  assert.equal(payload.confidence, 0.94);
  assert.equal(payload.duration_ms, 42);
  assert.deepEqual((event.quality as Record<string, unknown>).flags, ['recorded-replay']);
});

test('warning produces degraded status without discarding the value', async () => {
  const sensor = await runningSensor();
  const event = await sensor.processFrame(frame(fixture.records[1]!.frameId));
  const measurements = event.measurements as Array<Record<string, unknown>>;
  assert.equal(event.status, 'degraded');
  assert.equal(measurements[0]!.value, 0.5);
  assert.match(String((event.payload as Record<string, unknown>).warning), /low contrast/);
});

test('parse failure emits no mock or stale measurement', async () => {
  const sensor = await runningSensor();
  const event = await sensor.processFrame(frame(fixture.records[2]!.frameId));
  assert.equal(event.status, 'error');
  assert.deepEqual(event.measurements, []);
  assert.equal((event.error as Record<string, unknown>).code, 'OCR_PARSE_FAILED');
});

test('recognizer failure remains an explicit error with no value', async () => {
  const sensor = await runningSensor();
  const event = await sensor.processFrame(frame(fixture.records[3]!.frameId));
  assert.equal(event.status, 'error');
  assert.deepEqual(event.measurements, []);
  assert.equal((event.error as Record<string, unknown>).code, 'OCR_RECOGNITION_FAILED');
  assert.equal(sensor.health().errorCount, 1);
});

test('missing recorded result cannot invent a number', async () => {
  const sensor = await runningSensor();
  const event = await sensor.processFrame(frame('10000000-0000-4000-8000-999999999999'));
  assert.equal(event.status, 'error');
  assert.deepEqual(event.measurements, []);
  assert.equal((event.error as Record<string, unknown>).code, 'OCR_RECOGNITION_FAILED');
});

test('invalid normalized ROI is rejected before start', () => {
  const sensor = new NumberOCRSensor(new RecordedNumberRecognizer(fixture.records));
  assert.throws(
    () => sensor.configure({ roiId: 'bad', roi: { x: 0.9, y: 0.1, width: 0.2, height: 0.2 } }),
    /normalized ROI/,
  );
});
