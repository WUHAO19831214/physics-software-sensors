import type { GasParticle, GasStatistics, ContainerGeometry } from '../core/types.js';
import { lengthVector3D, lengthSqVector3D } from '../core/vector3d.js';
import { calculateContainerArea } from '../core/container.js';

interface TimedCollision {
  time: number;
  impulse: number;
}

export class MicroscopicStatisticsAccumulator {
  private totalCollisions = 0;
  private readonly recentCollisions: TimedCollision[] = [];
  private readonly windowDuration: number;
  private readonly containerArea: number;
  private readonly referenceTemperatureK: number;

  constructor(
    container: ContainerGeometry,
    windowDurationSeconds = 0.5,
    referenceTemperatureK = 300,
    private readonly unitSystem: 'si' | 'display' = 'display'
  ) {
    this.containerArea = calculateContainerArea(container);
    if (!Number.isFinite(windowDurationSeconds) || windowDurationSeconds <= 0) throw new RangeError('Statistics window must be finite and positive');
    this.windowDuration = windowDurationSeconds;
    this.referenceTemperatureK = referenceTemperatureK;
  }

  public recordCollision(time: number, impulse: number): void {
    this.totalCollisions++;
    this.recentCollisions.push({ time, impulse });
  }

  public prune(currentTime: number): void {
    const cutoff = currentTime - this.windowDuration;
    while (this.recentCollisions.length > 0 && this.recentCollisions[0]!.time < cutoff) {
      this.recentCollisions.shift();
    }
  }

  public compute(
    currentTime: number,
    currentTemperatureK: number,
    particles: ReadonlyArray<GasParticle>,
    referencePressureKPa?: number
  ): GasStatistics {
    this.prune(currentTime);

    // Collision frequency in Hz
    const countInWindow = this.recentCollisions.length;
    const collisionFrequencyHz = countInWindow / this.windowDuration;

    // Microscopic impulse pressure: p = sum(I) / (Area * delta_t)
    let totalImpulseInWindow = 0;
    for (const c of this.recentCollisions) {
      totalImpulseInWindow += c.impulse;
    }
    const microscopicImpulsePressure =
      this.containerArea > 0
        ? totalImpulseInWindow / (this.containerArea * this.windowDuration)
        : 0;

    // Particle speed stats
    let sumSpeed = 0;
    let sumSpeedSq = 0;
    const n = particles.length;

    if (n > 0) {
      for (let i = 0; i < n; i++) {
        const p = particles[i]!;
        const speed = lengthVector3D(p.velocity);
        sumSpeed += speed;
        sumSpeedSq += lengthSqVector3D(p.velocity);
      }
    }

    const meanSpeed = n > 0 ? sumSpeed / n : 0;
    const rmsSpeed = n > 0 ? Math.sqrt(sumSpeedSq / n) : 0;

    // Pedagogical pressure ratio: T / T0
    const safeRefT = Math.max(0.1, this.referenceTemperatureK);
    const pedagogicalPressureRatio = currentTemperatureK / safeRefT;

    const stats: GasStatistics = {
      temperatureK: currentTemperatureK,
      collisionCountTotal: this.totalCollisions,
      collisionFrequencyHz,
      meanSpeed,
      rmsSpeed,
      microscopicImpulsePressure,
      microscopicImpulsePressureUnit: this.unitSystem === 'si' ? 'Pa' : 'simulation',
      pedagogicalPressureRatio,
    };

    if (referencePressureKPa !== undefined) {
      stats.stateEquationPressure = referencePressureKPa * pedagogicalPressureRatio;
    }

    return stats;
  }

  public reset(): void {
    this.totalCollisions = 0;
    this.recentCollisions.length = 0;
  }
}
