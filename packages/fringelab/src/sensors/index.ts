import type { ConfigResult, HealthSnapshot, JsonObject, RuntimeFramePacket, SensorContext, SensorDescriptor } from '@physics-software-sensors/core';
import { extractStripProfile, type ExtractStripProfileOptions } from '../core/signal.js';
import { detectPhysicalRuler } from '../core/ruler-detection.js';

type SensorOptions = ExtractStripProfileOptions & Partial<Omit<Parameters<typeof detectPhysicalRuler>[1], 'sourceType'>>;
abstract class FrameProcessor {
  private state: HealthSnapshot['state'] = 'created';
  private processedCount = 0;
  private lostCount = 0;
  private errorCount = 0;
  private lastLatency = 0;
  private sequence = 0;
  private context: SensorContext | null = null;
  protected options: SensorOptions = {};
  private readonly instanceId = globalThis.crypto.randomUUID();
  abstract readonly sensorId: string;
  protected abstract observe(frame: RuntimeFramePacket): { measurements: object[]; payload: object; flags: string[]; confidence?: number; status: 'ok' | 'degraded' | 'lost' };
  describe(): SensorDescriptor { return { sensorId: this.sensorId, version: '0.1.0', category: 'processor', inputKinds: ['frame-packet.image-frame', 'frame-packet.camera-frame', 'frame-packet.screen-frame'], outputKinds: ['sensor-event.measurement'], capabilities: ['rgba-pixel-input', 'source-frame-provenance'], configSchemaVersion: '1.0.0', evidenceLevel: 'source-tested' }; }
  configure(config: JsonObject): ConfigResult {
    if (this.state === 'running') return { accepted: false, effectiveConfig: {}, warnings: ['Stop before reconfiguring'] };
    const allowed = this.sensorId === 'image.strip-profile' ? ['channel', 'roi', 'fringeOrientation', 'saturationThreshold', 'maxAutoSaturationRate', 'minAutoContrast'] : ['region', 'contrastMode', 'tickSnapEnabled', 'numberSnapEnabled', 'manualOriginMm'];
    if (Object.keys(config).some(key => !allowed.includes(key))) return { accepted: false, effectiveConfig: {}, warnings: ['Unsupported configuration field'] };
    const channel = config.channel;
    if (channel != null && !['r', 'g', 'b', 'luminance', 'auto'].includes(String(channel))) return { accepted: false, effectiveConfig: {}, warnings: ['Invalid channel'] };
    const validObject = (value: unknown, fields: string[]) => value != null && typeof value === 'object' && fields.every(key => typeof (value as Record<string, unknown>)[key] === 'number' && Number.isFinite((value as Record<string, number>)[key]));
    if (config.fringeOrientation != null && !['vertical', 'horizontal'].includes(String(config.fringeOrientation))) return { accepted: false, effectiveConfig: {}, warnings: ['Invalid fringe orientation'] };
    if (config.roi != null && (!validObject(config.roi, ['centerX', 'centerY', 'width', 'height']) || Number((config.roi as JsonObject).width) <= 0 || Number((config.roi as JsonObject).height) <= 0 || !Number.isFinite(Number((config.roi as JsonObject).angleDeg ?? 0)))) return { accepted: false, effectiveConfig: {}, warnings: ['Finite ROI with positive size required'] };
    if (config.region != null && (!validObject(config.region, ['x', 'y', 'width', 'height']) || Number((config.region as JsonObject).width) <= 0 || Number((config.region as JsonObject).height) <= 0)) return { accepted: false, effectiveConfig: {}, warnings: ['Finite ruler region with positive size required'] };
    for (const key of ['saturationThreshold', 'maxAutoSaturationRate', 'minAutoContrast']) if (config[key] != null && (typeof config[key] !== 'number' || !Number.isFinite(config[key]) || Number(config[key]) < 0)) return { accepted: false, effectiveConfig: {}, warnings: [`Invalid ${key}`] };
    if (config.contrastMode != null && !['auto', 'light-on-dark', 'dark-on-light', 'cyan', 'magenta'].includes(String(config.contrastMode))) return { accepted: false, effectiveConfig: {}, warnings: ['Invalid ruler contrast mode'] };
    for (const key of ['tickSnapEnabled', 'numberSnapEnabled']) if (config[key] != null && typeof config[key] !== 'boolean') return { accepted: false, effectiveConfig: {}, warnings: [`Invalid ${key}`] };
    if (config.manualOriginMm != null && (typeof config.manualOriginMm !== 'number' || !Number.isFinite(config.manualOriginMm))) return { accepted: false, effectiveConfig: {}, warnings: ['Finite manual ruler origin required'] };
    this.options = structuredClone(config) as SensorOptions; this.state = 'configured';
    return { accepted: true, effectiveConfig: structuredClone(config), warnings: [] };
  }
  async start(context: SensorContext) { if (!context.runId || context.cancellation?.aborted) throw new RangeError('Active runId/context required'); if (this.state === 'running') throw new Error('Already running'); this.context = context; this.state = 'running'; this.sequence = 0; this.processedCount = 0; this.lostCount = 0; this.errorCount = 0; }
  health(): HealthSnapshot { return { state: this.state, processedCount: this.processedCount, lostCount: this.lostCount, droppedCount: 0, errorCount: this.errorCount, latencyMs: { last: this.lastLatency } }; }
  async stop() { this.context = null; this.state = 'stopped'; }
  async *process(frame: RuntimeFramePacket): AsyncIterable<JsonObject> {
    if (this.state !== 'running' || !this.context) throw new Error('Sensor is not running');
    if (this.context.cancellation?.aborted) return;
    if (frame.runId !== this.context.runId) throw new RangeError('Frame runId does not match sensor run');
    const started = performance.now();
    let result: ReturnType<FrameProcessor['observe']>;
    let error: object | undefined;
    try {
      if (!frame.pixels || frame.pixels.width !== frame.media.width || frame.pixels.height !== frame.media.height || frame.pixels.data.length !== frame.media.width * frame.media.height * 4 || frame.media.colorSpace.toLowerCase() !== 'rgba') throw new RangeError('Matching RGBA pixels required');
      result = this.observe(frame); this.processedCount++;
      if (result.status === 'lost') this.lostCount++;
    } catch (cause) {
      this.errorCount++;
      result = { status: 'lost', measurements: [], payload: {}, flags: [] };
      error = { code: 'INVALID_FRAME_OR_CONFIG', message: cause instanceof Error ? cause.message : String(cause), retryable: true };
    }
    this.lastLatency = performance.now() - started;
    const event = {
      schema_version: '1.0.0', event_id: crypto.randomUUID(), run_id: this.context.runId,
      sensor: { id: this.sensorId, instance_id: this.instanceId, version: '0.1.0', category: 'processor' }, sequence: this.sequence++,
      time: { observed_at: frame.observedAt, emitted_at: new Date().toISOString(), monotonic_ns: frame.monotonicNs, source_timestamp: frame.sourceTimestamp ?? null, clock: { domain: frame.sourceSensorId, sync_status: 'single-clock' } },
      status: error ? 'error' : result.status,
      quality: { flags: [...new Set([...(frame.qualityFlags ?? []), ...result.flags])], confidence: result.confidence ?? null, latency_ms: this.lastLatency, dropped_since_last: frame.droppedSinceLast ?? 0 },
      measurements: result.measurements,
      coordinate_frame: { id: frame.frameId, space: 'image-pixel', origin: 'top-left', x_direction: 'right', y_direction: 'down', unit: 'px', width: frame.media.width, height: frame.media.height },
      payload: { input_frame_id: frame.frameId, input_artifact_uri: frame.artifactUri, ...result.payload }, ...(error ? { error } : {}),
    };
    yield event as unknown as JsonObject;
  }
}

