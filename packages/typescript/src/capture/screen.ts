/** User-authorized browser screen capture and deterministic replay sources. */

import type {
  ConfigResult,
  HealthSnapshot,
  JsonObject,
  LifecycleState,
  RuntimeFramePacket,
  SensorContext,
  SensorDescriptor,
  SourceSensor,
} from '../core/types.js';
import type { RgbaImage } from '../core/pixels.js';

export interface ScreenCaptureConfig {
  requestedIntervalMs: number;
  artifactPrefix: string;
}

export interface CapturedScreenFrame {
  pixels: RgbaImage;
  sourceTimestamp?: number | null;
  observedAt?: string;
  monotonicNs?: number;
  droppedSinceLast?: number;
  artifactUri?: string;
  qualityFlags?: string[];
  metadata?: JsonObject;
}

export interface ScreenBackendInfo extends JsonObject {
  backend: string;
  user_authorized: boolean;
  deterministic_replay: boolean;
}

export interface ScreenCaptureBackend {
  readonly backendId: string;
  readonly live: boolean;
  start(config: ScreenCaptureConfig): Promise<ScreenBackendInfo>;
  read(): Promise<CapturedScreenFrame | null>;
  stop(): Promise<void>;
}

export class ScreenCaptureError extends Error {
  constructor(
    readonly code: string,
    message: string,
    readonly retryable = true,
  ) {
    super(message);
    this.name = 'ScreenCaptureError';
  }
}

export class RecordedScreenBackend implements ScreenCaptureBackend {
  readonly backendId = 'recorded-screen';
  readonly live = false;
  private index = 0;
  private running = false;

  constructor(
    private readonly frames: readonly CapturedScreenFrame[],
    private readonly sourceName = 'recorded-screen-sequence',
  ) {}

  async start(_config: ScreenCaptureConfig): Promise<ScreenBackendInfo> {
    this.index = 0;
    this.running = true;
    const first = this.frames[0];
    return {
      backend: this.backendId,
      source_name: this.sourceName,
      user_authorized: false,
      deterministic_replay: true,
      actual_width: first?.pixels.width ?? null,
      actual_height: first?.pixels.height ?? null,
      nominal_fps: null,
    };
  }

  async read(): Promise<CapturedScreenFrame | null> {
    if (!this.running) throw new ScreenCaptureError('SCREEN_CAPTURE_NOT_RUNNING', 'recorded source is not running');
    const frame = this.frames[this.index];
    if (!frame) return null;
    this.index += 1;
    return {
      ...frame,
      pixels: { ...frame.pixels, data: new Uint8ClampedArray(frame.pixels.data) },
      qualityFlags: [...(frame.qualityFlags ?? []), 'recorded-replay'],
      metadata: { ...(frame.metadata ?? {}) },
    };
  }

  async stop(): Promise<void> {
    this.running = false;
  }
}

export interface BrowserScreenDriver {
  request(): Promise<ScreenBackendInfo>;
  read(): Promise<CapturedScreenFrame | null>;
  stop(): Promise<void>;
}

/**
 * DOM implementation. `request()` is the permission boundary and must be
 * called synchronously from a user gesture through `ScreenCaptureSource.start()`.
 */
export class MediaDevicesScreenDriver implements BrowserScreenDriver {
  private stream: MediaStream | null = null;
  private video: HTMLVideoElement | null = null;
  private canvas: HTMLCanvasElement | null = null;
  private ended = false;

