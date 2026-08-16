/** Tesseract.js backend for real RGBA pixel frames. */

import Tesseract from 'tesseract.js';

import { cropNormalizedRoi, validateRgbaImage, type PixelRect, type RgbaImage } from '../core/pixels.js';
import type { JsonObject } from '../core/types.js';
import type { NumberRecognizer, OcrRecognitionResult, RecognizeRequest } from './number.js';
import { preprocessForLangweiNumber, type PreprocessMode } from './preprocess.js';

type TesseractWorker = Awaited<ReturnType<typeof Tesseract.createWorker>>;
type TesseractImage = Parameters<TesseractWorker['recognize']>[0];

export type TesseractRuntimeState = 'not-loaded' | 'loading' | 'ready' | 'recognizing' | 'error' | 'closed';

export interface TesseractRuntimeStatus {
  state: TesseractRuntimeState;
  error?: string;
}

export interface TesseractDebugArtifacts {
  roi: RgbaImage;
  preprocessed: RgbaImage;
  pixelRect: PixelRect;
}

export interface TesseractJsRecognizerOptions {
  language?: string;
  psmMode?: 'SINGLE_LINE' | 'SINGLE_WORD' | 'SINGLE_BLOCK';
  preprocessMode?: PreprocessMode;
  whitelist?: string;
  workerOptions?: Partial<Tesseract.WorkerOptions>;
  imageEncoder?: (image: RgbaImage) => Promise<TesseractImage>;
}

function mapPsmMode(mode: TesseractJsRecognizerOptions['psmMode']): Tesseract.PSM {
  if (mode === 'SINGLE_WORD') return Tesseract.PSM.SINGLE_WORD;
  if (mode === 'SINGLE_BLOCK') return Tesseract.PSM.SINGLE_BLOCK;
  return Tesseract.PSM.SINGLE_LINE;
}

async function encodeForTesseract(image: RgbaImage): Promise<TesseractImage> {
  validateRgbaImage(image);
  if (typeof document !== 'undefined' && typeof ImageData !== 'undefined') {
    const canvas = document.createElement('canvas');
    canvas.width = image.width;
    canvas.height = image.height;
    const context = canvas.getContext('2d', { willReadFrequently: true });
    if (!context) throw new Error('cannot create browser canvas for OCR');
    context.putImageData(new ImageData(new Uint8ClampedArray(image.data), image.width, image.height), 0, 0);
    return canvas;
  }

  const { PNG } = await import('pngjs');
  const png = new PNG({ width: image.width, height: image.height });
  png.data = Buffer.from(image.data.buffer, image.data.byteOffset, image.data.byteLength);
  return PNG.sync.write(png);
}

export class TesseractJsRecognizer implements NumberRecognizer {
  readonly id = 'tesseract.js';
  readonly replay = false;
  private readonly options: Required<
    Pick<TesseractJsRecognizerOptions, 'language' | 'psmMode' | 'preprocessMode' | 'whitelist'>
  > & TesseractJsRecognizerOptions;
  private workerPromise: Promise<TesseractWorker> | null = null;
  private queue: Promise<unknown> = Promise.resolve();
  private status: TesseractRuntimeStatus = { state: 'not-loaded' };
  private artifacts: TesseractDebugArtifacts | null = null;

  constructor(options: TesseractJsRecognizerOptions = {}) {
    this.options = {
      language: options.language ?? 'eng',
      psmMode: options.psmMode ?? 'SINGLE_LINE',
      preprocessMode: options.preprocessMode ?? 'auto',
      whitelist: options.whitelist ?? '0123456789.-',
      ...options,
    };
  }

  runtimeStatus(): TesseractRuntimeStatus {
    return { ...this.status };
  }

  lastArtifacts(): TesseractDebugArtifacts | null {
    if (!this.artifacts) return null;
    return {
      pixelRect: { ...this.artifacts.pixelRect },
      roi: { ...this.artifacts.roi, data: new Uint8ClampedArray(this.artifacts.roi.data) },
      preprocessed: {
        ...this.artifacts.preprocessed,
        data: new Uint8ClampedArray(this.artifacts.preprocessed.data),
      },
    };
  }

  private async worker(): Promise<TesseractWorker> {
    if (!this.workerPromise) {
      this.status = { state: 'loading' };
      this.workerPromise = Tesseract.createWorker(
        this.options.language,
        Tesseract.OEM.LSTM_ONLY,
        this.options.workerOptions,
      )
        .then(async (worker) => {
          await worker.setParameters({
            tessedit_char_whitelist: this.options.whitelist,
            tessedit_pageseg_mode: mapPsmMode(this.options.psmMode),
            preserve_interword_spaces: '0',
            user_defined_dpi: '300',
          });
          this.status = { state: 'ready' };
          return worker;
        })
        .catch((error: unknown) => {
          const message = error instanceof Error ? error.message : 'Tesseract.js worker initialization failed';
          this.workerPromise = null;
          this.status = { state: 'error', error: message };
          throw error;
        });
    }
    return this.workerPromise;
  }

  async recognize(input: RecognizeRequest): Promise<OcrRecognitionResult> {
    const execute = async (): Promise<OcrRecognitionResult> => {
      const started = performance.now();
      try {
        const pixels = input.frame.pixels;
        if (!pixels) throw new Error('TesseractJsRecognizer requires RuntimeFramePacket.pixels');
        validateRgbaImage(pixels);
        if (pixels.width !== input.frame.media.width || pixels.height !== input.frame.media.height) {
          throw new Error('RGBA pixel dimensions do not match FramePacket media');
        }
        const cropped = cropNormalizedRoi(pixels, input.roi);
        const preprocessed = preprocessForLangweiNumber(cropped.image, this.options.preprocessMode);
        this.artifacts = { roi: cropped.image, preprocessed, pixelRect: cropped.rect };
        const encoder = this.options.imageEncoder ?? encodeForTesseract;
        const encoded = await encoder(preprocessed);
        const worker = await this.worker();
        this.status = { state: 'recognizing' };
        await worker.setParameters({
          tessedit_char_whitelist: this.options.whitelist,
          tessedit_pageseg_mode: mapPsmMode(this.options.psmMode),
        });
        const result = await worker.recognize(encoded);
        const rawText = result.data.text.trim();
        const confidence = Number((Math.max(0, Math.min(100, result.data.confidence)) / 100).toFixed(3));
        const durationMs = Math.round(performance.now() - started);
        this.status = { state: 'ready' };
        return {
          method: this.id,
          rawText,
          confidence,
          durationMs,
          ...(rawText ? {} : { warning: `${input.roiId} OCR returned empty text` }),
          details: {
            language: this.options.language,
            psm_mode: this.options.psmMode,
            preprocess_mode: this.options.preprocessMode,
            pixel_roi: cropped.rect as unknown as JsonObject,
          },
        };
      } catch (error) {
        const message = error instanceof Error ? error.message : `${input.roiId} Tesseract.js recognition failed`;
        this.status = { state: 'error', error: message };
        return {
          method: this.id,
          rawText: '',
          confidence: 0,
          durationMs: Math.round(performance.now() - started),
          warning: message,
          error: message,
        };
      }
    };

    const pending = this.queue.then(execute, execute);
    this.queue = pending.catch(() => undefined);
    return pending;
  }

  async close(): Promise<void> {
    await this.queue.catch(() => undefined);
    const worker = this.workerPromise ? await this.workerPromise.catch(() => null) : null;
    if (worker) await worker.terminate();
    this.workerPromise = null;
    this.status = { state: 'closed' };
  }
}
