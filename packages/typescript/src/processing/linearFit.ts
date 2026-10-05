/**
 * General 1D linear regression and physical extrapolation toolkit.
 * Extracted from high-school physics lab apparatus and Charles's Law extrapolations.
 */

export interface Point2D {
  x: number;
  y: number;
}

export interface LinearFitResult {
  /** Ordinary least-squares slope (k in y = kx + b). */
  slope: number;
  /** Ordinary least-squares y-intercept (b in y = kx + b). */
  intercept: number;
  /** Coefficient of determination R^2 (0..1) for unconstrained fit. */
  rSquared: number;
  /** Constrained-through-origin slope (k0 in y = k0 * x). */
  originSlope: number;
  /** Centered R^2 for origin-constrained fit; may be negative for a poor fit. */
  originRSquared: number;
  /** Whether the fit is mathematically well-defined. */
  valid: boolean;
  /** Number of valid data points used in the fit. */
  count: number;
}

/**
 * Calculates both unconstrained and origin-constrained linear regressions.
 */
export function calculateLinearFit(points: readonly Point2D[]): LinearFitResult {
  const validPoints = points.filter(
    (p) => Number.isFinite(p.x) && Number.isFinite(p.y),
  );
  const n = validPoints.length;

  if (n < 2) {
    return {
      slope: 0,
      intercept: 0,
      rSquared: 0,
      originSlope: 0,
      originRSquared: 0,
      valid: false,
      count: n,
    };
  }

  let sumX = 0;
  let sumY = 0;
  let sumX2 = 0;
  let sumXY = 0;
  let sumY2 = 0;

  for (const p of validPoints) {
    sumX += p.x;
    sumY += p.y;
    sumX2 += p.x * p.x;
    sumXY += p.x * p.y;
    sumY2 += p.y * p.y;
  }

  const meanX = sumX / n;
  const meanY = sumY / n;

  let ssXX = 0;
  let ssXY = 0;
  let ssYY = 0;

  for (const p of validPoints) {
    const dx = p.x - meanX;
    const dy = p.y - meanY;
    ssXX += dx * dx;
    ssXY += dx * dy;
    ssYY += dy * dy;
  }

  if (ssXX <= 1e-12 || ![ssXX, ssXY, ssYY, sumX2, sumXY, meanX, meanY].every(Number.isFinite)) {
    return {
      slope: 0,
      intercept: Number.isFinite(meanY) ? meanY : 0,
      rSquared: 0,
      originSlope: 0,
      originRSquared: 0,
      valid: false,
      count: n,
    };
  }

  const slope = ssXY / ssXX;
  const intercept = meanY - slope * meanX;

  let ssRes = 0;
  for (const p of validPoints) {
    const pred = slope * p.x + intercept;
    const res = p.y - pred;
    ssRes += res * res;
  }

  const rSquared = ssYY > 1e-12 ? Math.max(0, Math.min(1, 1 - ssRes / ssYY)) : 1;

  // Origin-constrained slope k0 = sum(x*y) / sum(x^2)
  const originSlope = sumX2 > 1e-12 ? sumXY / sumX2 : 0;
  let ssOriginRes = 0;
  for (const p of validPoints) {
    const originPred = originSlope * p.x;
    const diff = p.y - originPred;
    ssOriginRes += diff * diff;
  }
  const originRSquared =
    ssYY > 1e-12 ? 1 - ssOriginRes / ssYY : (ssOriginRes <= 1e-12 ? 1 : 0);

  return {
    slope,
    intercept,
    rSquared,
    originSlope,
    originRSquared,
    valid: true,
    count: n,
  };
}

/**
 * Extrapolates the x-coordinate where y reaches a target value (default 0).
 * Useful for finding physical intercept constants, e.g. Absolute Zero:
 * in p = k*t + p0, setting targetY = 0 yields t0 = -p0 / k ≈ -273.15 ℃.
 */
export function extrapolateX(fit: LinearFitResult, targetY = 0): number | null {
  if (!fit.valid || !Number.isFinite(targetY) || !Number.isFinite(fit.slope) || !Number.isFinite(fit.intercept) || Math.abs(fit.slope) <= 1e-12) {
    return null;
  }
  const x = (targetY - fit.intercept) / fit.slope;
  return Number.isFinite(x) ? x : null;
}

/**
 * Computes a human-friendly scale step (1, 2, or 5 × 10^n) for plotting and axes.
 */
export function calculateNiceStep(range: number, targetTicks = 6): number {
  if (!Number.isFinite(range) || range <= 0) return 10;
  const ticks = Number.isFinite(targetTicks) ? Math.max(1, targetTicks) : 6;
  const rawStep = range / ticks;
  if (rawStep === 0) return range;
  const magnitude = Math.pow(10, Math.floor(Math.log10(rawStep)));
  if (magnitude === 0) return range;
  const residual = rawStep / magnitude;

  let niceStep = magnitude;
  if (residual > 5) {
    niceStep = 10 * magnitude;
  } else if (residual > 2) {
    niceStep = 5 * magnitude;
  } else if (residual > 1) {
    niceStep = 2 * magnitude;
  }
  return niceStep;
}
