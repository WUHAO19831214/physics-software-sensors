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
  private status: StabilizerStatus = 'uninitialized';

  constructor(options: StabilizerOptions = {}) {
    this.options = {
      maxHoldingDurationMs: options.maxHoldingDurationMs ?? 3000,
      confidenceDecayRate: options.confidenceDecayRate ?? 0.95,
      minHoldingConfidence: options.minHoldingConfidence ?? 0.2,
      maxAllowedSpikeRatio: options.maxAllowedSpikeRatio ?? Infinity,
    };
  }

  public update(input: {
    value: T | null;
    confidence?: number;
    timestamp?: number;
    isValid?: boolean;
  }): StabilizedSample<T> {
    const now = input.timestamp ?? Date.now();
    const flags: string[] = [];
    const hasValue = input.value !== null && input.value !== undefined;
    const isValid = input.isValid !== undefined ? input.isValid : hasValue;

    if (isValid && hasValue) {
      // Check spike rejection if numeric
      let isSpike = false;
      if (
        typeof input.value === 'number' &&
        typeof this.lastValidValue === 'number' &&
        Number.isFinite(this.options.maxAllowedSpikeRatio) &&
        this.options.maxAllowedSpikeRatio > 0 &&
        this.lastValidValue !== 0
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
        this.currentConfidence = Math.max(
          this.options.minHoldingConfidence,
          this.currentConfidence * this.options.confidenceDecayRate,
        );
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
