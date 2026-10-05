import { test } from 'node:test';
import assert from 'node:assert/strict';
import { resolveWallCollision, calculateKineticEnergy } from '../src/physics/collisions.js';
import { createVector3D, lengthSqVector3D } from '../src/core/vector3d.js';

test('Specular elastic wall collision strictly conserves kinetic energy', () => {
  const mass = 2.0;
  // Particle moving right-down towards ground wall (inward normal = [0, 1, 0])
  const v = createVector3D(3.0, -4.0, 0.0);
  const normal = createVector3D(0.0, 1.0, 0.0);

  const initialEnergy = calculateKineticEnergy(mass, v);
  const response = resolveWallCollision(v, normal, mass);

  // Normal component (-4) should invert to (+4)
  assert.equal(response.newVelocity.x, 3.0);
  assert.equal(response.newVelocity.y, 4.0);
  assert.equal(response.newVelocity.z, 0.0);

  // Kinetic energy strictly conserved
  const finalEnergy = calculateKineticEnergy(mass, response.newVelocity);
  assert.equal(finalEnergy, initialEnergy);

  // Impulse: 2 * mass * |v_n| = 2 * 2.0 * 4.0 = 16.0
  assert.equal(response.impulse, 16.0);
});

test('Particle moving away from wall produces no collision or impulse', () => {
  const mass = 1.0;
  const v = createVector3D(0.0, 5.0, 0.0);
  const inwardNormal = createVector3D(0.0, 1.0, 0.0); // already moving along inward normal

  const response = resolveWallCollision(v, inwardNormal, mass);
  assert.equal(response.impulse, 0);
  assert.equal(response.newVelocity.y, 5.0);
});

test('Arbitrary oblique 3D collision preserves speed and momentum balance', () => {
  const mass = 1.5;
  const v = createVector3D(1.2, -2.4, 3.6);
  // Inward normal at 45 degrees in XY plane
  const invSqrt2 = 1 / Math.SQRT2;
  const normal = createVector3D(invSqrt2, invSqrt2, 0);

  const response = resolveWallCollision(v, normal, mass);

  // Speed magnitude must be strictly identical
  const v0Sq = lengthSqVector3D(v);
  const v1Sq = lengthSqVector3D(response.newVelocity);
  assert.ok(Math.abs(v1Sq - v0Sq) < 1e-12);
  assert.ok(response.impulse > 0);
});