  async request(): Promise<ScreenBackendInfo> {
    if (!globalThis.navigator?.mediaDevices?.getDisplayMedia || !globalThis.document) {
      throw new ScreenCaptureError('SCREEN_CAPTURE_UNSUPPORTED', 'getDisplayMedia and DOM canvas are required', false);
    }
    try {
      this.stream = await globalThis.navigator.mediaDevices.getDisplayMedia({ video: true, audio: false });
    } catch (error) {
      const name = error instanceof DOMException ? error.name : 'UnknownError';
      const code = name === 'NotAllowedError' ? 'SCREEN_CAPTURE_PERMISSION_DENIED' : 'SCREEN_CAPTURE_REQUEST_FAILED';
      throw new ScreenCaptureError(code, `screen/window selection failed: ${name}`);
    }
    const track = this.stream.getVideoTracks()[0];
    if (!track) {
      await this.stop();
      throw new ScreenCaptureError('SCREEN_CAPTURE_NO_VIDEO_TRACK', 'selected stream has no video track');
    }
    this.ended = false;
    track.addEventListener('ended', () => { this.ended = true; }, { once: true });
    this.video = globalThis.document.createElement('video');
    this.video.muted = true;
    this.video.playsInline = true;
    this.video.srcObject = this.stream;
    try {
      await this.video.play();
    } catch (error) {
      await this.stop();
      throw new ScreenCaptureError(
        'SCREEN_CAPTURE_VIDEO_START_FAILED',
        `shared video could not start: ${error instanceof Error ? error.message : String(error)}`,
      );
    }
    this.canvas = globalThis.document.createElement('canvas');
    const settings = track.getSettings();
    return {
      backend: 'browser-get-display-media',
      user_authorized: true,
      deterministic_replay: false,
      display_surface: settings.displaySurface ?? null,
      actual_width: settings.width ?? this.video.videoWidth ?? null,
      actual_height: settings.height ?? this.video.videoHeight ?? null,
      nominal_fps: settings.frameRate ?? null,
      browser_user_agent: globalThis.navigator.userAgent,
      platform: globalThis.navigator.platform,
    };
  }

  async read(): Promise<CapturedScreenFrame> {
    if (this.ended) throw new ScreenCaptureError('SCREEN_CAPTURE_ENDED', 'the user or browser ended screen sharing', false);
    if (!this.video || !this.canvas) throw new ScreenCaptureError('SCREEN_CAPTURE_NOT_RUNNING', 'screen capture is not running');
    const width = this.video.videoWidth;
    const height = this.video.videoHeight;
    if (width < 1 || height < 1) throw new ScreenCaptureError('SCREEN_FRAME_NOT_READY', 'screen video has no decoded frame yet');
    this.canvas.width = width;
    this.canvas.height = height;
    const context = this.canvas.getContext('2d', { willReadFrequently: true });
    if (!context) throw new ScreenCaptureError('SCREEN_CANVAS_UNAVAILABLE', '2D canvas context is unavailable', false);
    context.drawImage(this.video, 0, 0, width, height);
    const image = context.getImageData(0, 0, width, height);
    return {
      pixels: { width, height, data: new Uint8ClampedArray(image.data) },
      sourceTimestamp: null,
      metadata: { capture_api: 'getDisplayMedia', sampling_clock: 'browser-performance' },
    };
  }

  async stop(): Promise<void> {
    this.stream?.getTracks().forEach((track) => track.stop());
    if (this.video) this.video.srcObject = null;
    this.stream = null;
    this.video = null;
    this.canvas = null;
    this.ended = true;
  }
}

export class BrowserScreenBackend implements ScreenCaptureBackend {
  readonly backendId = 'browser-get-display-media';
  readonly live = true;

  constructor(private readonly driver: BrowserScreenDriver = new MediaDevicesScreenDriver()) {}

  async start(_config: ScreenCaptureConfig): Promise<ScreenBackendInfo> {
    return this.driver.request();
  }

  async read(): Promise<CapturedScreenFrame | null> {
    return this.driver.read();
  }

  async stop(): Promise<void> {
    await this.driver.stop();
  }
}

function nowMonotonicNs(): number {
  return Math.round(globalThis.performance.now() * 1_000_000);
}

async function digestSha256(data: Uint8ClampedArray): Promise<string> {
  const copy = new Uint8Array(data.byteLength);
  copy.set(data);
  const digest = await globalThis.crypto.subtle.digest('SHA-256', copy.buffer);
  return [...new Uint8Array(digest)].map((value) => value.toString(16).padStart(2, '0')).join('');
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => globalThis.setTimeout(resolve, ms));
}

