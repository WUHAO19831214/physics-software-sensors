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
  let u1 = rng();
  while (u1 <= 1e-15) {
    u1 = rng();
  }
  const u2 = rng();
  return Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
}
