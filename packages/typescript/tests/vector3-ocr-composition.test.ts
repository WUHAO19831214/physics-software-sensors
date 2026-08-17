import assert from 'node:assert/strict';
import test from 'node:test';

import {
  NumberOCRSensor,
  RecordedNumberRecognizer,
  Vector3Assembler,
  componentFromNumberOcrEvent,
  type RecordedRecognition,
  type RuntimeFramePacket,
} from '../src/index.js';

const records: RecordedRecognition[] = [
  { frameId: 'yanan-frame', roiId: 'Fy', result: { method: 'recorded', rawText: '-2.33', confidence: 0.94, durationMs: 42 } },
  { frameId: 'yanan-frame', roiId: 'Fz', result: { method: 'recorded', rawText: '0.50', confidence: 0.91, durationMs: 39 } },
  { frameId: 'bad-frame', roiId: 'Fz', result: { method: 'recorded', rawText: '--', confidence: 0.1, durationMs: 41 } },
];

function frame(frameId: string): RuntimeFramePacket {
  return {
    frameId, runId: 'yanan-replay', sequence: 1, observedAt: '2026-06-04T12:54:03.000Z',
    monotonicNs: 1_000_000, sourceTimestamp: 1000, sourceSensorId: 'screen.capture',
    media: { kind: 'screen-frame', width: 1920, height: 1080, mediaType: 'image/png', colorSpace: 'RGBA' },
    artifactUri: `fixture://yanan/${frameId}.png`,
  };
}

async function ocr(roiId: 'Fy' | 'Fz', frameId = 'yanan-frame') {
  const sensor = new NumberOCRSensor(new RecordedNumberRecognizer(records), `ocr-${roiId}`);
  sensor.configure({ roiId, roi: { x: 0, y: 0, width: 0.5, height: 0.5 }, name: roiId, symbol: roiId, unit: 'N' });
  await sensor.start({ runId: 'yanan-replay' });
  return sensor.processFrame(frame(frameId));
}

test('recorded Fy/Fz OCR composes with explicit constrained Fx=0', async () => {
  const [fyEvent, fzEvent] = await Promise.all([ocr('Fy'), ocr('Fz')]);
  const result = new Vector3Assembler({ maxComponentSkewMs: 150 }).compose({
    quantity: 'force', unit: 'N', coordinateSystem: 'yanan-classroom-x-conductor-y-horizontal-z-up',
    components: {
      x: { value: 0, source: 'constrained', quality: { flags: ['yanan-apparatus-plane-constraint'] } },
      y: componentFromNumberOcrEvent(fyEvent),
      z: componentFromNumberOcrEvent(fzEvent),
    },
  });
  assert.deepEqual(result.measurement!.components, { x: 0, y: -2.33, z: 0.5 });
  assert.equal(result.measurement!.componentDetails.x.source, 'constrained');
  assert.equal(result.measurement!.componentDetails.y.source, 'observed');
  assert.equal(result.measurement!.componentDetails.y.quality!.confidence, 0.94);
  assert.equal(result.measurement!.magnitude, Math.hypot(0, -2.33, 0.5));
});

test('OCR parse failure becomes a missing component, never a mock number', async () => {
  const [fyEvent, failedFz] = await Promise.all([ocr('Fy'), ocr('Fz', 'bad-frame')]);
  const result = new Vector3Assembler().compose({
    quantity: 'force', unit: 'N', coordinateSystem: 'yanan-classroom',
    components: { x: { value: 0, source: 'constrained' }, y: componentFromNumberOcrEvent(fyEvent), z: componentFromNumberOcrEvent(failedFz) },
  });
  assert.equal(result.status, 'incomplete');
  assert.equal(result.measurement, null);
  assert.deepEqual(result.missingComponents, ['z']);
});