export function serializeRuntimeFramePacket(frame: RuntimeFramePacket): JsonObject {
  if (!frame.artifactSha256) throw new Error('serializable FramePacket requires artifactSha256');
  return {
    schema_version: '1.0.0',
    frame_id: frame.frameId,
    run_id: frame.runId,
    source_sensor_id: frame.sourceSensorId,
    sequence: frame.sequence,
    observed_at: frame.observedAt,
    monotonic_ns: frame.monotonicNs,
    source_timestamp: frame.sourceTimestamp ?? null,
    media: {
      kind: frame.media.kind,
      media_type: frame.media.mediaType,
      width: frame.media.width,
      height: frame.media.height,
      color_space: frame.media.colorSpace,
      orientation: frame.media.orientation ?? '0',
      mirrored: frame.media.mirrored ?? false,
    },
    artifact: {
      uri: frame.artifactUri,
      media_type: frame.media.mediaType,
      sha256: frame.artifactSha256,
      bytes: frame.artifactBytes ?? null,
    },
    quality: {
      dropped_since_last: frame.droppedSinceLast ?? 0,
      flags: frame.qualityFlags ?? [],
    },
    payload: frame.payload ?? {},
  };
}

export class ScreenCaptureSource implements SourceSensor {
  private state: LifecycleState = 'created';
  private context: SensorContext | null = null;
  private config: ScreenCaptureConfig = { requestedIntervalMs: 500, artifactPrefix: 'runtime://screen.capture' };
  private backendInfo: ScreenBackendInfo | null = null;
  private sequence = 0;
  private processedCount = 0;
  private droppedCount = 0;
  private errorCount = 0;
  private lastError: JsonObject | undefined;
  private lastMonotonicNs: number | undefined;
  private actualRateHz: number | undefined;

  constructor(
    private readonly backend: ScreenCaptureBackend,
    private readonly instanceId = 'screen-source-01',
    private readonly clocks: {
      observedAt: () => string;
      monotonicNs: () => number;
      frameId: () => string;
    } = {
      observedAt: () => new Date().toISOString(),
      monotonicNs: nowMonotonicNs,
      frameId: () => globalThis.crypto.randomUUID(),
    },
  ) {}

  describe(): SensorDescriptor {
    return {
      sensorId: 'screen.capture',
      version: '0.3.0',
      category: 'source',
      inputKinds: [],
      outputKinds: ['frame-packet.screen-frame'],
      capabilities: [
        'browser-get-display-media',
        'recorded-screen-replay',
        'requested-vs-measured-sampling-rate',
        'runtime-rgba-pixels',
        'stream-end-detection',
      ],
      configSchemaVersion: '1.0.0',
      evidenceLevel: 'replay-benchmarked',
    };
  }

  configure(config: JsonObject): ConfigResult {
    if (this.state === 'running') throw new Error('stop screen capture before reconfiguring it');
    const allowed = new Set(['requestedIntervalMs', 'artifactPrefix']);
    const unknown = Object.keys(config).filter((key) => !allowed.has(key));
    if (unknown.length > 0) throw new Error(`unknown screen capture settings: ${unknown.sort().join(', ')}`);
    const requestedIntervalMs = Number(config.requestedIntervalMs ?? this.config.requestedIntervalMs);
    const artifactPrefix = String(config.artifactPrefix ?? this.config.artifactPrefix);
    if (!Number.isFinite(requestedIntervalMs) || requestedIntervalMs <= 0) {
      throw new Error('requestedIntervalMs must be positive');
    }
    if (!artifactPrefix) throw new Error('artifactPrefix is required');
    this.config = { requestedIntervalMs, artifactPrefix };
    this.state = 'configured';
    return { accepted: true, effectiveConfig: { requestedIntervalMs, artifactPrefix }, warnings: [] };
  }

  /** Browser callers must invoke this directly from a user click/gesture. */
  async start(context: SensorContext): Promise<void> {
    if (this.state === 'running') return;
    this.context = context;
    try {
      this.backendInfo = await this.backend.start(this.config);
    } catch (error) {
      this.state = 'error';
      this.errorCount += 1;
      this.lastError = {
        code: error instanceof ScreenCaptureError ? error.code : 'SCREEN_CAPTURE_START_FAILED',
        message: error instanceof Error ? error.message : String(error),
      };
      throw error;
    }
    this.sequence = 0;
    this.processedCount = 0;
    this.droppedCount = 0;
    this.lastMonotonicNs = undefined;
    this.actualRateHz = undefined;
    this.state = 'running';
  }

