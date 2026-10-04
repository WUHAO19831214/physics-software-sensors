import type { ImageDataLike } from "../../src/core/signal.js";
export function syntheticRuler(options: {
  body: [number, number, number];
  ink: [number, number, number];
  angleDeg?: number;
  perspective?: number;
  noise?: number;
  missing?: Set<number>;
}): ImageDataLike {
  const width = 720;
  const height = 280;
  const data = new Uint8ClampedArray(width * height * 4);
  const angle = (options.angleDeg ?? 0) * Math.PI / 180;
  const axis = { x: Math.cos(angle), y: Math.sin(angle) };
  const normal = { x: -axis.y, y: axis.x };
  const centre = { x: width / 2, y: height * 0.62 };
  const rulerLength = 620;
  const rulerHeight = 92;
  const pixelsPerMm = 10;
  let seed = 9173;
  const random = () => {
    seed = (seed * 1664525 + 1013904223) >>> 0;
    return seed / 0xffffffff;
  };
  for (let y = 0; y < height; y += 1) {
    for (let x = 0; x < width; x += 1) {
      const dx = x - centre.x;
      const dy = y - centre.y;
      const u = dx * axis.x + dy * axis.y;
      const v = dx * normal.x + dy * normal.y;
      let color: [number, number, number] = [18, 25, 32];
      if (Math.abs(u) <= rulerLength / 2 && Math.abs(v) <= rulerHeight / 2) {
        color = options.body;
        for (let millimetre = 0; millimetre <= 60; millimetre += 1) {
          if (options.missing?.has(millimetre)) continue;
          const base = -300 + millimetre * pixelsPerMm;
          const warped = base + (options.perspective ?? 0) * (base / 300) ** 2 * 12;
          const tickHeight = millimetre % 10 === 0 ? 45 : millimetre % 5 === 0 ? 31 : 20;
          if (Math.abs(u - warped) <= 1.45 && v >= -rulerHeight / 2 && v <= -rulerHeight / 2 + tickHeight) {
            color = options.ink;
          }
        }
      }
      const noise = ((random() - 0.5) * 2) * (options.noise ?? 0);
      const offset = (y * width + x) * 4;
      data[offset] = Math.max(0, Math.min(255, color[0] + noise));
      data[offset + 1] = Math.max(0, Math.min(255, color[1] + noise));
      data[offset + 2] = Math.max(0, Math.min(255, color[2] + noise));
      data[offset + 3] = 255;
    }
  }
  return { width, height, data };
}
