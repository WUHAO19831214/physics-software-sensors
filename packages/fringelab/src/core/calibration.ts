import { calculateMmPerPixel, type RulerCalibration } from './ruler.js';
import { mapScreenPointMm, validateSpatialAnchors, type SpatialAnchor } from './spatial.js';
import type { Point } from './roi.js';

export type CalibrationState = { id: string; sourceKey: string; confirmed: true; method: 'two-point' | 'multi-point'; anchors: SpatialAnchor[]; ruler?: RulerCalibration };

/** Owner-confirmed calibration, separate from automatic ruler candidates. */
export function confirmTwoPointCalibration(ruler: RulerCalibration, sourceKey: string, id: string): CalibrationState {
  if (!sourceKey || !id || !Number.isFinite(ruler.originMm ?? 0) || calculateMmPerPixel(ruler) == null) throw new RangeError('Invalid confirmed calibration');
  return { id, sourceKey, confirmed: true, method: 'two-point', anchors: [], ruler: structuredClone(ruler) };
}
export function confirmMultiPointCalibration(anchors: readonly SpatialAnchor[], sourceKey: string, id: string): CalibrationState {
  const validity = validateSpatialAnchors(anchors);
  if (!sourceKey || !id || !validity.valid) throw new RangeError(validity.reason || 'Calibration identity required');
  return { id, sourceKey, confirmed: true, method: 'multi-point', anchors: structuredClone([...anchors]) };
}
export function calibratedPosition(point: Point, calibration: CalibrationState | null, sourceKey: string) {
  if (!calibration || !calibration.confirmed || calibration.sourceKey !== sourceKey) return { status: 'stale' as const, valueMm: null, extrapolated: false };
  if (![point.x, point.y].every(Number.isFinite)) throw new RangeError('Invalid point');
  if (calibration.method === 'multi-point') {
    const validity = validateSpatialAnchors(calibration.anchors);
    if (!validity.valid) throw new RangeError(validity.reason);
    const valueMm = mapScreenPointMm(point, calibration.anchors);
    const limits = calibration.anchors.map(p => p.mm);
    const extrapolated = valueMm < Math.min(...limits) || valueMm > Math.max(...limits);
    return { status: extrapolated ? 'provisional' as const : 'valid' as const, valueMm, extrapolated };
  }
  const ruler = calibration.ruler!;
  const scale = calculateMmPerPixel(ruler);
  if (scale == null) throw new RangeError('Invalid ruler');
  const dx = ruler.end.x - ruler.start.x, dy = ruler.end.y - ruler.start.y;
  const q = ((point.x - ruler.start.x) * dx + (point.y - ruler.start.y) * dy) / Math.hypot(dx, dy);
  const extrapolated = q < 0 || q > Math.hypot(dx, dy);
  return { status: extrapolated ? 'provisional' as const : 'valid' as const, valueMm: (ruler.originMm ?? 0) + q * scale, extrapolated };
}

export class MeasurementSession {
  private revision = 0;
  private _calibration: CalibrationState | null = null;
  constructor(public sourceKey: string) {}
  get calibration() { return this._calibration ? structuredClone(this._calibration) : null; }
  get calculationKey() { return `${this.sourceKey}:${this.revision}:${this._calibration?.id ?? 'uncalibrated'}`; }
  apply(calibration: CalibrationState) {
    if (calibration.sourceKey !== this.sourceKey) throw new RangeError('Calibration belongs to another image');
    this._calibration = structuredClone(calibration); this.revision++;
  }
  changeSource(sourceKey: string) { this.sourceKey = sourceKey; this._calibration = null; this.revision++; }
  invalidateProcessing() { this.revision++; }
  isCurrent(key: string) { return key === this.calculationKey; }
}
