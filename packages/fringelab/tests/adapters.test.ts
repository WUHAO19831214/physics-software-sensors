import assert from 'node:assert/strict';
import test from 'node:test';
import type { RuntimeFramePacket, ProcessorSensor, SourceSensor } from '@physics-software-sensors/core';
import { StripProfileSensor, RulerTicksSensor } from '../src/sensors/index.js';
import { confirmMultiPointCalibration, confirmTwoPointCalibration, calibratedPosition, MeasurementSession } from '../src/core/calibration.js';
import { createImageViewport } from '../src/core/viewport.js';
import { BrowserCameraSource, type CameraBackend } from '../src/browser/camera-source.js';
import { RulerDetectionRunner } from '../src/browser/ruler-runner.js';
import { syntheticRuler } from './fixtures/scenes.js';
import { writeFileSync } from 'node:fs';

export function frame(width = 24, height = 12): RuntimeFramePacket {
  return { frameId: 'f1', runId: 'test', sequence: 0, observedAt: '2026-10-04T12:00:00.000Z', monotonicNs: 1000000, sourceSensorId: 'screen.capture', media: { kind: 'image-frame', width, height, mediaType: 'image/raw-rgba', colorSpace: 'RGBA' }, artifactUri: 'memory://fixture', pixels: { width, height, data: new Uint8ClampedArray(width * height * 4).fill(255) } };
}
const events: object[] = [];
test('processor adapters satisfy shared lifecycle and preserve frame timing; errors never produce measurements', async () => {
  const sensor: ProcessorSensor = new StripProfileSensor();
  assert.equal(sensor.configure({ channel: 'invalid' }).accepted, false);
  assert.equal(sensor.configure({ roi: { centerX: 0, centerY: 0, width: -1, height: 1 } }).accepted, false);
  assert.equal(sensor.configure({ fringeOrientation: 'diagonal' }).accepted, false);
  assert.equal(sensor.configure({ minAutoContrast: -1 }).accepted, false);
  assert.equal(sensor.configure({ channel: 'r' }).accepted, true);
  await sensor.start({ runId: 'test' });
  const input = frame();
  for await (const event of sensor.process(input)) { events.push(event); assert.equal((event.time as any).observed_at, input.observedAt); assert.equal(event.status, 'degraded'); assert.equal((event.payload as any).input_frame_id, input.frameId); }
  for await (const event of sensor.process({ ...input, pixels: undefined })) { events.push(event); assert.equal(event.status, 'error'); assert.deepEqual(event.measurements, []); }
  assert.equal(sensor.health().errorCount, 1);
  await sensor.stop();
  await assert.rejects(async () => { for await (const _ of sensor.process(input)) {} });
});
test('no-sample profile is lost and automatic ruler remains an unconfirmed candidate', async () => {
  const sensor = new StripProfileSensor(); sensor.configure({ roi: { centerX: -500, centerY: -500, width: 12, height: 6 } }); await sensor.start({ runId: 'test' });
  for await (const event of sensor.process(frame())) { events.push(event); assert.equal(event.status, 'lost'); assert.deepEqual(event.measurements, []); }
  const ruler = new RulerTicksSensor(); await ruler.start({ runId: 'test' });
  const scene = syntheticRuler({ body: [235,235,230], ink: [18,18,18] });
  for await (const event of ruler.process({ ...frame(scene.width, scene.height), pixels: { ...scene, data: new Uint8ClampedArray(Array.from(scene.data)) } })) { events.push(event); assert.equal(event.status, 'degraded'); assert.equal((event.payload as any).calibration_applied, false); }
  for await (const event of ruler.process(frame())) { events.push(event); assert.equal(event.status, 'lost'); }
});
test('confirmed calibration detects extrapolation and all source changes invalidate manual and multi-point state', () => {
  const session = new MeasurementSession('photo-a');
  const two = confirmTwoPointCalibration({ start: { x: 0, y: 0 }, end: { x: 100, y: 0 }, knownLengthMm: 10 }, 'photo-a', 'c1');
  assert.throws(() => confirmTwoPointCalibration({ ...two.ruler!, originMm: Infinity }, 'photo-a', 'bad'));
  session.apply(two); assert.equal(calibratedPosition({ x: 50, y: 50 }, session.calibration, session.sourceKey).valueMm, 5);
  assert.equal(calibratedPosition({ x: 120, y: 0 }, session.calibration, session.sourceKey).extrapolated, true);
  const key = session.calculationKey; session.invalidateProcessing(); assert.equal(session.isCurrent(key), false);
  session.changeSource('photo-b'); assert.equal(session.calibration, null); assert.equal(calibratedPosition({ x: 20, y: 0 }, two, session.sourceKey).status, 'stale');
  assert.throws(() => confirmMultiPointCalibration([{ x: 0, y: 0, mm: 0 }, { x: 20, y: 0, mm: 0 }, { x: 40, y: 0, mm: 1 }], 'x', 'c'));
  const multi = confirmMultiPointCalibration([{ x: 0, y: 0, mm: 0 }, { x: 100, y: 0, mm: 10 }, { x: 220, y: 0, mm: 20 }], 'photo-b', 'c2'); session.apply(multi);
  assert.equal(calibratedPosition({ x: 160, y: 0 }, session.calibration, 'photo-b').valueMm, 15);
});
test('contain mapping preserves original coordinates despite letterboxing', () => {
  const transform = createImageViewport({ width: 4032, height: 3024 }, { width: 960, height: 540 });
  const p = { x: 2048, y: 1000 }; const restored = transform.toImage(transform.toDisplay(p));
  assert.ok(Math.hypot(restored.x - p.x, restored.y - p.y) < 1e-9); assert.equal(transform.offset.x, 120);
});
test('camera backend lifecycle reports requested sampling separately and releases on abort', async () => {
  let stopped = 0, captures = 0;
  const backend: CameraBackend = { async start() { return { label: 'controlled-test-backend', capabilities: {}, settings: { frameRate: 30 } }; }, async capture() { captures++; return { pixels: frame().pixels!, sourceTimestamp: captures / 30 }; }, async stop() { stopped++; } };
  const source: SourceSensor = new BrowserCameraSource(backend); source.configure({ intervalMs: 16 }); const controller = new AbortController(); await source.start({ runId: 'test', cancellation: controller.signal });
  for await (const packet of source.read()) { assert.equal(packet.runId, 'test'); assert.equal((packet as RuntimeFramePacket).payload?.requested_interval_ms, 16); assert.ok(packet.pixels); controller.abort(); }
  assert.ok(stopped > 0); assert.equal(source.health().state, 'stopped');
});
test('cancelled ruler runner rejects obsolete work without detaching input', async () => {
  const runner = new RulerDetectionRunner(false); const image = frame().pixels!;
  const pending = runner.detect(image, { sourceType: 'image' }); runner.cancel(); await assert.rejects(pending, { name: 'AbortError' }); assert.ok(image.data.byteLength > 0);
});
test.after(() => { if (process.env.FRINGELAB_EVENTS_OUT) writeFileSync(process.env.FRINGELAB_EVENTS_OUT, JSON.stringify(events, null, 2) + '\n'); });
