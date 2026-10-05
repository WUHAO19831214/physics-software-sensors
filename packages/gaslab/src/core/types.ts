export interface Vector3D {
  x: number;
  y: number;
  z: number;
}

export interface GasParticle {
  id: number;
  position: Vector3D;
  velocity: Vector3D;
  mass: number;
  radius: number;
}

export interface BoxContainer {
  type: 'box';
  width: number;
  height: number;
  depth: number;
}

export interface CylinderContainer {
  type: 'cylinder';
  radius: number;
  height: number;
}

export interface CapsuleContainer {
  type: 'capsule';
  radius: number;
  cylinderHeight: number;
}

export type ContainerGeometry = BoxContainer | CylinderContainer | CapsuleContainer;

export interface SpeedCalibration {
  referenceTemperatureK: number;
  referenceRmsSpeed: number;
}

export interface GasStatistics {
  temperatureK: number;
  collisionCountTotal: number;
  collisionFrequencyHz: number;
  meanSpeed: number;
  rmsSpeed: number;
  microscopicImpulsePressure: number;
  pedagogicalPressureRatio: number;
  stateEquationPressure?: number;
}

export interface GasSimulationSnapshot {
  timestamp: number;
  stepIndex: number;
  temperatureK: number;
  particleCount: number;
  particles: ReadonlyArray<GasParticle>;
  statistics: GasStatistics;
}

export interface GasSimulationConfig {
  particleCount: number;
  particleMass: number;
  particleRadius?: number;
  container: ContainerGeometry;
  initialTemperatureK: number;
  speedCalibration?: SpeedCalibration;
  randomSeed?: number;
  frequencyWindowSeconds?: number;
}

export type SimulationMode = 'live' | 'replay' | 'manual';

export interface ExperimentDataPoint {
  timestamp: number;
  temperatureK: number;
  pressureKPa?: number;
  realSensorPressure?: number;
}
