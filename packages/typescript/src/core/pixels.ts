/** Runtime-only RGBA pixels kept outside the serializable FramePacket envelope. */

export interface RgbaImage {
  width: number;
  height: number;
  data: Uint8ClampedArray;
}

export interface NormalizedRect {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface PixelRect {
  x: number;
  y: number;
  width: number;
  height: number;
}

export function validateRgbaImage(image: RgbaImage): void {
  if (!Number.isInteger(image.width) || !Number.isInteger(image.height) || image.width < 1 || image.height < 1) {
    throw new Error('RGBA image width and height must be positive integers');
  }
  if (!(image.data instanceof Uint8ClampedArray)) throw new Error('RGBA image data must be Uint8ClampedArray');
  if (image.data.length !== image.width * image.height * 4) {
    throw new Error('RGBA image data length does not match width and height');
  }
}

export function validateNormalizedRect(roi: NormalizedRect): void {
  const values = [roi.x, roi.y, roi.width, roi.height];
  if (!values.every((value) => Number.isFinite(value))) throw new Error('ROI values must be finite');
  if (roi.width <= 0 || roi.height <= 0) throw new Error('ROI width and height must be positive');
  if (roi.x < 0 || roi.y < 0 || roi.x + roi.width > 1 || roi.y + roi.height > 1) {
    throw new Error('normalized ROI must stay within [0, 1]');
  }
}

export function normalizedRectToPixels(roi: NormalizedRect, width: number, height: number): PixelRect {
  validateNormalizedRect(roi);
  const x = Math.max(0, Math.round(roi.x * width));
  const y = Math.max(0, Math.round(roi.y * height));
  return {
    x,
    y,
    width: Math.max(1, Math.min(width - x, Math.round(roi.width * width))),
    height: Math.max(1, Math.min(height - y, Math.round(roi.height * height))),
  };
}

export function cropNormalizedRoi(image: RgbaImage, roi: NormalizedRect): { image: RgbaImage; rect: PixelRect } {
  validateRgbaImage(image);
  const rect = normalizedRectToPixels(roi, image.width, image.height);
  const data = new Uint8ClampedArray(rect.width * rect.height * 4);
  for (let row = 0; row < rect.height; row += 1) {
    const sourceStart = ((rect.y + row) * image.width + rect.x) * 4;
    const targetStart = row * rect.width * 4;
    data.set(image.data.subarray(sourceStart, sourceStart + rect.width * 4), targetStart);
  }
  return { image: { width: rect.width, height: rect.height, data }, rect };
}
