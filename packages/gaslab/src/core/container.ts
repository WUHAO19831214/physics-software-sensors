import type { Vector3D, ContainerGeometry } from './types.js';
import { createVector3D } from './vector3d.js';

export interface CollisionResult {
  collided: boolean;
  normals?: Vector3D[]; // Independent face contacts at corners/rims.
  normal: Vector3D; // inward-pointing unit normal of the container boundary
  clampedPosition: Vector3D;
}

/**
 * Calculates total internal surface area of the container.
 */
export function calculateContainerArea(container: ContainerGeometry): number {
  validateContainer(container);
  switch (container.type) {
    case 'box':
      return 2 * (container.width * container.height + container.width * container.depth + container.height * container.depth);
    case 'cylinder': {
      const r = container.radius;
      const h = container.height;
      return 2 * Math.PI * r * h + 2 * Math.PI * r * r;
    }
    case 'capsule': {
      // Cylinder of height h with radius r + bottom hemisphere + flat top
      const r = container.radius;
      const h = container.cylinderHeight;
      return 2 * Math.PI * r * h + 2 * Math.PI * r * r + Math.PI * r * r;
    }
  }
}

/**
 * Checks and resolves particle-wall collision against container boundary.
 * Container is centered at origin (0, 0, 0).
 */
export function checkContainerBoundary(
  pos: Vector3D,
  particleRadius: number,
  container: ContainerGeometry
): CollisionResult {
  validateContainer(container, particleRadius);
  if (![pos.x, pos.y, pos.z].every(Number.isFinite)) throw new RangeError('Position must be finite');
  switch (container.type) {
    case 'box': {
      const halfW = container.width / 2 - particleRadius;
      const halfH = container.height / 2 - particleRadius;
      const halfD = container.depth / 2 - particleRadius;

      let nx = 0;
      let ny = 0;
      let nz = 0;
      let cx = pos.x;
      let cy = pos.y;
      let cz = pos.z;
      let collided = false;

      if (pos.x > halfW) {
        cx = halfW;
        nx = -1;
        collided = true;
      } else if (pos.x < -halfW) {
        cx = -halfW;
        nx = 1;
        collided = true;
      }

      if (pos.y > halfH) {
        cy = halfH;
        ny = -1;
        collided = true;
      } else if (pos.y < -halfH) {
        cy = -halfH;
        ny = 1;
        collided = true;
      }

      if (pos.z > halfD) {
        cz = halfD;
        nz = -1;
        collided = true;
      } else if (pos.z < -halfD) {
        cz = -halfD;
        nz = 1;
        collided = true;
      }

      if (!collided) {
        return { collided: false, normal: createVector3D(0, 0, 0), clampedPosition: pos };
      }

      // Normalize normal vector if hit at a corner/edge
      const len = Math.sqrt(nx * nx + ny * ny + nz * nz);
      return {
        collided: true,
        normal: createVector3D(nx / len, ny / len, nz / len),
        normals: [
          ...(nx ? [createVector3D(nx, 0, 0)] : []),
          ...(ny ? [createVector3D(0, ny, 0)] : []),
          ...(nz ? [createVector3D(0, 0, nz)] : []),
        ],
        clampedPosition: createVector3D(cx, cy, cz),
      };
    }

    case 'cylinder': {
      // Cylinder aligned along Y axis: x^2 + z^2 <= radius^2, -height/2 <= y <= height/2
      const rLimit = Math.max(0.001, container.radius - particleRadius);
      const halfH = Math.max(0.001, container.height / 2 - particleRadius);

      const r = Math.sqrt(pos.x * pos.x + pos.z * pos.z);
      let cx = pos.x;
      let cy = pos.y;
      let cz = pos.z;
      let nx = 0;
      let ny = 0;
      let nz = 0;
      let collided = false;

      if (r > rLimit) {
        collided = true;
        const factor = rLimit / (r || 1);
        cx = pos.x * factor;
        cz = pos.z * factor;
        nx = -pos.x / (r || 1);
        nz = -pos.z / (r || 1);
      }

      if (pos.y > halfH) {
        collided = true;
        cy = halfH;
        ny = -1;
      } else if (pos.y < -halfH) {
        collided = true;
        cy = -halfH;
        ny = 1;
      }

      if (!collided) {
        return { collided: false, normal: createVector3D(0, 0, 0), clampedPosition: pos };
      }

      const len = Math.sqrt(nx * nx + ny * ny + nz * nz);
      return {
        collided: true,
        normal: createVector3D(nx / len, ny / len, nz / len),
        normals: [
          ...(nx || nz ? [createVector3D(nx, 0, nz)] : []),
          ...(ny ? [createVector3D(0, ny, 0)] : []),
        ],
        clampedPosition: createVector3D(cx, cy, cz),
      };
    }

    case 'capsule': {
      // Straight cylinder centered at y=0, a hemisphere below -cylinderHeight/2, flat top.
      const rLimit = Math.max(0.001, container.radius - particleRadius);
      const topLimit = Math.max(0.001, container.cylinderHeight / 2 - particleRadius);
      const bottomLimit = -container.cylinderHeight / 2;

      let cx = pos.x;
      let cy = pos.y;
      let cz = pos.z;
      let nx = 0;
      let ny = 0;
      let nz = 0;
      let collided = false;

      // If in bottom hemisphere region
      if (pos.y < bottomLimit) {
        const dy = pos.y - bottomLimit;
        const dist = Math.sqrt(pos.x * pos.x + dy * dy + pos.z * pos.z);
        if (dist > rLimit) {
          collided = true;
          const factor = rLimit / (dist || 1);
          cx = pos.x * factor;
          cy = bottomLimit + dy * factor;
          cz = pos.z * factor;
          nx = -pos.x / (dist || 1);
          ny = -dy / (dist || 1);
          nz = -pos.z / (dist || 1);
        }
      } else {
        // In cylinder section
        const r = Math.sqrt(pos.x * pos.x + pos.z * pos.z);
        if (r > rLimit) {
          collided = true;
          const factor = rLimit / (r || 1);
          cx = pos.x * factor;
          cz = pos.z * factor;
          nx = -pos.x / (r || 1);
          nz = -pos.z / (r || 1);
        }
        if (pos.y > topLimit) {
          collided = true;
          cy = topLimit;
          ny = -1;
        }
      }

      if (!collided) {
        return { collided: false, normal: createVector3D(0, 0, 0), clampedPosition: pos };
      }

      const len = Math.sqrt(nx * nx + ny * ny + nz * nz) || 1;
      return {
        collided: true,
        normal: createVector3D(nx / len, ny / len, nz / len),
        normals: pos.y < bottomLimit
          ? [createVector3D(nx / len, ny / len, nz / len)]
          : [
            ...(nx || nz ? [createVector3D(nx, 0, nz)] : []),
            ...(ny ? [createVector3D(0, ny, 0)] : []),
          ],
        clampedPosition: createVector3D(cx, cy, cz),
      };
    }
  }
}

