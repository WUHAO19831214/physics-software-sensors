export type JsonPrimitive = string | number | boolean | null;
export type JsonValue = JsonPrimitive | JsonObject | JsonValue[];
export interface JsonObject { [key: string]: JsonValue }

export type LifecycleState =
  | 'created'
  | 'configured'
  | 'running'
  | 'stopping'
  | 'stopped'
  | 'error';

export interface SensorDescriptor {
  sensorId: string;
  version: string;
  category: 'source' | 'processor' | 'fusion';
  inputKinds: string[];
  outputKinds: string[];
  capabilities: string[];
  configSchemaVersion: string;
  evidenceLevel: 'documented-prototype' | 'source-tested' | 'replay-benchmarked' | 'hardware-validated';
}

export interface ConfigResult {
  accepted: boolean;
  effectiveConfig: JsonObject;
  warnings: string[];
}

export interface SensorContext {
  runId: string;
  cancellation?: AbortSignal;
}

export interface HealthSnapshot {
  state: LifecycleState;
  processedCount: number;
  droppedCount: number;
  lostCount: number;
  errorCount: number;
  actualRateHz?: number;
  latencyMs: Record<string, number>;
  lastError?: JsonObject;
}

export interface RuntimeFramePacket {
  frameId: string;
  runId: string;
  sequence: number;
  observedAt: string;
  monotonicNs: number;
  sourceTimestamp?: number | null;
  sourceSensorId: string;
  media: {
    kind: 'camera-frame' | 'screen-frame' | 'image-frame';
    width: number;
    height: number;
    mediaType: string;
    colorSpace: string;
  };
  artifactUri: string;
  droppedSinceLast?: number;
}

export interface SensorLifecycle {
  describe(): SensorDescriptor;
  configure(config: JsonObject): ConfigResult;
  start(context: SensorContext): Promise<void>;
  health(): HealthSnapshot;
  stop(): Promise<void>;
}

export interface SourceSensor extends SensorLifecycle {
  read(): AsyncIterable<JsonObject>;
}

export interface ProcessorSensor extends SensorLifecycle {
  process(input: RuntimeFramePacket): AsyncIterable<JsonObject>;
}
