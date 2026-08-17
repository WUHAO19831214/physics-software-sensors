import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import test from 'node:test';

import {
  Vector3Assembler,
  YANAN_CLASSROOM_TO_SCENE,
  applyCoordinateTransform,
  composeVector3,
  createVector3RenderModel,
  type Vector3Components,
} from '../src/index.js';

const observed = (value: number, timestampMs = 1000) => ({ value, source: 'observed' as const, timestampMs });
const constrained = (value: number) => ({ value, source: 'constrained' as const });

function components(x: number, y: number, z: number): Vector3Components {
  return { x: observed(x), y: observed(y), z: observed(z) };
}

function compose(values: Vector3Components) {
  return composeVector3({ quantity: 'generic-vector', unit: '1', coordinateSystem: 'right-handed-xyz', components: values });
}

test('axis-aligned and negative vectors use the documented angle convention', () => {
  const positiveX = compose(components(2, 0, 0)).measurement!;
  assert.deepEqual(positiveX.direction, { azimuthDeg: 0, elevationDeg: 0 });
  assert.deepEqual(positiveX.normalized, { x: 1, y: 0, z: 0 });
  const negativeY = compose(components(0, -2, 0)).measurement!;
  assert.deepEqual(negativeY.direction, { azimuthDeg: 270, elevationDeg: 0 });
  const positiveZ = compose(components(0, 0, 5)).measurement!;
  assert.deepEqual(positiveZ.direction, { azimuthDeg: 0, elevationDeg: 90 });
});

test('general xyz magnitude, normalization, azimuth, and elevation are correct', () => {
  const measurement = compose(components(3, 4, 12)).measurement!;
  assert.equal(measurement.magnitude, 13);
  assert.deepEqual(measurement.normalized, { x: 3 / 13, y: 4 / 13, z: 12 / 13 });
  assert.ok(Math.abs(measurement.direction!.azimuthDeg - 53.13010235415598) < 1e-12);
  assert.ok(Math.abs(measurement.direction!.elevationDeg - 67.38013505195957) < 1e-12);
});

test('zero vector has no invented normalized direction', () => {
  const result = compose(components(0, 0, 0));
  assert.equal(result.status, 'warning');
  assert.equal(result.measurement!.normalized, null);
  assert.equal(result.measurement!.direction, null);
  assert.deepEqual(result.flags, ['zero-vector']);
});

test('missing component remains incomplete and is not defaulted to zero', () => {
  const result = compose({ x: observed(1), y: { source: 'missing' }, z: observed(3) });
  assert.equal(result.status, 'incomplete');
  assert.equal(result.measurement, null);
  assert.deepEqual(result.missingComponents, ['y']);
});

test('component sources and quality remain distinct', () => {
  const result = compose({
    x: constrained(0),
    y: { value: 2, source: 'observed', timestampMs: 1000, quality: { confidence: 0.91, flags: ['ocr-replay'] } },
    z: { value: 3, source: 'derived', timestampMs: 1000, quality: { uncertainty: 0.2 } },
  });
  assert.equal(result.measurement!.componentDetails.x.source, 'constrained');
  assert.equal(result.measurement!.componentDetails.y.quality!.confidence, 0.91);
  assert.equal(result.measurement!.componentDetails.z.quality!.uncertainty, 0.2);
  assert.equal('confidence' in result.measurement!.quality, false);
  assert.ok(result.flags.includes('component-y:ocr-replay'));
});

test('assembler flags component time skew above its configured boundary', () => {
  const assembler = new Vector3Assembler({ maxComponentSkewMs: 50 });
  const result = assembler.compose({
    quantity: 'force', unit: 'N', coordinateSystem: 'lab',
    components: { x: observed(1, 1000), y: observed(2, 1040), z: observed(3, 1100) },
  });
  assert.equal(result.measurement!.componentSkewMs, 100);
  assert.equal(result.measurement!.timestampMs, 1100);
  assert.ok(result.flags.includes('component-time-skew'));
});

test('Yan\'an classroom transform is separate and maps xyz to -x,z,y', () => {
  assert.deepEqual(applyCoordinateTransform({ x: 3, y: 4, z: 12 }, YANAN_CLASSROOM_TO_SCENE), { x: -3, y: 12, z: 4 });
});

test('renderer-neutral adapter preserves constrained provenance on component arrows', () => {
  const result = compose({ x: constrained(0), y: observed(-2.33), z: observed(0.5) });
  const model = createVector3RenderModel(result.measurement!, YANAN_CLASSROOM_TO_SCENE);
  assert.equal(model.axes.length, 3);
  assert.deepEqual(model.axes.map((axis) => axis.direction), [{ x: -1, y: 0, z: 0 }, { x: 0, y: 0, z: 1 }, { x: 0, y: 1, z: 0 }]);
  assert.deepEqual(model.arrows.at(-1)!.to, { x: 0, y: 0.5, z: -2.33 });
  assert.equal(model.arrows[0]!.source, 'constrained');
});

test('golden cases match historical and current source formulas', () => {
  const fixturePath = path.join(process.cwd(), 'tests', 'fixtures', 'vector3', 'yanan-golden.json');
  const fixture = JSON.parse(readFileSync(fixturePath, 'utf8')) as {
    tolerance: number;
    cases: Array<{ components: { x: number; y: number; z: number }; expected_magnitude: number; expected_direction: { azimuth_deg: number; elevation_deg: number } | null; expected_scene: { x: number; y: number; z: number } }>;
  };
  for (const item of fixture.cases) {
    const measurement = compose(components(item.components.x, item.components.y, item.components.z)).measurement!;
    assert.ok(Math.abs(measurement.magnitude - item.expected_magnitude) <= fixture.tolerance);
    if (item.expected_direction === null) {
      assert.equal(measurement.direction, null);
    } else {
      assert.ok(Math.abs(measurement.direction!.azimuthDeg - item.expected_direction.azimuth_deg) <= fixture.tolerance);
      assert.ok(Math.abs(measurement.direction!.elevationDeg - item.expected_direction.elevation_deg) <= fixture.tolerance);
    }
    const scene = applyCoordinateTransform(measurement.components, YANAN_CLASSROOM_TO_SCENE);
    for (const axis of ['x', 'y', 'z'] as const) assert.ok(Math.abs(scene[axis] - item.expected_scene[axis]) <= fixture.tolerance);
  }
});

test('invalid values and confidence are rejected explicitly', () => {
  assert.throws(() => compose({ x: observed(Number.NaN), y: observed(2), z: observed(3) }), /finite value/);
  assert.throws(() => compose({ x: observed(1), y: { value: 2, source: 'observed', quality: { confidence: 1.2 } }, z: observed(3) }), /confidence/);
});
