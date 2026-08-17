import type { JsonObject } from '../../core/types.js';
import type { ComponentSource, Vector3Component } from './types.js';

/** Convert a successful Number OCR SensorEvent into one vector component. */
export function componentFromNumberOcrEvent(
  event: JsonObject,
  source: Exclude<ComponentSource, 'missing'> = 'observed',
): Vector3Component {
  const measurements = event.measurements;
  if (event.status === 'error' || !Array.isArray(measurements) || measurements.length === 0) {
    return {
      source: 'missing',
      quality: {
        flags: ['ocr-failure'],
        error: typeof event.error === 'object' && event.error !== null && !Array.isArray(event.error)
          ? String(event.error.code ?? 'OCR_ERROR')
          : 'OCR_ERROR',
      },
    };
  }
  const first = measurements[0];
  if (typeof first !== 'object' || first === null || Array.isArray(first) || typeof first.value !== 'number') {
    return { source: 'missing', quality: { flags: ['ocr-measurement-missing'], error: 'OCR_MEASUREMENT_MISSING' } };
  }
  const quality = typeof event.quality === 'object' && event.quality !== null && !Array.isArray(event.quality) ? event.quality : {};
  const time = typeof event.time === 'object' && event.time !== null && !Array.isArray(event.time) ? event.time : {};
  const sourceTimestamp = time.source_timestamp;
  return {
    value: first.value,
    source,
    ...(typeof sourceTimestamp === 'number' ? { timestampMs: sourceTimestamp } : {}),
    quality: {
      ...(typeof quality.confidence === 'number' ? { confidence: quality.confidence } : {}),
      flags: Array.isArray(quality.flags) ? quality.flags.map(String) : [],
      metadata: {
        sensor_event_id: typeof event.event_id === 'string' ? event.event_id : null,
        sensor_status: typeof event.status === 'string' ? event.status : null,
      },
    },
  };
}
