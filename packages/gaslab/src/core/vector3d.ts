import type { Vector3D } from './types.js';

export function createVector3D(x = 0, y = 0, z = 0): Vector3D {
  return { x, y, z };
}

export function addVector3D(a: Vector3D, b: Vector3D): Vector3D {
  return { x: a.x + b.x, y: a.y + b.y, z: a.z + b.z };
}

export function subVector3D(a: Vector3D, b: Vector3D): Vector3D {
  return { x: a.x - b.x, y: a.y - b.y, z: a.z - b.z };
}

export function scaleVector3D(v: Vector3D, s: number): Vector3D {
  return { x: v.x * s, y: v.y * s, z: v.z * s };
}

export function dotVector3D(a: Vector3D, b: Vector3D): number {
  return a.x * b.x + a.y * b.y + a.z * b.z;
}

export function lengthSqVector3D(v: Vector3D): number {
  return v.x * v.x + v.y * v.y + v.z * v.z;
}

export function lengthVector3D(v: Vector3D): number {
  return Math.sqrt(lengthSqVector3D(v));
}

export function normalizeVector3D(v: Vector3D): Vector3D {
  const len = lengthVector3D(v);
  if (len === 0) {
    return { x: 0, y: 1, z: 0 };
  }
  return { x: v.x / len, y: v.y / len, z: v.z / len };
}

export function reflectVector3D(v: Vector3D, normal: Vector3D): Vector3D {
  // v' = v - 2 * (v . n) * n
  const vn = dotVector3D(v, normal);
  return {
    x: v.x - 2 * vn * normal.x,
    y: v.y - 2 * vn * normal.y,
    z: v.z - 2 * vn * normal.z,
  };
}
