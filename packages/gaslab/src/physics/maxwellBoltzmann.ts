import type { SpeedCalibration, Vector3D } from '../core/types.js';
import { sampleStandardNormal } from '../core/prng.js';
import { createVector3D } from '../core/vector3d.js';

export const DISPLAY_CALIBRATION: SpeedCalibration = {
  referenceTemperatureK: 300,
  referenceRmsSpeed: 2.5,
};

export const SI_CALIBRATION_NITROGEN: SpeedCalibration = {
  referenceTemperatureK: 300,
  // v_rms = sqrt(3 * kB * T / m_N2) = sqrt(3 * 1.380649e-23 * 300 / 4.65e-26) ≈ 516.8 m/s
  referenceRmsSpeed: 516.82,
};

/**
 * Calculates theoretical Root Mean Square speed (v_rms) for a given temperature.
 * v_rms(T) = v_rms0 * sqrt(T / T0)
 */
export function calculateRmsSpeed(
  temperatureK: number,
  calibration: SpeedCalibration = DISPLAY_CALIBRATION
): number {
  validateTemperature(temperatureK);
  validateTemperature(calibration.referenceTemperatureK);
  if (!Number.isFinite(calibration.referenceRmsSpeed) || calibration.referenceRmsSpeed <= 0) throw new RangeError('Reference RMS speed must be finite and positive');
  return calibration.referenceRmsSpeed * Math.sqrt(temperatureK / calibration.referenceTemperatureK);
}

/**
 * Calculates theoretical Most Probable speed (v_p).
 * v_p = sqrt(2/3) * v_rms
 */
export function calculateMostProbableSpeed(
  temperatureK: number,
  calibration: SpeedCalibration = DISPLAY_CALIBRATION
): number {
  return Math.sqrt(2 / 3) * calculateRmsSpeed(temperatureK, calibration);
}

/**
 * Calculates theoretical Mean speed (v_bar).
 * v_bar = sqrt(8 / (3 * pi)) * v_rms
 */
export function calculateMeanSpeed(
  temperatureK: number,
  calibration: SpeedCalibration = DISPLAY_CALIBRATION
): number {
  return Math.sqrt(8 / (3 * Math.PI)) * calculateRmsSpeed(temperatureK, calibration);
}

/**
 * Maxwell-Boltzmann speed Probability Density Function (PDF):
 * f(v) = 4*pi * (1 / (2*pi*sigma^2))^(3/2) * v^2 * exp(-v^2 / (2*sigma^2))
 * where sigma = v_rms / sqrt(3).
 */
export function maxwellBoltzmannSpeedPdf(
  speed: number,
  temperatureK: number,
  calibration: SpeedCalibration = DISPLAY_CALIBRATION
): number {
  if (!Number.isFinite(speed)) throw new RangeError('Speed must be finite');
  if (speed < 0) return 0;
  const vRms = calculateRmsSpeed(temperatureK, calibration);
  const sigma = vRms / Math.sqrt(3);
  const sigma2 = sigma * sigma;
  const prefactor = Math.sqrt(2 / Math.PI) / (sigma2 * sigma);
  return prefactor * speed * speed * Math.exp(-(speed * speed) / (2 * sigma2));
}

/**
 * Generates an exact 3D velocity vector drawn from the Maxwell-Boltzmann distribution
 * by sampling 3 independent Gaussian coordinates N(0, sigma^2).
 */
export function sampleMaxwellVelocity(
  temperatureK: number,
  calibration: SpeedCalibration = DISPLAY_CALIBRATION,
  rng: () => number = Math.random
): Vector3D {
  const vRms = calculateRmsSpeed(temperatureK, calibration);
  const sigma = vRms / Math.sqrt(3);
  return createVector3D(
    sampleStandardNormal(rng) * sigma,
    sampleStandardNormal(rng) * sigma,
    sampleStandardNormal(rng) * sigma
  );
}

/**
 * Velocity scaling factor when temperature changes from T1 to T2.
 * k = sqrt(T2 / T1)
 */
export function calculateTemperatureScaling(fromTempK: number, toTempK: number): number {
  validateTemperature(fromTempK);
  validateTemperature(toTempK);
  return Math.sqrt(toTempK / fromTempK);
}

export function validateTemperature(temperatureK: number): void {
  if (!Number.isFinite(temperatureK) || temperatureK <= 0) throw new RangeError('Temperature must be finite and positive kelvin');
}
