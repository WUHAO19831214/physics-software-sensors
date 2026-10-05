import type {
  GasParticle,
  GasSimulationConfig,
  GasSimulationSnapshot,
  SpeedCalibration,
} from '../core/types.js';
import { createSeededRandom } from '../core/prng.js';
import { checkContainerBoundary, samplePositionInsideContainer, validateContainer } from '../core/container.js';
import {
  DISPLAY_CALIBRATION,
  sampleMaxwellVelocity,
  calculateTemperatureScaling,
  calculateRmsSpeed,
  validateTemperature,
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
  private rng: () => number;
  private readonly statistics: MicroscopicStatisticsAccumulator;

  constructor(config: GasSimulationConfig) {
    validateContainer(config.container, config.particleRadius ?? 0.05);
    validateTemperature(config.initialTemperatureK);
    if (!Number.isInteger(config.particleCount) || config.particleCount < 0 || !Number.isFinite(config.particleMass) || config.particleMass <= 0) throw new RangeError('Particle count must be a nonnegative integer and mass positive');
    this.config = Object.freeze({ ...config, container: Object.freeze({ ...config.container }),
      ...(config.speedCalibration ? { speedCalibration: Object.freeze({ ...config.speedCalibration }) } : {}) });
    this.currentTemperatureK = config.initialTemperatureK;
    if (config.unitSystem === 'si' && config.speedCalibration) throw new RangeError('SI mode derives speeds from particleMass; omit display calibration');
    this.calibration = config.unitSystem === 'si'
      ? { referenceTemperatureK: config.initialTemperatureK, referenceRmsSpeed: Math.sqrt(3 * 1.380649e-23 * config.initialTemperatureK / config.particleMass) }
      : this.config.speedCalibration ?? DISPLAY_CALIBRATION;
    // Validate calibration even when no particles are requested.
    calculateRmsSpeed(config.initialTemperatureK, this.calibration);
    if (config.randomSeed !== undefined && !Number.isSafeInteger(config.randomSeed)) throw new RangeError('Random seed must be a safe integer');
    this.rng = config.randomSeed !== undefined ? createSeededRandom(config.randomSeed) : Math.random;
    this.statistics = new MicroscopicStatisticsAccumulator(
      config.container,
      config.frequencyWindowSeconds ?? 0.5,
      this.calibration.referenceTemperatureK,
      config.unitSystem ?? 'display'
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
    validateTemperature(newTempK);
    const targetTempK = newTempK;
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
    if (!Number.isFinite(dtSeconds) || dtSeconds < 0) throw new RangeError('Step duration must be finite and nonnegative seconds');
    if (dtSeconds === 0) return this.getSnapshot();
    const c = this.config.container;
    const radius = this.config.particleRadius ?? 0.05;
    const minSpan = c.type === 'box' ? Math.min(c.width, c.height, c.depth) - 2 * radius
      : c.type === 'cylinder' ? Math.min(2 * c.radius, c.height) - 2 * radius
      : Math.min(2 * c.radius - 2 * radius, c.cylinderHeight - radius);
    const maxSpeed = this.particles.reduce((v, p) => Math.max(v, Math.hypot(p.velocity.x, p.velocity.y, p.velocity.z)), 0);
    const subSteps = Math.max(1, Math.ceil(dtSeconds / 0.01), Math.ceil(dtSeconds * maxSpeed / (minSpan * 0.1)));
    if (!Number.isFinite(subSteps) || subSteps > 1000000) throw new RangeError('Step exceeds substep budget; use smaller durations');
    const subDt = dtSeconds / subSteps;
    const startTime = this.simTimeSeconds;
    for (let s = 0; s < subSteps; s++) {
      this.simTimeSeconds = startTime + (s + 1) * subDt;
      this.advanceSubStep(subDt);
    }
    this.simTimeSeconds = startTime + dtSeconds;
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
        for (const normal of col.normals ?? [col.normal]) {
          const response = resolveWallCollision(p.velocity, normal, p.mass);
          p.velocity = response.newVelocity;
          if (response.impulse > 0) this.statistics.recordCollision(currentTime, response.impulse);
        }
        p.position = col.clampedPosition;
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
      particles: this.particles.map(p => ({ ...p, position: { ...p.position }, velocity: { ...p.velocity } })),
      statistics: stats,
    };
  }

  public reset(initialTemperatureK?: number): void {
    validateTemperature(initialTemperatureK ?? this.config.initialTemperatureK);
    this.rng = this.config.randomSeed !== undefined ? createSeededRandom(this.config.randomSeed) : Math.random;
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
