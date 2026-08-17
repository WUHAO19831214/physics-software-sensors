import type {
  ComponentQuality,
  Vector3AssemblerOptions,
  Vector3AssemblyResult,
  Vector3Axis,
  Vector3Component,
  Vector3ComposeInput,
  Vector3Components,
  Vector3Direction,
  Vector3Measurement,
  Vector3Value,
} from './types.js';

const AXES: readonly Vector3Axis[] = ['x', 'y', 'z'];
const ZERO_TOLERANCE = Number.EPSILON;

function validateComponent(axis: Vector3Axis, component: Vector3Component): void {
  if (component.source === 'missing') {
    if (component.value !== undefined) throw new Error(`${axis}: missing component cannot carry a value`);
    return;
  }
  if (component.value === undefined || !Number.isFinite(component.value)) {
    throw new Error(`${axis}: ${component.source} component requires a finite value`);
  }
  if (component.timestampMs !== undefined && !Number.isFinite(component.timestampMs)) {
    throw new Error(`${axis}: timestampMs must be finite`);
  }
  validateQuality(axis, component.quality);
}

function validateQuality(axis: Vector3Axis, quality: ComponentQuality | undefined): void {
  if (!quality) return;
  if (quality.confidence !== undefined && (!Number.isFinite(quality.confidence) || quality.confidence < 0 || quality.confidence > 1)) {
    throw new Error(`${axis}: confidence must be within [0, 1]`);
  }
  if (quality.uncertainty !== undefined && quality.uncertainty !== null && (!Number.isFinite(quality.uncertainty) || quality.uncertainty < 0)) {
    throw new Error(`${axis}: uncertainty must be non-negative`);
  }
}

function directionFor(value: Vector3Value, magnitude: number): Vector3Direction | null {
  if (magnitude <= ZERO_TOLERANCE) return null;
  const radiansToDegrees = 180 / Math.PI;
  const rawAzimuth = Math.atan2(value.y, value.x) * radiansToDegrees;
  return {
    azimuthDeg: rawAzimuth < 0 ? rawAzimuth + 360 : rawAzimuth,
    elevationDeg: Math.atan2(value.z, Math.hypot(value.x, value.y)) * radiansToDegrees,
  };
}

function qualityFlags(components: Vector3Components): string[] {
  const flags: string[] = [];
  for (const axis of AXES) {
    const quality = components[axis].quality;
    for (const flag of quality?.flags ?? []) flags.push(`component-${axis}:${flag}`);
    if (quality?.error) flags.push(`component-${axis}:error`);
  }
  return flags;
}

export function composeVector3(
  input: Vector3ComposeInput,
  options: Vector3AssemblerOptions = {},
): Vector3AssemblyResult {
  const maxComponentSkewMs = options.maxComponentSkewMs ?? 150;
  if (!Number.isFinite(maxComponentSkewMs) || maxComponentSkewMs < 0) {
    throw new Error('maxComponentSkewMs must be a finite non-negative number');
  }

  for (const axis of AXES) validateComponent(axis, input.components[axis]);
  const missingComponents = AXES.filter((axis) => input.components[axis].source === 'missing');
  if (missingComponents.length > 0) {
    return {
      status: 'incomplete',
      flags: missingComponents.map((axis) => `component-${axis}:missing`),
      missingComponents,
      measurement: null,
    };
  }

  const value: Vector3Value = {
    x: input.components.x.value!,
    y: input.components.y.value!,
    z: input.components.z.value!,
  };
  const magnitude = Math.hypot(value.x, value.y, value.z);
  const normalized = magnitude <= ZERO_TOLERANCE
    ? null
    : { x: value.x / magnitude, y: value.y / magnitude, z: value.z / magnitude };
  const timestamps = AXES
    .map((axis) => input.components[axis].timestampMs)
    .filter((timestamp): timestamp is number => timestamp !== undefined);
  const timestampMs = timestamps.length > 0 ? Math.max(...timestamps) : null;
  const componentSkewMs = timestamps.length > 1 ? Math.max(...timestamps) - Math.min(...timestamps) : null;
  const flags = qualityFlags(input.components);
  if (componentSkewMs !== null && componentSkewMs > maxComponentSkewMs) flags.push('component-time-skew');
  if (normalized === null) flags.push('zero-vector');
  const status = flags.length > 0 ? 'warning' : 'ok';

  const measurement: Vector3Measurement = {
    kind: 'vector3-measurement',
    quantity: input.quantity,
    unit: input.unit,
    coordinateSystem: input.coordinateSystem,
    components: value,
    componentDetails: input.components,
    magnitude,
    normalized,
    direction: directionFor(value, magnitude),
    timestampMs,
    componentSkewMs,
    quality: { status, flags: [...flags], components: input.components },
    ...(input.metadata === undefined ? {} : { metadata: input.metadata }),
  };
  return { status, flags, missingComponents: [], measurement };
}

export class Vector3Assembler {
  readonly maxComponentSkewMs: number;

  constructor(options: Vector3AssemblerOptions = {}) {
    this.maxComponentSkewMs = options.maxComponentSkewMs ?? 150;
    if (!Number.isFinite(this.maxComponentSkewMs) || this.maxComponentSkewMs < 0) {
      throw new Error('maxComponentSkewMs must be a finite non-negative number');
    }
  }

  compose(input: Vector3ComposeInput): Vector3AssemblyResult {
    return composeVector3(input, { maxComponentSkewMs: this.maxComponentSkewMs });
  }
}
