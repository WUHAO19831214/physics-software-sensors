import type { Point, RoiGeometry } from './roi.js';

/** Explicit contain transform; all physical operations use original pixels. */
export function createImageViewport(source: { width: number; height: number }, display: { width: number; height: number }) {
  if (![source.width, source.height, display.width, display.height].every(v => Number.isFinite(v) && v > 0)) throw new RangeError('Positive dimensions required');
  const scale = Math.min(display.width / source.width, display.height / source.height);
  const offset = { x: (display.width - source.width * scale) / 2, y: (display.height - source.height * scale) / 2 };
  const toImage = (p: Point): Point => ({ x: (p.x - offset.x) / scale, y: (p.y - offset.y) / scale });
  const toDisplay = (p: Point): Point => ({ x: p.x * scale + offset.x, y: p.y * scale + offset.y });
  return { scale, offset, toImage, toDisplay, roiToImage: (r: RoiGeometry): RoiGeometry => ({ ...r, centerX: toImage({ x: r.centerX, y: r.centerY }).x, centerY: toImage({ x: r.centerX, y: r.centerY }).y, width: r.width / scale, height: r.height / scale }) };
}
