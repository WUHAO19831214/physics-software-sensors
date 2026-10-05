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
  const vn = dotVector3D(velocity, inwardNormal);
  if (vn >= 0) {
    // Particle is already moving away from the wall
    return {
      newVelocity: velocity,
      impulse: 0,
    };
  }

  // Reflect: v' = v - 2 * vn * n
  const newVelocity: Vector3D = {
    x: velocity.x - 2 * vn * inwardNormal.x,
    y: velocity.y - 2 * vn * inwardNormal.y,
    z: velocity.z - 2 * vn * inwardNormal.z,
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
