/**
 * Experimental Number OCR adapter.
 *
 * Parser behavior is anchored to both source repositories at the commits
 * recorded in sensors/ocr.number/SOURCE.md. This module does not yet perform
 * Tesseract inference; the recorded recognizer only replays captured results.
 */

import type {
  ConfigResult,
  HealthSnapshot,
  JsonObject,
  LifecycleState,
  ProcessorSensor,
  RuntimeFramePacket,
  SensorContext,
  SensorDescriptor,
} from '../core/types.js';
import { validateNormalizedRect, type NormalizedRect } from '../core/pixels.js';

const DECIMAL_NUMBER = /[+-]?(?:(?:\d+\.\d*)|(?:\d*\.\d+)|(?:\d+))/g;

export type Rect = NormalizedRect;

export interface OcrRecognitionResult {
  method: string;
  rawText: string;
  confidence: number;
  durationMs: number;
  warning?: string;
  error?: string;
  details?: JsonObject;
}

export interface RecognizeRequest {
  frame: RuntimeFramePacket;
  roiId: string;
  roi: Rect;
}

export interface NumberRecognizer {
  readonly id: string;
  readonly replay: boolean;
  recognize(input: RecognizeRequest): Promise<OcrRecognitionResult>;
  close?(): Promise<void>;
}

export interface RecordedRecognition {
  frameId: string;
  roiId: string;
  result: OcrRecognitionResult;
}

export interface NumberOCRConfig {
  roiId: string;
  roi: Rect;
  name: string;
  symbol: string;
  unit: string;
}

export function normalizeOcrText(text: string): string {
  return text
    .replace(/[Oo]/g, '0')
    .replace(/[Il|]/g, '1')
    .replace(/S/g, '5')
    .replace(/B/g, '8')
    .replace(/[，]/g, '.')
    .replace(/\s+/g, '')
    .replace(/[^0-9+\-.]/g, '');
}

export function extractNumberFromText(text: string): number | null {
  const normalized = normalizeOcrText(text);
  const matches = normalized.match(DECIMAL_NUMBER);
  if (!matches?.length) return null;

  const candidates = matches
    .map((candidate) => ({ text: candidate, value: Number(candidate) }))
    .filter((candidate) => Number.isFinite(candidate.value))
    .sort((left, right) => {
      const leftHasDecimal = left.text.includes('.') ? 1 : 0;
      const rightHasDecimal = right.text.includes('.') ? 1 : 0;
      const leftLength = left.text.replace(/[+-.]/g, '').length;
      const rightLength = right.text.replace(/[+-.]/g, '').length;
      return rightHasDecimal - leftHasDecimal || rightLength - leftLength;
    });
  const value = candidates[0]?.value;
  return value !== undefined && Number.isFinite(value) ? value : null;
}

export class RecordedNumberRecognizer implements NumberRecognizer {
  readonly id = 'recorded-source-result';
  readonly replay = true;
  private readonly records: Map<string, OcrRecognitionResult>;

  constructor(records: RecordedRecognition[]) {
    this.records = new Map(records.map((record) => [`${record.frameId}:${record.roiId}`, { ...record.result }]));
  }

  async recognize(input: RecognizeRequest): Promise<OcrRecognitionResult> {
    const result = this.records.get(`${input.frame.frameId}:${input.roiId}`);
    if (!result) {
      return {
        method: this.id,
        rawText: '',
        confidence: 0,
        durationMs: 0,
        warning: 'No recorded OCR result for frame and ROI',
        error: 'RECORDED_RESULT_NOT_FOUND',
      };
    }
    return { ...result };
  }
}

function validateFrame(frame: RuntimeFramePacket): void {
  if (!frame.frameId || !frame.runId || !frame.observedAt) throw new Error('FramePacket identity/time is incomplete');
  if (!Number.isInteger(frame.sequence) || frame.sequence < 0) throw new Error('FramePacket sequence is invalid');
  if (!Number.isFinite(frame.monotonicNs) || frame.monotonicNs < 0) throw new Error('FramePacket monotonicNs is invalid');
  if (frame.media.width < 1 || frame.media.height < 1) throw new Error('FramePacket media dimensions are invalid');
}

