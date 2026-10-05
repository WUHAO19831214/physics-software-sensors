/** Pixel-only OCR preprocessing extracted from the fixed source implementation. */

import { validateRgbaImage, type RgbaImage } from '../core/pixels.js';

export type PreprocessMode = 'auto' | 'default' | 'invert' | 'high-contrast' | 'color-number';

export interface NumberPreprocessOptions {
  scale?: number;
  threshold?: number;
  invert?: boolean;
  removeNoise?: boolean;
  padding?: number;
  autoScale?: boolean;
}

/** Resolves an optimal integer scale factor to bring small text up to target pixel height (default 120px). */
export function resolveOptimalScale(height: number, targetHeight = 120): number {
  if (!Number.isFinite(targetHeight) || targetHeight <= 0) throw new RangeError('Target height must be finite and positive');
  if (!Number.isFinite(height) || height <= 0) return 4;
  const ideal = Math.round(targetHeight / height);
  return Math.max(1, Math.min(6, ideal));
}

export function addRgbaPadding(input: RgbaImage, padding: number, fillVal = 255): RgbaImage {
  validateRgbaImage(input);
  if (!Number.isInteger(padding) || padding < 0) throw new RangeError('Padding must be a nonnegative integer');
  if (padding === 0) return input;
  if (!Number.isFinite(fillVal) || fillVal < 0 || fillVal > 255) throw new RangeError('Padding color must be between 0 and 255');
  const width = input.width + padding * 2;
  const height = input.height + padding * 2;
  const data = new Uint8ClampedArray(width * height * 4);
  data.fill(fillVal);
  for (let i = 3; i < data.length; i += 4) data[i] = 255;
  for (let y = 0; y < input.height; y += 1) {
    const srcRow = y * input.width * 4;
    const dstRow = ((y + padding) * width + padding) * 4;
    data.set(input.data.subarray(srcRow, srcRow + input.width * 4), dstRow);
  }
  return { width, height, data };
}

function resizeNearest(image: RgbaImage, scale: number): RgbaImage {
  if (!Number.isInteger(scale) || scale < 1) throw new Error('preprocess scale must be a positive integer');
  if (scale === 1) return { ...image, data: new Uint8ClampedArray(image.data) };
  const width = image.width * scale;
  const height = image.height * scale;
  const data = new Uint8ClampedArray(width * height * 4);
  for (let y = 0; y < height; y += 1) {
    const sourceY = Math.floor(y / scale);
    for (let x = 0; x < width; x += 1) {
      const sourceX = Math.floor(x / scale);
      const source = (sourceY * image.width + sourceX) * 4;
      const target = (y * width + x) * 4;
      data[target] = image.data[source] ?? 0;
      data[target + 1] = image.data[source + 1] ?? 0;
      data[target + 2] = image.data[source + 2] ?? 0;
      data[target + 3] = image.data[source + 3] ?? 255;
    }
  }
  return { width, height, data };
}

function removeIsolatedPixels(data: Uint8ClampedArray, width: number, height: number): void {
  const copy = new Uint8ClampedArray(data);
  for (let y = 1; y < height - 1; y += 1) {
    for (let x = 1; x < width - 1; x += 1) {
      const index = (y * width + x) * 4;
      if (copy[index] !== 0) continue;
      let darkNeighbors = 0;
      for (let oy = -1; oy <= 1; oy += 1) {
        for (let ox = -1; ox <= 1; ox += 1) {
          if (ox === 0 && oy === 0) continue;
          if (copy[((y + oy) * width + x + ox) * 4] === 0) darkNeighbors += 1;
        }
      }
      if (darkNeighbors <= 1) {
        data[index] = 255;
        data[index + 1] = 255;
        data[index + 2] = 255;
      }
    }
  }
}

export function preprocessForNumberRecognition(
  input: RgbaImage,
  options: NumberPreprocessOptions = {},
): RgbaImage {
  validateRgbaImage(input);
  const padded = options.padding ? addRgbaPadding(input, options.padding) : input;
  const scale = options.autoScale
    ? resolveOptimalScale(padded.height)
    : (options.scale ?? 4);
  const threshold = options.threshold ?? 150;
  const processed = resizeNearest(padded, scale);
  for (let index = 0; index < processed.data.length; index += 4) {
    const red = processed.data[index] ?? 0;
    const green = processed.data[index + 1] ?? 0;
    const blue = processed.data[index + 2] ?? 0;
    const gray = 0.299 * red + 0.587 * green + 0.114 * blue;
    const contrast = Math.max(0, Math.min(255, (gray - 128) * 1.9 + 128));
    let value = contrast > threshold ? 255 : 0;
    if (options.invert) value = 255 - value;
    processed.data[index] = value;
    processed.data[index + 1] = value;
    processed.data[index + 2] = value;
    processed.data[index + 3] = 255;
  }
  if (options.removeNoise ?? true) removeIsolatedPixels(processed.data, processed.width, processed.height);
  return processed;
}

function sharpenImageData(input: RgbaImage): RgbaImage {
  const output: RgbaImage = { ...input, data: new Uint8ClampedArray(input.data) };
  for (let y = 1; y < input.height - 1; y += 1) {
    for (let x = 1; x < input.width - 1; x += 1) {
      const index = (y * input.width + x) * 4;
      for (let channel = 0; channel < 3; channel += 1) {
        const center = (input.data[index + channel] ?? 0) * 5;
        const left = input.data[index - 4 + channel] ?? 0;
        const right = input.data[index + 4 + channel] ?? 0;
        const top = input.data[index - input.width * 4 + channel] ?? 0;
        const bottom = input.data[index + input.width * 4 + channel] ?? 0;
        output.data[index + channel] = Math.max(0, Math.min(255, center - left - right - top - bottom));
      }
    }
  }
  return output;
}

function extractColoredDigits(input: RgbaImage): RgbaImage {
  const data = new Uint8ClampedArray(input.data.length);
  for (let index = 0; index < input.data.length; index += 4) {
    const red = input.data[index] ?? 0;
    const green = input.data[index + 1] ?? 0;
    const blue = input.data[index + 2] ?? 0;
    const saturation = Math.max(red, green, blue) - Math.min(red, green, blue);
    const blueDigit = blue > red * 1.1 && blue > green * 1.05 && saturation > 28;
    const magentaDigit = red > 120 && blue > 100 && green < 170 && saturation > 28;
    const darkBlueDigit = blue > 70 && red < 120 && green < 150 && saturation > 20;
    const value = blueDigit || magentaDigit || darkBlueDigit ? 0 : 255;
    data[index] = value;
    data[index + 1] = value;
    data[index + 2] = value;
    data[index + 3] = 255;
  }
  return { width: input.width, height: input.height, data };
}

export function preprocessForLangweiNumber(input: RgbaImage, mode: PreprocessMode = 'auto'): RgbaImage {
  if (mode === 'invert') {
    return preprocessForNumberRecognition(input, { scale: 4, threshold: 145, invert: true, removeNoise: true });
  }
  if (mode === 'high-contrast') {
    return preprocessForNumberRecognition(sharpenImageData(input), {
      scale: 4,
      threshold: 135,
      removeNoise: true,
    });
  }
  if (mode === 'color-number') {
    return preprocessForNumberRecognition(extractColoredDigits(input), {
      scale: 4,
      threshold: 210,
      removeNoise: true,
    });
  }
  return preprocessForNumberRecognition(input, {
    scale: 4,
    threshold: mode === 'auto' ? 142 : 150,
    removeNoise: true,
  });
}
