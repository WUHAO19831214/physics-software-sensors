import { applyCoordinateTransform } from './coordinates.js';
import type { CoordinateTransform3, Vector3Arrow, Vector3Measurement, Vector3RenderModel, Vector3Value } from './types.js';

const ORIGIN: Vector3Value = { x: 0, y: 0, z: 0 };

export function createVector3RenderModel(
  measurement: Vector3Measurement,
  transform: CoordinateTransform3,
): Vector3RenderModel {
  const transformed = applyCoordinateTransform(measurement.components, transform);
  const source = measurement.componentDetails;
  const componentTargets: Array<[Vector3Arrow['id'], string, Vector3Value, 'x' | 'y' | 'z']> = [
    ['x-component', 'x', applyCoordinateTransform({ x: measurement.components.x, y: 0, z: 0 }, transform), 'x'],
    ['y-component', 'y', applyCoordinateTransform({ x: 0, y: measurement.components.y, z: 0 }, transform), 'y'],
    ['z-component', 'z', applyCoordinateTransform({ x: 0, y: 0, z: measurement.components.z }, transform), 'z'],
  ];
  const arrows: Vector3Arrow[] = componentTargets.map(([id, label, to, axis]) => ({
    id,
    label,
    from: ORIGIN,
    to,
    source: source[axis].source,
  }));
  arrows.push({ id: 'resultant', label: 'resultant', from: ORIGIN, to: transformed });
  return {
    coordinateSystem: transform.to,
    axes: [
      { id: 'x-axis', label: 'x', direction: applyCoordinateTransform({ x: 1, y: 0, z: 0 }, transform) },
      { id: 'y-axis', label: 'y', direction: applyCoordinateTransform({ x: 0, y: 1, z: 0 }, transform) },
      { id: 'z-axis', label: 'z', direction: applyCoordinateTransform({ x: 0, y: 0, z: 1 }, transform) },
    ],
    arrows,
    annotations: {
      quantity: measurement.quantity,
      unit: measurement.unit,
      magnitude: measurement.magnitude,
      source_coordinate_system: measurement.coordinateSystem,
      transform_id: transform.id,
    },
  };
}