  async *read(): AsyncIterable<RuntimeFramePacket> {
    if (this.state !== 'running') throw new ScreenCaptureError('SCREEN_CAPTURE_NOT_RUNNING', 'screen source must be running');
    while (this.state === 'running') {
      if (this.backend.live && this.processedCount > 0) await sleep(this.config.requestedIntervalMs);
      const frame = await this.readOne();
      if (!frame) break;
      yield frame;
    }
  }

  async readOne(): Promise<RuntimeFramePacket | null> {
    if (this.state !== 'running' || !this.context || !this.backendInfo) {
      throw new ScreenCaptureError('SCREEN_CAPTURE_NOT_RUNNING', 'screen source must be running');
    }
    let captured: CapturedScreenFrame | null;
    try {
      captured = await this.backend.read();
    } catch (error) {
      this.state = 'error';
      this.errorCount += 1;
      this.lastError = {
        code: error instanceof ScreenCaptureError ? error.code : 'SCREEN_CAPTURE_READ_FAILED',
        message: error instanceof Error ? error.message : String(error),
      };
      throw error;
    }
    if (!captured) return null;
    const monotonicNs = captured.monotonicNs ?? this.clocks.monotonicNs();
    if (this.lastMonotonicNs !== undefined && monotonicNs > this.lastMonotonicNs) {
      this.actualRateHz = 1_000_000_000 / (monotonicNs - this.lastMonotonicNs);
    }
    this.lastMonotonicNs = monotonicNs;
    const frameId = this.clocks.frameId();
    const dropped = captured.droppedSinceLast ?? 0;
    const flags = [...new Set([...(captured.qualityFlags ?? []), ...(dropped ? ['frame-dropped'] : [])])];
    const sha256 = await digestSha256(captured.pixels.data);
    const packet: RuntimeFramePacket = {
      frameId,
      runId: this.context.runId,
      sequence: this.sequence,
      observedAt: captured.observedAt ?? this.clocks.observedAt(),
      monotonicNs,
      sourceTimestamp: captured.sourceTimestamp ?? null,
      sourceSensorId: 'screen.capture',
      media: {
        kind: 'screen-frame',
        width: captured.pixels.width,
        height: captured.pixels.height,
        mediaType: 'application/x-raw-rgba',
        colorSpace: 'RGBA',
        orientation: '0',
        mirrored: false,
      },
      artifactUri: captured.artifactUri ?? `${this.config.artifactPrefix}/${frameId}`,
      artifactSha256: sha256,
      artifactBytes: captured.pixels.data.byteLength,
      droppedSinceLast: dropped,
      qualityFlags: flags,
      payload: {
        capture: {
          backend: this.backend.backendId,
          instance_id: this.instanceId,
          user_authorized: this.backendInfo.user_authorized,
          requested: { sampling_interval_ms: this.config.requestedIntervalMs },
          actual: {
            measured_interval_ms: this.actualRateHz ? 1_000 / this.actualRateHz : null,
            measured_rate_hz: this.actualRateHz ?? null,
            width: captured.pixels.width,
            height: captured.pixels.height,
          },
          backend_info: this.backendInfo,
          frame: captured.metadata ?? {},
        },
      },
      pixels: captured.pixels,
    };
    this.sequence += 1;
    this.processedCount += 1;
    this.droppedCount += dropped;
    return packet;
  }

  health(): HealthSnapshot {
    return {
      state: this.state,
      processedCount: this.processedCount,
      droppedCount: this.droppedCount,
      lostCount: 0,
      errorCount: this.errorCount,
      ...(this.actualRateHz === undefined ? {} : { actualRateHz: this.actualRateHz }),
      latencyMs: {},
      ...(this.lastError === undefined ? {} : { lastError: this.lastError }),
    };
  }

  async stop(): Promise<void> {
    if (this.state === 'stopped') return;
    this.state = 'stopping';
    await this.backend.stop();
    this.state = 'stopped';
  }
}
