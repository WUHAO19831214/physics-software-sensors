import type { ConfigResult, HealthSnapshot, JsonObject, RuntimeFramePacket, SensorContext, SensorDescriptor, SourceSensor } from '@physics-software-sensors/core';
import { openCamera, closeCamera, lockCurrentCameraSettings, type CameraSnapshot } from './camera.js';

export interface CameraBackend {
  start(deviceId?: string): Promise<CameraSnapshot>;
  capture(): Promise<{ pixels: NonNullable<RuntimeFramePacket['pixels']>; sourceTimestamp: number } | null>;
  stop(): Promise<void>;
  lock?(): Promise<CameraSnapshot>;
}

export class DomCameraBackend implements CameraBackend {
  private stream: MediaStream | null = null;
  private video: HTMLVideoElement | null = null;
  private generation = 0;
  async start(deviceId?: string) {
    const generation = ++this.generation;
    const result = await openCamera(deviceId);
    if (generation !== this.generation) { closeCamera(result.stream); throw new Error('Camera start cancelled'); }
    this.stream = result.stream;
    const video = document.createElement('video'); video.muted = true; video.playsInline = true; video.srcObject = result.stream;
    this.video = video;
    try { await video.play(); if (generation !== this.generation) throw new Error('Camera start cancelled'); return result.snapshot; }
    catch (error) { await this.stop(); throw error; }
  }
  async capture() {
    const video = this.video;
    if (!video || video.readyState < 2 || !video.videoWidth || !video.videoHeight) return null;
    if (!this.stream?.getVideoTracks().some(track => track.readyState === 'live')) throw new Error('Camera stream ended');
    const canvas = document.createElement('canvas'); canvas.width = video.videoWidth; canvas.height = video.videoHeight;
    const context = canvas.getContext('2d', { willReadFrequently: true });
    if (!context) throw new Error('Canvas unavailable');
    context.drawImage(video, 0, 0);
    return { pixels: context.getImageData(0, 0, canvas.width, canvas.height), sourceTimestamp: video.currentTime };
  }
  async lock() { if (!this.stream) throw new Error('No active camera'); return lockCurrentCameraSettings(this.stream); }
  async stop() { this.generation++; closeCamera(this.stream); this.stream = null; if (this.video) { this.video.pause(); this.video.srcObject = null; this.video = null; } }
}

/** Browser backend for the existing camera.capture identity; no physical FPS claim. */
export class BrowserCameraSource implements SourceSensor {
  private state: HealthSnapshot['state'] = 'created';
  private context: SensorContext | null = null;
  private intervalMs = 250;
  private deviceId: string | undefined;
  private sequence = 0;
  private errors = 0;
  private startedAt = 0;
  private generation = 0;
  private reading = false;
  private abortHandler: (() => void) | null = null;
  private snapshot: CameraSnapshot | null = null;
  constructor(private readonly backend: CameraBackend = new DomCameraBackend()) {}
  describe(): SensorDescriptor { return { sensorId: 'camera.capture', version: '0.3.1', category: 'source', inputKinds: [], outputKinds: ['frame-packet.camera-frame'], capabilities: ['browser-get-user-media', 'camera-settings', 'original-rgba-pixels'], configSchemaVersion: '1.0.0', evidenceLevel: 'source-tested' }; }
  configure(config: JsonObject): ConfigResult {
    const intervalMs = Number(config.intervalMs ?? 250);
    if (this.state === 'running' || !Number.isFinite(intervalMs) || intervalMs < 16 || intervalMs > 60000) return { accepted: false, effectiveConfig: {}, warnings: ['Stop source and use intervalMs in [16,60000]'] };
    this.intervalMs = intervalMs; this.deviceId = typeof config.deviceId === 'string' ? config.deviceId : undefined; this.state = 'configured';
    return { accepted: true, effectiveConfig: { intervalMs, deviceId: this.deviceId ?? null }, warnings: [] };
  }
  async start(context: SensorContext) {
    if (this.state === 'running') throw new Error('Already running');
    if (!context.runId || context.cancellation?.aborted) throw new Error('Valid active context required');
    const generation = ++this.generation;
    this.context = context; this.sequence = 0; this.errors = 0; this.state = 'running';
    this.abortHandler = () => { void this.stop(); };
    context.cancellation?.addEventListener('abort', this.abortHandler, { once: true });
    try {
      this.snapshot = await this.backend.start(this.deviceId);
      if (generation !== this.generation) { await this.backend.stop(); throw new Error('Camera start cancelled'); }
      this.startedAt = performance.now();
    } catch (error) { if (generation === this.generation) { this.errors++; this.state = 'error'; await this.stop(); this.state = 'error'; } throw error; }
  }
  async lockSettings() { if (this.state !== 'running' || !this.backend.lock) throw new Error('Settings lock unavailable'); this.snapshot = await this.backend.lock(); return this.snapshot; }
  settings() { return this.snapshot ? structuredClone(this.snapshot) : null; }
  health(): HealthSnapshot { const elapsed = performance.now() - this.startedAt; return { state: this.state, processedCount: this.sequence, droppedCount: 0, lostCount: 0, errorCount: this.errors, actualRateHz: this.sequence && elapsed > 0 ? this.sequence * 1000 / elapsed : 0, latencyMs: {} }; }
  async *read(): AsyncIterable<RuntimeFramePacket> {
    if (this.state !== 'running' || !this.context) throw new Error('Start camera first');
    if (this.reading) throw new Error('Only one camera reader is supported');
    this.reading = true;
    const generation = this.generation;
    let lastTimestamp: number | null = null;
    try {
      while (this.state === 'running' && this.context && generation === this.generation) {
        const result = await this.backend.capture();
        if (this.state !== 'running' || !this.context || generation !== this.generation) break;
        if (result && result.sourceTimestamp !== lastTimestamp) {
          lastTimestamp = result.sourceTimestamp;
          const sequence = this.sequence++;
          yield { frameId: crypto.randomUUID(), runId: this.context.runId, sequence, observedAt: new Date().toISOString(), monotonicNs: Math.round(performance.now() * 1e6), sourceTimestamp: result.sourceTimestamp, sourceSensorId: 'camera.capture', media: { kind: 'camera-frame', width: result.pixels.width, height: result.pixels.height, mediaType: 'image/raw-rgba', colorSpace: 'RGBA' }, artifactUri: `memory://camera/${generation}/${sequence}`, droppedSinceLast: 0, qualityFlags: ['browser-sampling-clock', 'hardware-drop-count-unavailable'], payload: { requested_interval_ms: this.intervalMs, camera_settings: this.snapshot?.settings as unknown as JsonObject ?? {}, timestamp_definition: 'browser-video-current-time-seconds', dropped_count_measured: false }, pixels: result.pixels };
        }
        await new Promise<void>(resolve => { const timer = setTimeout(done, this.intervalMs); const signal = this.context?.cancellation; function done() { clearTimeout(timer); signal?.removeEventListener('abort', done); resolve(); } signal?.addEventListener('abort', done, { once: true }); });
      }
    } catch (error) { this.errors++; await this.stop(); this.state = 'error'; throw error; }
    finally { this.reading = false; }
  }
  async stop() { this.generation++; if (this.abortHandler) this.context?.cancellation?.removeEventListener('abort', this.abortHandler); this.abortHandler = null; this.context = null; this.snapshot = null; this.state = 'stopped'; await this.backend.stop(); }
}
