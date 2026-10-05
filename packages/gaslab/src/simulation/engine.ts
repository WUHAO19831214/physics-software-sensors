import type {
  GasParticle,
  GasSimulationConfig,
  GasSimulationSnapshot,
  SpeedCalibration,
} from '../core/types.js';
import { createSeededRandom } from '../core/prng.js';
import { checkContainerBoundary, samplePositionInsideContainer } from '../core/container.js';
import {
  DISPLAY_CALIBRATION,
  sampleMaxwellVelocity,
  calculateTemperatureScaling,
} from '../physics/maxwellBoltzmann.js';
import { resolveWallCollision } from '../physics/collisions.js';
import { MicroscopicStatisticsAccumulator } from './statistics.js';
import { scaleVector3D } from '../core/vector3d.js';

export interface IGasSimulationEngine {
  readonly config: Readonly<GasSimulationConfig>;
  getTemperature(): number;
  setTemperature(tempK: number): void;
  step(dtSeconds: number): GasSimulationSnapshot;
  getSnapshot(): GasSimulationSnapshot;
  reset(initialTemperatureK?: number): void;
}

export class GasSimulationEngine implements IGasSimulationEngine {
  public readonly config: Readonly<GasSimulationConfig>;
  private particles: GasParticle[] = [];
  private currentTemperatureK: number;
  private simTimeSeconds = 0;
  private stepIndex = 0;
  private readonly calibration: SpeedCalibration;
  private readonly rng: () => number;
  private readonly statistics: MicroscopicStatisticsAccumulator;

  constructor(config: GasSimulationConfig) {
    this.config = { ...config };
    this.currentTemperatureK = config.initialTemperatureK;
    this.calibration = config.speedCalibration ?? DISPLAY_CALIBRATION;
    this.rng = config.randomSeed !== undefined ? createSeededRandom(config.randomSeed) : Math.random;
    this.statistics = new MicroscopicStatisticsAccumulator(
      config.container,
      config.frequencyWindowSeconds ?? 0.5,
      this.calibration.referenceTemperatureK
    );

    this.initializeParticles();
  }

  private initializeParticles(): void {
    this.particles = [];
    const radius = this.config.particleRadius ?? 0.05;
    const mass = this.config.particleMass;

    for (let i = 0; i < this.config.particleCount; i++) {
      const position = samplePositionInsideContainer(this.config.container, this.rng, radius);
      const velocity = sampleMaxwellVelocity(this.currentTemperatureK, this.calibration, this.rng);
      this.particles.push({
        id: i,
        position,
        velocity,
        mass,
        radius,
      });
    }
  }

  public getTemperature(): number {
    return this.currentTemperatureK;
  }

  public setTemperature(newTempK: number): void {
    const targetTempK = Math.max(0.1, newTempK);
    if (Math.abs(targetTempK - this.currentTemperatureK) < 1e-4) {
      return;
    }
    const factor = calculateTemperatureScaling(this.currentTemperatureK, targetTempK);
    for (const p of this.particles) {
      p.velocity = scaleVector3D(p.velocity, factor);
    }
    this.currentTemperatureK = targetTempK;
  }

  /**
   * Advances the simulation by dtSeconds.
   * If dt is large, performs sub-stepping to prevent tunneling.
   */
  public step(dtSeconds: number): GasSimulationSnapshot {
    const safeDt = Math.max(0.0001, Math.min(0.1, dtSeconds));
    const maxSubStep = 0.01;
    const subSteps = Math.ceil(safeDt / maxSubStep);
    const subDt = safeDt / subSteps;

    for (let s = 0; s < subSteps; s++) {
      this.advanceSubStep(subDt);
    }

    this.simTimeSeconds += safeDt;
    this.stepIndex++;

    return this.getSnapshot();
  }

  private advanceSubStep(dt: number): void {
    const currentTime = this.simTimeSeconds;
    const container = this.config.container;

    for (const p of this.particles) {
      // Numerical integration: x(t + dt) = x(t) + v * dt
      p.position.x += p.velocity.x * dt;
      p.position.y += p.velocity.y * dt;
      p.position.z += p.velocity.z * dt;

      // Container boundary check
      const col = checkContainerBoundary(p.position, p.radius, container);
      if (col.collided) {
        // Specular bounce
        const response = resolveWallCollision(p.velocity, col.normal, p.mass);
        p.velocity = response.newVelocity;
        p.position = col.clampedPosition;

        if (response.impulse > 0) {
          this.statistics.recordCollision(currentTime, response.impulse);
        }
      }
    }
  }

  public getSnapshot(): GasSimulationSnapshot {
    const stats = this.statistics.compute(
      this.simTimeSeconds,
      this.currentTemperatureK,
      this.particles
    );

    return {
      timestamp: this.simTimeSeconds,
      stepIndex: this.stepIndex,
      temperatureK: this.currentTemperatureK,
      particleCount: this.particles.length,
      particles: this.particles,
      statistics: stats,
    };
  }

  public reset(initialTemperatureK?: number): void {
    this.simTimeSeconds = 0;
    this.stepIndex = 0;
    if (initialTemperatureK !== undefined) {
      this.currentTemperatureK = initialTemperatureK;
    } else {
      this.currentTemperatureK = this.config.initialTemperatureK;
    }
    this.statistics.reset();
    this.initializeParticles();
  }
}