function eventId(): string {
  return globalThis.crypto.randomUUID();
}

function eventTime(frame: RuntimeFramePacket): JsonObject {
  return {
    observed_at: frame.observedAt,
    emitted_at: new Date().toISOString(),
    source_timestamp: frame.sourceTimestamp ?? null,
    monotonic_ns: frame.monotonicNs,
    clock: { domain: 'recorded-frame', sync_status: 'unknown', uncertainty_ms: null },
  };
}

function recognitionPayload(config: NumberOCRConfig, recognition: OcrRecognitionResult): JsonObject {
  return {
    roi_id: config.roiId,
    roi: config.roi as unknown as JsonObject,
    name: config.name,
    symbol: config.symbol,
    raw_text: recognition.rawText,
    normalized_text: normalizeOcrText(recognition.rawText),
    confidence: recognition.confidence,
    duration_ms: recognition.durationMs,
    warning: recognition.warning ?? null,
    recognition_error: recognition.error ?? null,
    recognizer: recognition.method,
    recognizer_details: recognition.details ?? null,
  };
}

function errorEvent(
  frame: RuntimeFramePacket,
  config: NumberOCRConfig,
  instanceId: string,
  sequence: number,
  recognition: OcrRecognitionResult,
  code: string,
  message: string,
  flags: string[],
): JsonObject {
  return {
    schema_version: '1.0.0',
    event_id: eventId(),
    run_id: frame.runId,
    sensor: { id: 'ocr.number', instance_id: instanceId, version: '0.2.0', category: 'processor' },
    sequence,
    time: eventTime(frame),
    status: 'error',
    quality: {
      confidence: recognition.confidence,
      latency_ms: recognition.durationMs,
      flags,
      dropped_since_last: frame.droppedSinceLast ?? 0,
    },
    measurements: [],
    parent_event_ids: [frame.frameId],
    payload: recognitionPayload(config, recognition),
    error: { code, message, retryable: true, cause: recognition.error ?? null },
  };
}

export class NumberOCRSensor implements ProcessorSensor {
  private state: LifecycleState = 'created';
  private context: SensorContext | null = null;
  private config: NumberOCRConfig | null = null;
  private sequence = 0;
  private processedCount = 0;
  private errorCount = 0;
  private lastLatencyMs: number | undefined;

  constructor(
    private readonly recognizer: NumberRecognizer,
    private readonly instanceId = 'number-ocr-01',
  ) {}

  describe(): SensorDescriptor {
    return {
      sensorId: 'ocr.number',
      version: '0.2.0',
      category: 'processor',
      inputKinds: ['frame-packet.screen-frame', 'frame-packet.image-frame'],
      outputKinds: ['sensor-event.measurement'],
      capabilities: [
        'rgba-pixel-input',
        'normalized-ocr-roi',
        'image-preprocessing',
        'tesseract-js',
        'numeric-parsing',
        'quality-metadata',
        'recorded-result-replay',
      ],
      configSchemaVersion: '1.0.0',
      evidenceLevel: 'replay-benchmarked',
    };
  }

  configure(config: JsonObject): ConfigResult {
    if (this.state === 'running') throw new Error('stop the sensor before reconfiguring it');
    const allowed = new Set(['roiId', 'roi', 'name', 'symbol', 'unit']);
    const unknown = Object.keys(config).filter((key) => !allowed.has(key));
    if (unknown.length > 0) throw new Error(`unknown Number OCR settings: ${unknown.sort().join(', ')}`);
    if (typeof config.roi !== 'object' || config.roi === null || Array.isArray(config.roi)) {
      throw new Error('roi must be an object with x, y, width, and height');
    }
    const roi = config.roi as unknown as Rect;
    validateNormalizedRect(roi);
    const roiId = String(config.roiId ?? '');
    if (!roiId) throw new Error('roiId is required');
    this.config = {
      roiId,
      roi: { ...roi },
      name: String(config.name ?? roiId),
      symbol: String(config.symbol ?? roiId),
      unit: String(config.unit ?? '1'),
    };
    this.state = 'configured';
    return {
      accepted: true,
      effectiveConfig: {
        roiId: this.config.roiId,
        roi: this.config.roi as unknown as JsonObject,
        name: this.config.name,
        symbol: this.config.symbol,
        unit: this.config.unit,
      },
      warnings: this.recognizer.replay ? ['recorded-result replay; no OCR inference is performed'] : [],
    };
  }