/**
 * Samples a random initial position uniformly distributed inside the container.
 */
export function samplePositionInsideContainer(
  container: ContainerGeometry,
  rng: () => number = Math.random,
  particleRadius = 0.05
): Vector3D {
  validateContainer(container, particleRadius);
  switch (container.type) {
    case 'box': {
      const halfW = Math.max(0.01, container.width / 2 - particleRadius);
      const halfH = Math.max(0.01, container.height / 2 - particleRadius);
      const halfD = Math.max(0.01, container.depth / 2 - particleRadius);
      return {
        x: (rng() * 2 - 1) * halfW,
        y: (rng() * 2 - 1) * halfH,
        z: (rng() * 2 - 1) * halfD,
      };
    }
    case 'cylinder': {
      const rLimit = Math.max(0.01, container.radius - particleRadius);
      const halfH = Math.max(0.01, container.height / 2 - particleRadius);
      const theta = rng() * 2 * Math.PI;
      const r = Math.sqrt(rng()) * rLimit;
      return {
        x: r * Math.cos(theta),
        y: (rng() * 2 - 1) * halfH,
        z: r * Math.sin(theta),
      };
    }
    case 'capsule': {
      const rLimit = container.radius - particleRadius;
      const bottom = -container.cylinderHeight / 2 - rLimit;
      const top = container.cylinderHeight / 2 - particleRadius;
      // Uniform rejection sampling within the cylinder enclosing the accessible volume.
      for (let attempt = 0; attempt < 10000; attempt++) {
        const theta = rng() * 2 * Math.PI;
        const r = Math.sqrt(rng()) * rLimit;
        const pos = { x: r * Math.cos(theta), y: bottom + rng() * (top - bottom), z: r * Math.sin(theta) };
        if (!checkContainerBoundary(pos, particleRadius, container).collided) return pos;
      }
      throw new RangeError('RNG failed to sample a position inside the capsule');
    }
  }
}

export function validateContainer(container: ContainerGeometry, particleRadius = 0): void {
  if (!Number.isFinite(particleRadius) || particleRadius < 0) throw new RangeError('Particle radius must be finite and nonnegative');
  const dimensions = container.type === 'box'
    ? [container.width, container.height, container.depth]
    : container.type === 'cylinder' ? [container.radius, container.height]
    : container.type === 'capsule' ? [container.radius, container.cylinderHeight] : [];
  if (!dimensions.length || !dimensions.every(x => Number.isFinite(x) && x > 0)) throw new RangeError('Container dimensions must be finite and positive');
  const fits = container.type === 'box'
    ? Math.min(container.width, container.height, container.depth) / 2 > particleRadius
    : container.type === 'cylinder'
      ? Math.min(container.radius, container.height / 2) > particleRadius
      : container.radius > particleRadius && container.cylinderHeight > particleRadius;
  if (!fits) throw new RangeError('Particle radius must fit inside the container');
}
