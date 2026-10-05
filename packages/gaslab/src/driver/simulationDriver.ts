import type {
  GasSimulationSnapshot,
  SimulationMode,
  ExperimentDataPoint,
} from '../core/types.js';
import { GasSimulationEngine } from '../simulation/engine.js';

export interface DriverTickMetadata {
  mode: SimulationMode;
  currentTemperatureK: number;
  currentPressureKPa?: number;
  replayIndex?: number;
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
  private liveTemperatureK: number;
  private livePressureKPa?: number;
  private readonly listeners: Set<TickListener> = new Set();

  constructor(engine: GasSimulationEngine, initialMode: SimulationMode = 'manual') {
    this.engine = engine;
    this.mode = initialMode;
    this.liveTemperatureK = engine.getTemperature();
  }

  public getMode(): SimulationMode {
    return this.mode;
  }

  public setMode(mode: SimulationMode): void {
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
    this.liveTemperatureK = temperatureK;
    this.livePressureKPa = pressureKPa;
    if (this.mode === 'live') {
      this.engine.setTemperature(temperatureK);
    }
  }

  public setManualTemperature(temperatureK: number): void {
    if (this.mode === 'manual') {
      this.engine.setTemperature(temperatureK);
    }
  }

  public loadReplayData(data: ReadonlyArray<ExperimentDataPoint>): void {
    this.replayData = [...data];
    this.replayCurrentIndex = 0;
    this.replayCurrentTime = 0;
    if (this.mode === 'replay' && this.replayData.length > 0) {
      const p = this.replayData[0]!;
      this.engine.setTemperature(p.temperatureK);
    }
  }

  public setReplayPlaybackSpeed(speed: number): void {
    this.replayPlaybackSpeed = Math.max(0.1, Math.min(10.0, speed));
  }

  public seekReplayIndex(index: number): void {
    if (this.replayData.length === 0) return;
    const clampedIndex = Math.max(0, Math.min(this.replayData.length - 1, index));
    this.replayCurrentIndex = clampedIndex;
    const point = this.replayData[clampedIndex]!;
    this.replayCurrentTime = point.timestamp;
    this.engine.setTemperature(point.temperatureK);
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
    let currentTemp = this.engine.getTemperature();
    let currentPressure: number | undefined;

    if (this.mode === 'live') {
      currentTemp = this.liveTemperatureK;
      currentPressure = this.livePressureKPa;
      this.engine.setTemperature(currentTemp);
    } else if (this.mode === 'replay' && this.replayData.length > 0) {
      this.replayCurrentTime += dtSeconds * this.replayPlaybackSpeed;
      // Advance replay index
      while (
        this.replayCurrentIndex < this.replayData.length - 1 &&
        this.replayData[this.replayCurrentIndex + 1]!.timestamp <= this.replayCurrentTime
      ) {
        this.replayCurrentIndex++;
      }
      const point = this.replayData[this.replayCurrentIndex]!;
      currentTemp = point.temperatureK;
      currentPressure = point.pressureKPa ?? point.realSensorPressure;
      this.engine.setTemperature(currentTemp);
    }

    const snapshot = this.engine.step(dtSeconds);

    const meta: DriverTickMetadata = {
      mode: this.mode,
      currentTemperatureK: currentTemp,
      currentPressureKPa: currentPressure,
    };

    if (this.mode === 'replay' && this.replayData.length > 0) {
      meta.replayIndex = this.replayCurrentIndex;
      meta.replayProgress = this.replayCurrentIndex / Math.max(1, this.replayData.length - 1);
    }

    for (const listener of this.listeners) {
      listener(snapshot, meta);
    }

    return snapshot;
  }
}
