import assert from 'node:assert/strict';
import test from 'node:test';

import {
  BrowserScreenBackend,
  type BrowserScreenDriver,
  NumberOCRSensor,
  RecordedNumberRecognizer,
  RecordedScreenBackend,
  ScreenCaptureError,
  ScreenCaptureSource,
  serializeRuntimeFramePacket,
  type CapturedScreenFrame,
  type ScreenBackendInfo,
} from '../src/index.js';

function rgba(value = 0) {
  return { width: 2, height: 1, data: new Uint8ClampedArray([value, value, value, 255, 0, 0, 0, 255]) };
}

function recordedFrames(): CapturedScreenFrame[] {
  return [
    {
      pixels: rgba(20),
      observedAt: '2026-08-16T12:00:00.000Z',
      monotonicNs: 1_000_000_000,
      sourceTimestamp: 10,
      artifactUri: 'recorded://screen/0',
      qualityFlags: ['synthetic-fixture'],
    },
    {
      pixels: rgba(40),
      observedAt: '2026-08-16T12:00:00.250Z',
      monotonicNs: 1_250_000_000,
      sourceTimestamp: 10.25,
      artifactUri: 'recorded://screen/1',
      droppedSinceLast: 1,
    },
  ];
}

function deterministicClocks() {
  let id = 1;
  return {
    observedAt: () => '2026-08-16T12:00:00.000Z',
    monotonicNs: () => 1,
    frameId: () => `82000000-0000-4000-8000-${String(id++).padStart(12, '0')}`,
  };
}

test('recorded screen replay emits serializable FramePackets with distinct requested/measured timing', async () => {
  const source = new ScreenCaptureSource(new RecordedScreenBackend(recordedFrames()), 'screen-test', deterministicClocks());
  source.configure({ requestedIntervalMs: 100 });
  await source.start({ runId: 'screen-replay' });
  const frames = [];
  for await (const frame of source.read()) frames.push(frame);
  await source.stop();

  assert.equal(frames.length, 2);
  assert.equal(frames[0]?.sourceSensorId, 'screen.capture');
  assert.equal(frames[0]?.pixels?.data[0], 20);
  const capture = frames[1]?.payload?.capture as Record<string, unknown>;
  assert.deepEqual(capture.requested, { sampling_interval_ms: 100 });
  assert.deepEqual(capture.actual, {
    measured_interval_ms: 250,
    measured_rate_hz: 4,
    width: 2,
    height: 1,
  });
  assert.deepEqual(frames[1]?.qualityFlags, ['recorded-replay', 'frame-dropped']);
  assert.equal(source.health().droppedCount, 1);

  const serialized = serializeRuntimeFramePacket(frames[0]!);
  assert.equal(serialized.schema_version, '1.0.0');
  assert.equal((serialized.media as Record<string, unknown>).orientation, '0');
  assert.match(String((serialized.artifact as Record<string, unknown>).sha256), /^[a-f0-9]{64}$/);
  assert.equal('pixels' in serialized, false);
});

test('browser permission is requested only when start is called', async () => {
  let requests = 0;
  let stops = 0;
  const driver: BrowserScreenDriver = {
    async request(): Promise<ScreenBackendInfo> {
      requests += 1;
      return {
        backend: 'fake-browser',
        user_authorized: true,
        deterministic_replay: false,
        display_surface: 'window',
      };
    },
    async read() { return { pixels: rgba(1) }; },
    async stop() { stops += 1; },
  };
  const source = new ScreenCaptureSource(new BrowserScreenBackend(driver), 'browser-test', deterministicClocks());
  source.configure({ requestedIntervalMs: 100 });
  assert.equal(requests, 0);
  await source.start({ runId: 'browser-screen' });
  assert.equal(requests, 1);
  const frame = await source.readOne();
  assert.equal((frame?.payload?.capture as Record<string, unknown>).user_authorized, true);
  await source.stop();
  assert.equal(stops, 1);
});

test('browser permission denial remains an explicit capture error', async () => {
  const driver: BrowserScreenDriver = {
    async request(): Promise<ScreenBackendInfo> {
      throw new ScreenCaptureError('SCREEN_CAPTURE_PERMISSION_DENIED', 'user denied the chooser');
    },
    async read() { return null; },
    async stop() {},
  };
  const source = new ScreenCaptureSource(new BrowserScreenBackend(driver));
  await assert.rejects(() => source.start({ runId: 'denied' }), (error: unknown) => {
    assert.equal((error as ScreenCaptureError).code, 'SCREEN_CAPTURE_PERMISSION_DENIED');
    return true;
  });
  assert.equal(source.health().state, 'error');
  assert.equal(source.health().errorCount, 1);
});

test('recorded screen FramePacket composes directly into NumberOCRSensor', async () => {
  const source = new ScreenCaptureSource(new RecordedScreenBackend(recordedFrames().slice(0, 1)), 'composition', deterministicClocks());
  source.configure({ requestedIntervalMs: 500 });
  await source.start({ runId: 'screen-to-ocr' });
  const frame = await source.readOne();
  assert.ok(frame);

  const recognizer = new RecordedNumberRecognizer([
    {
      frameId: frame.frameId,
      roiId: 'display',
      result: { method: 'recorded-source-result', rawText: '-2.33', confidence: 0.98, durationMs: 4 },
    },
  ]);
  const ocr = new NumberOCRSensor(recognizer);
  ocr.configure({ roiId: 'display', roi: { x: 0, y: 0, width: 1, height: 1 }, name: 'display', unit: 'N' });
  await ocr.start({ runId: 'screen-to-ocr' });
  const event = await ocr.processFrame(frame);
  await ocr.stop();
  await source.stop();

  assert.equal(event.status, 'ok');
  assert.equal((event.measurements as Array<Record<string, unknown>>)[0]?.value, -2.33);
  assert.deepEqual(event.parent_event_ids, [frame.frameId]);
});
