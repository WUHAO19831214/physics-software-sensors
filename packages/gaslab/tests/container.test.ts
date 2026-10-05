import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  checkContainerBoundary,
  calculateContainerArea,
  samplePositionInsideContainer,
} from '../src/core/container.js';
import { createVector3D } from '../src/core/vector3d.js';
import { createSeededRandom } from '../src/core/prng.js';

test('Box container boundary checking and clamping', () => {
  const box = { type: 'box' as const, width: 2.0, height: 2.0, depth: 2.0 };
  const particleRadius = 0.1;
  const halfLimit = 1.0 - 0.1; // 0.9

  // Inside
  const inside = checkContainerBoundary(createVector3D(0.5, 0.5, 0.5), particleRadius, box);
  assert.equal(inside.collided, false);

  // Outside +X
  const outsideX = checkContainerBoundary(createVector3D(1.2, 0.0, 0.0), particleRadius, box);
  assert.equal(outsideX.collided, true);
  assert.equal(outsideX.normal.x, -1);
  assert.ok(Math.abs(outsideX.clampedPosition.x - halfLimit) < 1e-6);

  // Area
  assert.equal(calculateContainerArea(box), 24.0);
});

test('Cylinder container boundary checking', () => {
  const cylinder = { type: 'cylinder' as const, radius: 1.5, height: 4.0 };
  const particleRadius = 0.05;
  const rLimit = 1.45;

  // Inside
  const inside = checkContainerBoundary(createVector3D(0.5, 1.0, 0.5), particleRadius, cylinder);
  assert.equal(inside.collided, false);

  // Outside radial wall (x = 2.0, z = 0, y = 0)
  const outsideWall = checkContainerBoundary(createVector3D(2.0, 0.0, 0.0), particleRadius, cylinder);
  assert.equal(outsideWall.collided, true);
  assert.ok(outsideWall.normal.x < 0);
  assert.ok(Math.abs(outsideWall.clampedPosition.x - rLimit) < 1e-6);

  // Outside top cap (y = 2.5)
  const outsideTop = checkContainerBoundary(createVector3D(0.0, 2.5, 0.0), particleRadius, cylinder);
  assert.equal(outsideTop.collided, true);
  assert.equal(outsideTop.normal.y, -1);
});

test('Position sampling strictly inside container bounds', () => {
  const cylinder = { type: 'cylinder' as const, radius: 2.0, height: 5.0 };
  const rng = createSeededRandom(101);

  for (let i = 0; i < 500; i++) {
    const pos = samplePositionInsideContainer(cylinder, rng, 0.1);
    const r = Math.sqrt(pos.x * pos.x + pos.z * pos.z);
    assert.ok(r <= 1.9 + 1e-6, `Sampled radius ${r} exceeds limit 1.9`);
    assert.ok(Math.abs(pos.y) <= 2.4 + 1e-6, `Sampled y ${pos.y} exceeds limit 2.4`);
  }
});

test('capsule initialization is uniformly sampled inside the declared hemisphere and cylinder', () => {
  const capsule = { type: 'capsule' as const, radius: 1, cylinderHeight: 3 };
  const rng = createSeededRandom(42);
  let hemisphereCount = 0;
  for (let i = 0; i < 4000; i++) {
    const p = samplePositionInsideContainer(capsule, rng, 0);
    assert.equal(checkContainerBoundary(p, 0, capsule).collided, false);
    if (p.y < -1.5) hemisphereCount++;
  }
  assert.ok(Math.abs(hemisphereCount / 4000 - 2 / 11) < 0.025);
  assert.ok(Math.abs(calculateContainerArea(capsule) - 9 * Math.PI) < 1e-12);
  assert.throws(() => samplePositionInsideContainer({ type: 'box', width: 1, height: 1, depth: 1 }, rng, 1), RangeError);
});

test('corner contacts reflect each crossed face instead of a fictitious diagonal wall', async () => {
  const { resolveWallCollision } = await import('../src/physics/collisions.js');
  const contact = checkContainerBoundary({ x: 2, y: 2, z: 0 }, 0, { type: 'box', width: 2, height: 2, depth: 2 });
  let velocity = { x: 3, y: 1, z: 2 };
  for (const normal of contact.normals!) velocity = resolveWallCollision(velocity, normal, 1).newVelocity;
  assert.deepEqual(velocity, { x: -3, y: -1, z: 2 });
});
