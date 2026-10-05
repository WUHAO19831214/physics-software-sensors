import type { Vector3D, ContainerGeometry } from './types.js';
import { createVector3D } from './vector3d.js';

export interface CollisionResult {
  collided: boolean;
  normal: Vector3D; // inward-pointing unit normal of the container boundary
  clampedPosition: Vector3D;
}

/**
 * Calculates total internal surface area of the container.
 */
export function calculateContainerArea(container: ContainerGeometry): number {
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
        clampedPosition: createVector3D(cx, cy, cz),
      };
    }

    case 'capsule': {
      // Cylinder section from y = 0 to y = cylinderHeight - radius, with bottom hemisphere at y <= 0
      const rLimit = Math.max(0.001, container.radius - particleRadius);
      const topLimit = Math.max(0.001, container.cylinderHeight / 2 - particleRadius);
      const bottomLimit = -container.cylinderHeight / 2 + container.radius;

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
      const rLimit = Math.max(0.01, container.radius - particleRadius);
      const halfH = Math.max(0.01, container.cylinderHeight / 2 - particleRadius);
      const theta = rng() * 2 * Math.PI;
      const r = Math.sqrt(rng()) * rLimit;
      return {
        x: r * Math.cos(theta),
        y: (rng() * 2 - 1) * halfH,
        z: r * Math.sin(theta),
      };
    }
  }
}
