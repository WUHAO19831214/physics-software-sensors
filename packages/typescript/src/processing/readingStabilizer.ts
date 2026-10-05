/**
 * Streaming reading stabilizer for physical sensors and continuous OCR feeds.
 * Provides holding-state persistence, confidence decay, spike rejection, and staleness detection.
 */

export type StabilizerStatus = 'uninitialized' | 'valid' | 'holding' | 'stale';

export interface StabilizerOptions {
  /** Maximum duration in ms to hold the last valid reading before transitioning to 'stale' (default: 3000ms). */
  maxHoldingDurationMs?: number;
  /** Multiplicative decay factor applied to confidence during holding intervals (default: 0.95). */
  confidenceDecayRate?: number;
  /** Lower bound for decayed confidence during prolonged holding (default: 0.2). */
  minHoldingConfidence?: number;
  /**
   * If specified for numeric values, rejects changes exceeding this ratio of the current value
   * in a single frame as spurious spikes.
   */
  maxAllowedSpikeRatio?: number;
}

export interface StabilizedSample<T> {
  value: T | null;
  status: StabilizerStatus;
  confidence: number;
  isFresh: boolean;
  lastValidTimestamp: number | null;
  flags: string[];
}

export class ReadingStabilizer<T = number> {
  private readonly options: Required<StabilizerOptions>;
  private lastValidValue: T | null = null;
  private lastValidTimestamp: number | null = null;
  private currentConfidence = 0;
  private lastUpdateTimestamp: number | null = null;
  private status: StabilizerStatus = 'uninitialized';

  constructor(options: StabilizerOptions = {}) {
    this.options = {
      maxHoldingDurationMs: options.maxHoldingDurationMs ?? 3000,
      confidenceDecayRate: options.confidenceDecayRate ?? 0.95,
      minHoldingConfidence: options.minHoldingConfidence ?? 0.2,
      maxAllowedSpikeRatio: options.maxAllowedSpikeRatio ?? Infinity,
    };
    if (!Number.isFinite(this.options.maxHoldingDurationMs) || this.options.maxHoldingDurationMs < 0
      || !Number.isFinite(this.options.confidenceDecayRate) || this.options.confidenceDecayRate < 0 || this.options.confidenceDecayRate > 1
      || !Number.isFinite(this.options.minHoldingConfidence) || this.options.minHoldingConfidence < 0 || this.options.minHoldingConfidence > 1
      || this.options.maxAllowedSpikeRatio < 0 || Number.isNaN(this.options.maxAllowedSpikeRatio)) {
      throw new RangeError('Invalid stabilizer options');
    }
  }

  public update(input: {
    value: T | null;
    confidence?: number;
    timestamp?: number;
    isValid?: boolean;
  }): StabilizedSample<T> {
    const now = input.timestamp ?? Date.now();
    if (!Number.isFinite(now)) throw new RangeError('timestamp must be finite milliseconds');
    const flags: string[] = [];
    if (this.lastUpdateTimestamp !== null && now < this.lastUpdateTimestamp) {
      return { ...this.getCurrent(), flags: ['out-of-order'] };
    }
    this.lastUpdateTimestamp = now;
    const hasValue = input.value !== null && input.value !== undefined
      && (typeof input.value !== 'number' || Number.isFinite(input.value))
      && (input.confidence === undefined || Number.isFinite(input.confidence));
    const isValid = input.isValid !== undefined ? input.isValid : hasValue;

    if (isValid && hasValue) {
      // Check spike rejection if numeric
      let isSpike = false;
      if (
        typeof input.value === 'number' &&
        typeof this.lastValidValue === 'number' &&
        Number.isFinite(this.options.maxAllowedSpikeRatio) &&
        this.options.maxAllowedSpikeRatio > 0 &&
        this.lastValidValue !== 0 &&
        this.lastValidTimestamp !== null &&
        now - this.lastValidTimestamp <= this.options.maxHoldingDurationMs
      ) {
        const deltaRatio = Math.abs(input.value - this.lastValidValue) / Math.abs(this.lastValidValue);
        if (deltaRatio > this.options.maxAllowedSpikeRatio) {
          isSpike = true;
          flags.push('spike-rejected');
        }
      }

      if (!isSpike) {
        this.lastValidValue = input.value;
        this.lastValidTimestamp = now;
        this.currentConfidence = input.confidence !== undefined
          ? Math.max(0, Math.min(1, input.confidence))
          : 0.9;
        this.status = 'valid';

        return {
          value: this.lastValidValue,
          status: 'valid',
          confidence: this.currentConfidence,
          isFresh: true,
          lastValidTimestamp: this.lastValidTimestamp,
          flags,
        };
      }
    }

    // Holding or Stale fallback
    if (this.lastValidValue !== null && this.lastValidTimestamp !== null) {
      const elapsed = now - this.lastValidTimestamp;
      if (elapsed > this.options.maxHoldingDurationMs) {
        this.status = 'stale';
        this.currentConfidence = 0;
        flags.push('timeout-stale');
      } else {
        this.status = 'holding';
        this.currentConfidence = Math.min(this.currentConfidence, Math.max(
          this.options.minHoldingConfidence,
          this.currentConfidence * this.options.confidenceDecayRate,
        ));
        flags.push('value-holding');
      }

      return {
        value: this.lastValidValue,
        status: this.status,
        confidence: Number(this.currentConfidence.toFixed(3)),
        isFresh: false,
        lastValidTimestamp: this.lastValidTimestamp,
        flags,
      };
    }

    this.status = 'uninitialized';
    return {
      value: null,
      status: 'uninitialized',
      confidence: 0,
      isFresh: false,
      lastValidTimestamp: null,
      flags: ['uninitialized'],
    };
  }

  public reset(): void {
    this.lastValidValue = null;
    this.lastValidTimestamp = null;
    this.currentConfidence = 0;
    this.status = 'uninitialized';
    this.lastUpdateTimestamp = null;
  }

  public getCurrent(): StabilizedSample<T> {
    return {
      value: this.lastValidValue,
      status: this.status,
      confidence: Number(this.currentConfidence.toFixed(3)),
      isFresh: false,
      lastValidTimestamp: this.lastValidTimestamp,
      flags: [],
    };
  }
}
