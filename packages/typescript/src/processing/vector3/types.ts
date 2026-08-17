import type { JsonObject, JsonValue } from '../../core/types.js';

export type Vector3Axis = 'x' | 'y' | 'z';
export type ComponentSource = 'observed' | 'derived' | 'constrained' | 'default' | 'missing';

export interface ComponentQuality {
  confidence?: number;
  uncertainty?: number | null;
  flags?: string[];
  error?: string | null;
  metadata?: JsonObject;
}

export interface Vector3Component {
  value?: number;
  source: ComponentSource;
  /** Observation time in milliseconds on a caller-defined, common clock. */
  timestampMs?: number;
  quality?: ComponentQuality;
}

export interface Vector3Components {
  x: Vector3Component;
  y: Vector3Component;
  z: Vector3Component;
}

export interface Vector3Value {
  x: number;
  y: number;
  z: number;
}

export interface Vector3Direction {
  /** Degrees in [0, 360), measured in the x-y plane from +x toward +y. */
  azimuthDeg: number;
  /** Degrees in [-90, 90], measured above the x-y plane toward +z. */
  elevationDeg: number;
}

export type Vector3AssemblyStatus = 'ok' | 'warning' | 'incomplete';

export interface Vector3Measurement {
  kind: 'vector3-measurement';
  quantity: string;
  unit: string;
  coordinateSystem: string;
  components: Vector3Value;
  componentDetails: Vector3Components;
  magnitude: number;
  normalized: Vector3Value | null;
  direction: Vector3Direction | null;
  /** Latest timestamp among timestamped components. */
  timestampMs: number | null;
  componentSkewMs: number | null;
  quality: {
    status: Exclude<Vector3AssemblyStatus, 'incomplete'>;
    flags: string[];
    /** Per-component evidence is preserved; no aggregate "accuracy" is invented. */
    components: Vector3Components;
  };
  metadata?: JsonObject;
}

export interface Vector3AssemblyResult {
  status: Vector3AssemblyStatus;
  flags: string[];
  missingComponents: Vector3Axis[];
  measurement: Vector3Measurement | null;
}

export interface Vector3ComposeInput {
  quantity: string;
  unit: string;
  coordinateSystem: string;
  components: Vector3Components;
  metadata?: JsonObject;
}

export interface Vector3AssemblerOptions {
  maxComponentSkewMs?: number;
}

export interface CoordinateTransform3 {
  id: string;
  from: string;
  to: string;
  /** Row-major 3x3 matrix. */
  matrix: readonly [number, number, number, number, number, number, number, number, number];
  notes?: string;
}

export interface Vector3Arrow {
  id: 'x-component' | 'y-component' | 'z-component' | 'resultant';
  label: string;
  from: Vector3Value;
  to: Vector3Value;
  source?: ComponentSource;
}

export interface Vector3AxisLine {
  id: 'x-axis' | 'y-axis' | 'z-axis';
  label: 'x' | 'y' | 'z';
  direction: Vector3Value;
}

export interface Vector3RenderModel {
  coordinateSystem: string;
  axes: Vector3AxisLine[];
  arrows: Vector3Arrow[];
  annotations: Record<string, JsonValue>;
}
