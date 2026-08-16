/** Exact minimal extraction of app.js::trackRedSpot/rgbToHsv at the fixed commits. */

import { createRequire } from 'node:module';
import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const requireFromPackage = createRequire(path.join(root, 'packages/typescript/package.json'));
const { PNG } = requireFromPackage('pngjs');
const sample = path.join(root, 'examples/spot-centroid/sample');
const manifest = JSON.parse(await readFile(path.join(sample, 'manifest.json'), 'utf8'));

function rgbToHsv(r, g, b) {
  r /= 255; g /= 255; b /= 255;
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  const delta = max - min;
  let h = 0;
  if (delta !== 0) {
    if (max === r) h = 60 * (((g - b) / delta) % 6);
    if (max === g) h = 60 * ((b - r) / delta + 2);
    if (max === b) h = 60 * ((r - g) / delta + 4);
  }
  if (h < 0) h += 360;
  return { h, s: max === 0 ? 0 : delta / max, v: max };
}

function sourceTrack(image) {
  const { width, height, data } = image;
  const step = width > 1000 ? 2 : 1;
  let weightSum = 0, sumX = 0, sumY = 0;
  let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
  for (let y = 0; y < height; y += step) {
    for (let x = 0; x < width; x += step) {
      const index = (y * width + x) * 4;
      const r = data[index], g = data[index + 1], b = data[index + 2];
      const hsv = rgbToHsv(r, g, b);
      const hueIsRed = hsv.h <= 18 || hsv.h >= 340;
      const strongRed = r > 135 && r - g > 35 && r - b > 20;
      if (hueIsRed && hsv.s > 0.38 && hsv.v > 0.35 && strongRed) {
        const weight = (hsv.s * hsv.v * 255 + Math.max(0, r - Math.max(g, b))) / 2;
        weightSum += weight; sumX += x * weight; sumY += y * weight;
        minX = Math.min(minX, x); maxX = Math.max(maxX, x);
        minY = Math.min(minY, y); maxY = Math.max(maxY, y);
      }
    }
  }
  if (weightSum > 900) {
    return { locked: true, x: sumX / weightSum, y: sumY / weightSum, radius: Math.max(7, Math.hypot(maxX - minX, maxY - minY) / 2), weight_sum: weightSum };
  }
  return { locked: false, x: null, y: null, radius: null, weight_sum: weightSum };
}

const result = {
  generated_by: 'exact-source-js-harness',
  source_commits: ['7f0d91cc73afafaecc54acc46b2b9d69375d994a', 'c3f58175a09ff29cacdfb976a5055758c4eff619'],
  tolerance_px: 1e-9,
  cases: [],
};
for (const item of manifest.cases) {
  const png = PNG.sync.read(await readFile(path.join(sample, item.file)));
  result.cases.push({ id: item.id, file: item.file, source_result: sourceTrack(png) });
}
const target = process.argv[2] ?? path.join(root, 'tests/fixtures/spot_centroid/golden.json');
await writeFile(target, `${JSON.stringify(result, null, 2)}\n`);
console.log(`wrote ${result.cases.length} source-harness results to ${target}`);