export class StripProfileSensor extends FrameProcessor {
  readonly sensorId = 'image.strip-profile';
  protected observe(frame: RuntimeFramePacket) {
    const p = extractStripProfile(frame.pixels!, this.options);
    const coverage = p.samplesPerBin.reduce((a, b) => a + b, 0);
    const flags = ['relative-camera-response'];
    if (!coverage) return { status: 'lost' as const, measurements: [], payload: { profile: [] }, flags: ['no-valid-samples'] };
    if (p.samplesPerBin.some(n => !n)) flags.push('partial-roi-coverage');
    if (p.saturationRates[p.selectedChannel] > 0) flags.push('source-clipping');
    return {
      status: flags.length > 1 ? 'degraded' as const : 'ok' as const,
      measurements: [{ name: 'sample_count', value: p.profile.length, value_type: 'integer', unit: 'sample', role: 'raw' }, { name: 'saturation_fraction', value: p.saturationRates[p.selectedChannel], value_type: 'number', unit: '1', role: 'derived' }],
      payload: { response_unit: 'DN', profile: Array.from(p.profile), axis_positions_px: Array.from(p.axisPositionsPx), axis_origin: 'roi-center', samples_per_bin: Array.from(p.samplesPerBin), selected_channel: p.selectedChannel, channel_reason: p.channelReason, roi: this.options.roi ?? null, profiles: Object.fromEntries(Object.entries(p.profiles).map(([k, a]) => [k, Array.from(a)])), saturation_by_channel: p.saturationRates }, flags,
    };
  }
}
export class RulerTicksSensor extends FrameProcessor {
  readonly sensorId = 'vision.ruler-ticks';
  protected observe(frame: RuntimeFramePacket) {
    const { region, contrastMode, tickSnapEnabled, numberSnapEnabled, manualOriginMm } = this.options;
    const r = detectPhysicalRuler(frame.pixels!, { sourceType: frame.media.kind === 'camera-frame' ? 'camera' : 'image', region, contrastMode, tickSnapEnabled, numberSnapEnabled, manualOriginMm });
    if (!r) return { status: 'lost' as const, measurements: [], payload: { candidate: null }, flags: ['ruler-not-found'] };
    return { status: 'degraded' as const, measurements: [{ name: 'tick_count', value: r.ticks.length, value_type: 'integer', unit: 'tick', role: 'raw' }], payload: { candidate: r, confirmed: false, scale_assumption: 'minor-tick-1-mm', calibration_applied: false }, flags: ['candidate-unconfirmed', ...(r.perspectiveWarning ? ['perspective-variation'] : [])], confidence: r.fit.confidence };
  }
}
