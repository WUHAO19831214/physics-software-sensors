/**
 * Deterministic 32-bit pseudo-random number generator (Mulberry32).
 */
export function createSeededRandom(seed = 123456789): () => number {
  let a = seed >>> 0;
  return function mulberry32(): number {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/**
 * Box-Muller transform to sample from standard normal distribution N(0, 1).
 */
export function sampleStandardNormal(rng: () => number = Math.random): number {
  const first = rng();
  const u2 = rng();
  if (![first, u2].every(u => Number.isFinite(u) && u >= 0 && u < 1)) throw new RangeError('RNG must return finite values in [0, 1)');
  const u1 = Math.max(Number.EPSILON, first);
  return Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
}
