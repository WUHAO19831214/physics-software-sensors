/** Language-level skeleton. JSON Schema in /contracts remains authoritative. */

export type JsonValue = string | number | boolean | null | JsonObject | JsonValue[];
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
  clock: unknown;
  artifactStore: unknown;
  logger: unknown;
  cancellation: AbortSignal;
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
  process(input: JsonObject): AsyncIterable<JsonObject>;
}
