import type {
  GasSimulationSnapshot,
  SimulationMode,
  ExperimentDataPoint,
} from '../core/types.js';
import { validateTemperature } from '../physics/maxwellBoltzmann.js';
import { GasSimulationEngine } from '../simulation/engine.js';

export interface DriverTickMetadata {
  mode: SimulationMode;
  currentTemperatureK: number;
  currentPressureKPa?: number;
  replayIndex?: number;
  replayTimeSeconds?: number;
  replayProgress?: number; // 0.0 to 1.0
}

export type TickListener = (snapshot: GasSimulationSnapshot, meta: DriverTickMetadata) => void;

export class GasSimulationDriver {
  private readonly engine: GasSimulationEngine;
  private mode: SimulationMode = 'manual';
  private replayData: ExperimentDataPoint[] = [];
  private replayPlaybackSpeed = 1.0;
  private replayCurrentTime = 0;
  private replayCurrentIndex = 0;
  private replayPaused = false;
  private liveTemperatureK: number;
  private livePressureKPa?: number;
  private readonly listeners: Set<TickListener> = new Set();

  constructor(engine: GasSimulationEngine, initialMode: SimulationMode = 'manual') {
    this.engine = engine;
    this.liveTemperatureK = engine.getTemperature();
    this.setMode(initialMode);
  }

  public getMode(): SimulationMode {
    return this.mode;
  }

  public setMode(mode: SimulationMode): void {
    if (!['manual', 'live', 'replay'].includes(mode)) throw new RangeError('Unknown simulation mode');
    this.mode = mode;
    if (mode === 'live') {
      this.engine.setTemperature(this.liveTemperatureK);
    } else if (mode === 'replay' && this.replayData.length > 0) {
      const point = this.replayData[this.replayCurrentIndex];
      if (point) {
        this.engine.setTemperature(point.temperatureK);
      }
    }
  }

  public getEngine(): GasSimulationEngine {
    return this.engine;
  }

  public updateLiveReading(temperatureK: number, pressureKPa?: number): void {
    validateTemperature(temperatureK);
    if (pressureKPa !== undefined && !Number.isFinite(pressureKPa)) throw new RangeError('Pressure must be finite kPa');
    this.liveTemperatureK = temperatureK;
    this.livePressureKPa = pressureKPa;
    if (this.mode === 'live') {
      this.engine.setTemperature(temperatureK);
    }
  }

  public setManualTemperature(temperatureK: number): void {
    validateTemperature(temperatureK);
    if (this.mode === 'manual') {
      this.engine.setTemperature(temperatureK);
    }
  }

  public loadReplayData(data: ReadonlyArray<ExperimentDataPoint>): void {
    for (let i = 0; i < data.length; i++) {
      const point = data[i]!;
      validateTemperature(point.temperatureK);
      if (!Number.isFinite(point.timestamp) || (i > 0 && point.timestamp <= data[i - 1]!.timestamp)
        || [point.pressureKPa, point.realSensorPressure].some(p => p !== undefined && !Number.isFinite(p))) {
        throw new RangeError('Replay requires finite seconds, strictly increasing timestamps and finite pressures');
      }
    }
    this.replayData = data.map(p => ({ ...p }));
    this.replayCurrentIndex = 0;
    this.replayCurrentTime = this.replayData[0]?.timestamp ?? 0;
    if (this.mode === 'replay' && this.replayData.length > 0) {
      const p = this.replayData[0]!;
      this.engine.setTemperature(p.temperatureK);
    }
  }

  public setReplayPlaybackSpeed(speed: number): void {
    if (!Number.isFinite(speed) || speed <= 0) throw new RangeError('Playback speed must be finite and positive');
    this.replayPlaybackSpeed = speed;
  }

  public seekReplayIndex(index: number): void {
    if (!Number.isInteger(index)) throw new RangeError('Replay index must be an integer');
    if (this.replayData.length === 0) return;
    const clampedIndex = Math.max(0, Math.min(this.replayData.length - 1, index));
    this.replayCurrentIndex = clampedIndex;
    const point = this.replayData[clampedIndex]!;
    this.replayCurrentTime = point.timestamp;
    if (this.mode === 'replay') this.engine.setTemperature(point.temperatureK);
  }

  public setReplayPaused(paused: boolean): void {
    this.replayPaused = paused;
  }

  public subscribe(listener: TickListener): () => void {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  }

  /**
   * Advances the simulation by dtSeconds and notifies subscribers.
   */
  public tick(dtSeconds: number): GasSimulationSnapshot {
    if (!Number.isFinite(dtSeconds) || dtSeconds < 0) throw new RangeError('Tick duration must be finite and nonnegative seconds');
    let snapshot: GasSimulationSnapshot | undefined;
    let currentTemp = this.engine.getTemperature();
    let currentPressure: number | undefined;

    if (this.mode === 'live') {
      currentTemp = this.liveTemperatureK;
      currentPressure = this.livePressureKPa;
      this.engine.setTemperature(currentTemp);
    } else if (this.mode === 'replay' && this.replayData.length > 0) {
      const targetTime = this.replayCurrentTime + (this.replayPaused ? 0 : dtSeconds * this.replayPlaybackSpeed);
      if (!Number.isFinite(targetTime)) throw new RangeError('Replay time overflow');
      // Piecewise-constant readings: apply each input at its recorded timestamp.
      while (this.replayCurrentIndex < this.replayData.length - 1
        && this.replayData[this.replayCurrentIndex + 1]!.timestamp <= targetTime) {
        const boundary = this.replayData[this.replayCurrentIndex + 1]!.timestamp;
        this.engine.setTemperature(this.replayData[this.replayCurrentIndex]!.temperatureK);
        snapshot = this.engine.step(boundary - this.replayCurrentTime);
        this.replayCurrentTime = boundary;
        this.replayCurrentIndex++;
      }
      this.engine.setTemperature(this.replayData[this.replayCurrentIndex]!.temperatureK);
      snapshot = this.engine.step(targetTime - this.replayCurrentTime);
      this.replayCurrentTime = targetTime;
      const point = this.replayData[this.replayCurrentIndex]!;
      currentTemp = point.temperatureK;
      currentPressure = point.pressureKPa ?? point.realSensorPressure;
      this.engine.setTemperature(currentTemp);
    }

    snapshot ??= this.engine.step(dtSeconds);

    const meta: DriverTickMetadata = {
      mode: this.mode,
      currentTemperatureK: currentTemp,
      currentPressureKPa: currentPressure,
    };

    if (this.mode === 'replay' && this.replayData.length > 0) {
      meta.replayIndex = this.replayCurrentIndex;
      meta.replayTimeSeconds = this.replayCurrentTime;
      meta.replayProgress = this.replayCurrentIndex / Math.max(1, this.replayData.length - 1);
    }

    for (const listener of this.listeners) {
      listener(snapshot, meta);
    }

    return snapshot;
  }
}
