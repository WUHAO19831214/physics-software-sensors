/** Run real Tesseract.js OCR on synthetic RGBA screen-frame fixtures. */

import { createRequire } from 'node:module';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import {
  NumberOCRSensor,
  TesseractJsRecognizer,
} from '../../packages/typescript/dist/src/index.js';

const here = path.dirname(fileURLToPath(import.meta.url));
const requireFromPackage = createRequire(path.join(here, '../../packages/typescript/package.json'));
const { PNG } = requireFromPackage('pngjs');
const sampleDir = path.join(here, 'sample');
const outputDir = path.join(here, 'output');
const manifest = JSON.parse(await readFile(path.join(sampleDir, 'manifest.json'), 'utf8'));

function decodePng(buffer) {
  const png = PNG.sync.read(buffer);
  return { width: png.width, height: png.height, data: new Uint8ClampedArray(png.data) };
}

async function writePng(filename, image) {
  const png = new PNG({ width: image.width, height: image.height });
  png.data = Buffer.from(image.data.buffer, image.data.byteOffset, image.data.byteLength);
  await writeFile(filename, PNG.sync.write(png));
}

function frame(caseId, pixels, sequence) {
  return {
    frameId: `40000000-0000-4000-8000-${String(sequence).padStart(12, '0')}`,
    runId: 'number-ocr-standalone-demo',
    sequence,
    observedAt: `2026-08-16T10:00:${String(sequence).padStart(2, '0')}.000Z`,
    monotonicNs: 2_000_000_000 + sequence * 1_000_000,
    sourceTimestamp: sequence,
    sourceSensorId: 'screen.capture',
    media: {
      kind: 'screen-frame',
      width: pixels.width,
      height: pixels.height,
      mediaType: 'image/png',
      colorSpace: 'RGBA',
    },
    artifactUri: `file://synthetic/number-ocr/${caseId}.png`,
    pixels,
  };
}

async function configuredSensor(recognizer) {
  const sensor = new NumberOCRSensor(recognizer, 'number-ocr-demo-01');
  sensor.configure({ roiId: 'display-value', roi: manifest.roi, name: 'display value', symbol: 'x', unit: '1' });
  await sensor.start({ runId: 'number-ocr-standalone-demo' });
  return sensor;
}

await mkdir(outputDir, { recursive: true });
const cachePath = path.join(os.tmpdir(), 'physics-software-sensors-tesseract-cache');
await mkdir(cachePath, { recursive: true });
const recognizer = new TesseractJsRecognizer({
  psmMode: 'SINGLE_WORD',
  preprocessMode: 'auto',
  whitelist: '0123456789.+-',
  workerOptions: { cachePath },
});
const sensor = await configuredSensor(recognizer);
const results = [];

for (const [sequence, item] of manifest.cases.filter((entry) => entry.id !== 'engine-failure').entries()) {
  const pixels = decodePng(await readFile(path.join(sampleDir, item.file)));
  const event = await sensor.processFrame(frame(item.id, pixels, sequence));
  const artifacts = recognizer.lastArtifacts();
  if (!artifacts) throw new Error(`missing OCR artifacts for ${item.id}`);
  await writePng(path.join(outputDir, `${item.id}-roi.png`), artifacts.roi);
  await writePng(path.join(outputDir, `${item.id}-preprocessed.png`), artifacts.preprocessed);
  results.push({ fixture: item, event, pixelRoi: artifacts.pixelRect });
  const value = event.measurements[0]?.value ?? 'none';
  console.log(`${item.id}: status=${event.status} raw=${JSON.stringify(event.payload.raw_text)} value=${value}`);
}
await sensor.stop();

const failing = manifest.cases.find((entry) => entry.id === 'engine-failure');
const failingPixels = decodePng(await readFile(path.join(sampleDir, failing.file)));
const failingRecognizer = new TesseractJsRecognizer({
  imageEncoder: async () => {
    throw new Error('intentional synthetic encoder failure');
  },
});
const failingSensor = await configuredSensor(failingRecognizer);
const failureEvent = await failingSensor.processFrame(frame(failing.id, failingPixels, manifest.cases.length - 1));
await failingSensor.stop();
results.push({ fixture: failing, event: failureEvent, pixelRoi: null });
console.log(`${failing.id}: status=${failureEvent.status} code=${failureEvent.error.code}`);

await writeFile(path.join(outputDir, 'results.json'), `${JSON.stringify(results, null, 2)}\n`);
console.log(`wrote ${results.length} results and pixel-stage PNGs to ${outputDir}`);
