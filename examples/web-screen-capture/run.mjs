/** Deterministic ScreenCaptureSource replay producing a serializable FramePacket. */

import { createRequire } from 'node:module';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import {
  RecordedScreenBackend,
  ScreenCaptureSource,
  serializeRuntimeFramePacket,
} from '../../packages/typescript/dist/src/index.js';

const here = path.dirname(fileURLToPath(import.meta.url));
const requireFromPackage = createRequire(path.join(here, '../../packages/typescript/package.json'));
const { PNG } = requireFromPackage('pngjs');
const sample = path.join(here, 'sample', 'recorded-screen.png');
const output = path.join(here, 'output');
const png = PNG.sync.read(await readFile(sample));
const pixels = { width: png.width, height: png.height, data: new Uint8ClampedArray(png.data) };
let id = 1;
const source = new ScreenCaptureSource(
  new RecordedScreenBackend([
    {
      pixels,
      observedAt: '2026-08-16T13:30:00.000Z',
      monotonicNs: 5_000_000_000,
      sourceTimestamp: 12.5,
      artifactUri: 'recorded://screen-capture-demo/recorded-screen.png',
      qualityFlags: ['synthetic-fixture'],
      metadata: { source_kind: 'synthetic-recorded-screen' },
    },
  ]),
  'screen-demo-01',
  {
    observedAt: () => '2026-08-16T13:30:00.000Z',
    monotonicNs: () => 5_000_000_000,
    frameId: () => `83000000-0000-4000-8000-${String(id++).padStart(12, '0')}`,
  },
);
source.configure({ requestedIntervalMs: 500 });
await source.start({ runId: 'screen-capture-standalone-demo' });
const frame = await source.readOne();
if (!frame) throw new Error('recorded screen source emitted no frame');
await source.stop();
const packet = serializeRuntimeFramePacket(frame);
await mkdir(output, { recursive: true });
await writeFile(path.join(output, 'frame-packet.json'), `${JSON.stringify(packet, null, 2)}\n`);
console.log(`screen frame ${frame.frameId}: ${frame.media.width}x${frame.media.height}, sha256=${frame.artifactSha256}`);
