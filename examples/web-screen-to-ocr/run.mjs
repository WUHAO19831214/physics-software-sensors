/** Real-pixel composition: ScreenCaptureSource -> NumberOCRSensor. */

import { createRequire } from 'node:module';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import {
  NumberOCRSensor,
  RecordedScreenBackend,
  ScreenCaptureSource,
  TesseractJsRecognizer,
  serializeRuntimeFramePacket,
} from '../../packages/typescript/dist/src/index.js';

const here = path.dirname(fileURLToPath(import.meta.url));
const requireFromPackage = createRequire(path.join(here, '../../packages/typescript/package.json'));
const { PNG } = requireFromPackage('pngjs');
const sourcePath = path.join(here, '..', 'web-screen-capture', 'sample', 'recorded-screen.png');
const png = PNG.sync.read(await readFile(sourcePath));
const pixels = { width: png.width, height: png.height, data: new Uint8ClampedArray(png.data) };
const screen = new ScreenCaptureSource(new RecordedScreenBackend([{
  pixels,
  observedAt: '2026-08-16T14:00:00.000Z',
  monotonicNs: 6_000_000_000,
  artifactUri: 'recorded://screen-to-ocr/recorded-screen.png',
  qualityFlags: ['synthetic-fixture'],
}]), 'screen-to-ocr-source');
screen.configure({ requestedIntervalMs: 500 });
await screen.start({ runId: 'screen-to-ocr-demo' });
const frame = await screen.readOne();
if (!frame) throw new Error('screen source emitted no frame');

const recognizer = new TesseractJsRecognizer({
  psmMode: 'SINGLE_WORD',
  whitelist: '0123456789.+-',
  workerOptions: { cachePath: path.join(os.tmpdir(), 'physics-software-sensors-tesseract-cache') },
});
const ocr = new NumberOCRSensor(recognizer, 'screen-to-ocr-processor');
ocr.configure({ roiId: 'display', roi: { x: 0.3, y: 0.38, width: 0.4, height: 0.34 }, name: 'display value', unit: '1' });
await ocr.start({ runId: 'screen-to-ocr-demo' });
const event = await ocr.processFrame(frame);
await ocr.stop();
await screen.stop();
const output = path.join(here, 'output');
await mkdir(output, { recursive: true });
await writeFile(path.join(output, 'frame-packet.json'), `${JSON.stringify(serializeRuntimeFramePacket(frame), null, 2)}\n`);
await writeFile(path.join(output, 'sensor-event.json'), `${JSON.stringify(event, null, 2)}\n`);
console.log(`ScreenCaptureSource -> NumberOCRSensor: status=${event.status}, raw=${JSON.stringify(event.payload.raw_text)}, value=${event.measurements[0]?.value ?? 'none'}`);