  async start(context: SensorContext): Promise<void> {
    if (!this.config) throw new Error('configure the sensor before starting it');
    this.context = context;
    this.sequence = 0;
    this.processedCount = 0;
    this.errorCount = 0;
    this.state = 'running';
  }

  async processFrame(frame: RuntimeFramePacket): Promise<JsonObject> {
    if (this.state !== 'running' || !this.context || !this.config) throw new Error('sensor must be running');
    validateFrame(frame);
    if (frame.runId !== this.context.runId) throw new Error('FramePacket runId does not match SensorContext runId');
    const recognition = await this.recognizer.recognize({ frame, roiId: this.config.roiId, roi: this.config.roi });
    this.processedCount += 1;
    this.lastLatencyMs = recognition.durationMs;
    const replayFlags = this.recognizer.replay ? ['recorded-replay'] : [];

    if (recognition.error) {
      this.errorCount += 1;
      const event = errorEvent(
        frame,
        this.config,
        this.instanceId,
        this.sequence,
        recognition,
        'OCR_RECOGNITION_FAILED',
        recognition.warning ?? recognition.error,
        [...replayFlags, 'ocr-recognition-failed'],
      );
      this.sequence += 1;
      return event;
    }

    const value = extractNumberFromText(recognition.rawText);
    if (value === null) {
      this.errorCount += 1;
      const event = errorEvent(
        frame,
        this.config,
        this.instanceId,
        this.sequence,
        recognition,
        'OCR_PARSE_FAILED',
        recognition.warning ?? `${this.config.name} OCR rawText contains no ordinary decimal number`,
        [...replayFlags, 'ocr-parse-failed'],
      );
      this.sequence += 1;
      return event;
    }

    const status = recognition.warning ? 'degraded' : 'ok';
    const flags = recognition.warning ? [...replayFlags, 'ocr-warning'] : replayFlags;
    const event: JsonObject = {
      schema_version: '1.0.0',
      event_id: eventId(),
      run_id: frame.runId,
      sensor: { id: 'ocr.number', instance_id: this.instanceId, version: '0.2.0', category: 'processor' },
      sequence: this.sequence,
      time: eventTime(frame),
      status,
      quality: {
        confidence: recognition.confidence,
        latency_ms: recognition.durationMs,
        flags,
        dropped_since_last: frame.droppedSinceLast ?? 0,
      },
      measurements: [
        {
          name: 'recognized_value',
          value,
          value_type: 'number',
          unit: this.config.unit,
          role: 'derived',
          uncertainty: null,
        },
      ],
      parent_event_ids: [frame.frameId],
      payload: recognitionPayload(this.config, recognition),
    };
    this.sequence += 1;
    return event;
  }

  async *process(frame: RuntimeFramePacket): AsyncIterable<JsonObject> {
    yield await this.processFrame(frame);
  }

  health(): HealthSnapshot {
    return {
      state: this.state,
      processedCount: this.processedCount,
      droppedCount: 0,
      lostCount: 0,
      errorCount: this.errorCount,
      latencyMs: this.lastLatencyMs === undefined ? {} : { last: this.lastLatencyMs },
    };
  }

  async stop(): Promise<void> {
    if (this.state === 'stopped') return;
    this.state = 'stopping';
    await this.recognizer.close?.();
    this.context = null;
    this.state = 'stopped';
  }
}
