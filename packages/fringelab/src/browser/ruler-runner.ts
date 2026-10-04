import { detectPhysicalRuler, type RulerDetectionResult } from '../core/ruler-detection.js';
import type { ImageDataLike } from '../core/signal.js';

type Options = Parameters<typeof detectPhysicalRuler>[1];
/** Terminates obsolete work; callers bind source changes to cancel(). */
export class RulerDetectionRunner {
  private worker: Worker | null = null;
  private reject: ((error: Error) => void) | null = null;
  private generation = 0;
  constructor(private readonly useWorker = true) {}
  cancel() { this.generation++; this.worker?.terminate(); this.worker = null; this.reject?.(new DOMException('Ruler detection cancelled', 'AbortError')); this.reject = null; }
  async detect(image: ImageDataLike, options: Options, signal?: AbortSignal): Promise<RulerDetectionResult | null> {
    this.cancel();
    if (signal?.aborted) throw new DOMException('Cancelled', 'AbortError');
    const id = this.generation;
    const abort = () => this.cancel(); signal?.addEventListener('abort', abort, { once: true });
    try {
      if (!this.useWorker || typeof Worker === 'undefined') {
        await Promise.resolve();
        if (id !== this.generation) throw new DOMException('Cancelled', 'AbortError');
        return detectPhysicalRuler(image, options);
      }
      return await new Promise((resolve, reject) => {
        this.reject = reject;
        const worker = new Worker(new URL('./ruler.worker.js', import.meta.url), { type: 'module' }); this.worker = worker;
        worker.onmessage = event => { if (id !== this.generation || event.data.id !== id) return; event.data.error ? reject(new Error(event.data.error)) : resolve(event.data.result); };
        worker.onerror = event => reject(new Error(event.message));
        const pixels = new Uint8ClampedArray(Array.from(image.data));
        worker.postMessage({ ...options, id, width: image.width, height: image.height, buffer: pixels.buffer, contrastMode: options.contrastMode ?? 'auto', tickSnapEnabled: options.tickSnapEnabled ?? true, numberSnapEnabled: options.numberSnapEnabled ?? true, manualOriginMm: options.manualOriginMm ?? null }, [pixels.buffer]);
      });
    } finally { signal?.removeEventListener('abort', abort); if (id === this.generation) { this.worker?.terminate(); this.worker = null; this.reject = null; } }
  }
}
