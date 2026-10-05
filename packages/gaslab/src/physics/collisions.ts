import type { Vector3D } from '../core/types.js';
import { dotVector3D, lengthSqVector3D } from '../core/vector3d.js';

export interface WallCollisionResponse {
  newVelocity: Vector3D;
  impulse: number; // magnitude of momentum imparted to the wall: 2 * m * |v_n|
}

/**
 * Resolves specular elastic collision against a wall with inward-pointing normal n.
 *
 * If v . n < 0, the particle is heading towards the wall boundary.
 * The specular bounce gives:
 *   v' = v - 2 * (v . n) * n
 * The momentum transferred to the wall is:
 *   Delta p_wall = 2 * m * |v . n| * (-n)
 * Kinetic energy is strictly conserved: |v'|^2 = |v|^2.
 */
export function resolveWallCollision(
  velocity: Vector3D,
  inwardNormal: Vector3D,
  mass: number
): WallCollisionResponse {
  if (![velocity.x, velocity.y, velocity.z, inwardNormal.x, inwardNormal.y, inwardNormal.z, mass].every(Number.isFinite) || mass <= 0) throw new RangeError('Collision inputs must be finite with positive mass');
  const norm = Math.sqrt(lengthSqVector3D(inwardNormal));
  if (norm === 0) throw new RangeError('Wall normal must be nonzero');
  const n = { x: inwardNormal.x / norm, y: inwardNormal.y / norm, z: inwardNormal.z / norm };
  const vn = dotVector3D(velocity, n);
  if (vn >= 0) {
    // Particle is already moving away from the wall
    return {
      newVelocity: velocity,
      impulse: 0,
    };
  }

  // Reflect: v' = v - 2 * vn * n
  const newVelocity: Vector3D = {
    x: velocity.x - 2 * vn * n.x,
    y: velocity.y - 2 * vn * n.y,
    z: velocity.z - 2 * vn * n.z,
  };

  const impulse = 2 * mass * Math.abs(vn);

  return {
    newVelocity,
    impulse,
  };
}

/**
 * Calculates translational kinetic energy: E_k = 0.5 * m * |v|^2
 */
export function calculateKineticEnergy(mass: number, velocity: Vector3D): number {
  return 0.5 * mass * lengthSqVector3D(velocity);
}
