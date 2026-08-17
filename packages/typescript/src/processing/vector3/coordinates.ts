import type { CoordinateTransform3, Vector3Value } from './types.js';

export const IDENTITY_VECTOR3_TRANSFORM: CoordinateTransform3 = {
  id: 'identity',
  from: 'caller-coordinate-system',
  to: 'caller-coordinate-system',
  matrix: [1, 0, 0, 0, 1, 0, 0, 0, 1],
};

/**
 * Yan'an classroom coordinates to its current Three.js scene convention:
 * classroom (x, y, z) -> scene (-x, z, y).
 * Kept separate from vector composition because it is a presentation choice.
 */
export const YANAN_CLASSROOM_TO_SCENE: CoordinateTransform3 = {
  id: 'yanan-classroom-to-three-scene',
  from: 'yanan-classroom-x-conductor-y-horizontal-z-up',
  to: 'yanan-three-scene-x-left-y-up-z-horizontal',
  matrix: [-1, 0, 0, 0, 0, 1, 0, 1, 0],
  notes: 'Pinned to source commit cb073e89d6d87129287030f1df08bd540504eb39.',
};

export function applyCoordinateTransform(value: Vector3Value, transform: CoordinateTransform3): Vector3Value {
  const [m00, m01, m02, m10, m11, m12, m20, m21, m22] = transform.matrix;
  return {
    x: m00 * value.x + m01 * value.y + m02 * value.z,
    y: m10 * value.x + m11 * value.y + m12 * value.z,
    z: m20 * value.x + m21 * value.y + m22 * value.z,
  };
}
