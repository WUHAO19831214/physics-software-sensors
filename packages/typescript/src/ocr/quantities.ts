/**
 * Physical quantities extractor with unit anchoring and range constraints.
 * Extracted and generalized from Charles's Law and DISLab classroom sensor bridges.
 */

import { normalizeOcrText } from './number.js';

export interface QuantitySpec {
  name: string;
  units: readonly string[];
  range: [number, number];
  keywords?: readonly string[];
  /** Convert matched value from secondary unit to primary unit (e.g. Pa -> kPa: 0.001) */
  unitConversions?: Record<string, number>;
  primaryUnit?: string;
}

export interface ExtractedQuantityValue {
  name: string;
  value: number;
  unit: string | null;
  rawTextMatch: string;
}

export interface QuantityExtractionResult {
  quantities: Record<string, ExtractedQuantityValue>;
  rawText: string;
  cleanText: string;
}

/** Pre-configured specifications for common thermal gas sensors (pressure & temperature). */
export const GAS_LAB_QUANTITY_SPECS: Record<'pressure' | 'temperature', QuantitySpec> = {
  pressure: {
    name: 'pressure',
    units: ['kPa', 'kpa', 'KPa', 'Pa', 'pa'],
    range: [50, 300],
    keywords: ['压强', '强', 'P', 'p'],
    unitConversions: {
      Pa: 0.001,
      pa: 0.001,
    },
    primaryUnit: 'kPa',
  },
  temperature: {
    name: 'temperature',
    units: ['K', 'k', '℃', '°C', 'C'],
    range: [-50, 500],
    keywords: ['温度', '度', 'T', 't'],
    primaryUnit: 'K',
  },
};

/**
 * Normalizes text while preserving unit labels (unlike single-number normalization
 * which strips alphabets).
 */
export function normalizeQuantityText(text: string): string {
  return text
    .replace(/[Oo](?=\d|\s*k?pa|\s*[k℃°c])/gi, '0')
    .replace(/[Il|](?=\d)/g, '1')
    .replace(/[，,]/g, '.')
    .replace(/：/g, ':');
}

/**
 * Extracts multiple structured physical quantities with explicit units from OCR text.
 * Strictly respects word boundaries and physical value intervals to reject stray alphanumeric noise.
 */
export function extractQuantities(
  text: string,
  specs: readonly QuantitySpec[],
): QuantityExtractionResult {
  const clean = normalizeQuantityText(text);
  const quantities: Record<string, ExtractedQuantityValue> = {};

  for (const spec of specs) {
    let matched: ExtractedQuantityValue | null = null;

    // 1. Unit anchoring: look for numbers immediately followed by defined units
    const unitPattern = spec.units
      .map((u) => u.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'))
      .join('|');
    const unitRegex = new RegExp(
      `\\b([+-]?(?:\\d+\\.\\d+|\\d+))\\s*(${unitPattern})(?![A-Za-z0-9])`,
      'gi',
    );

    for (const m of clean.matchAll(unitRegex)) {
      if (!m[1]) continue;
      let rawVal = parseFloat(m[1]);
      const matchedUnit = m[2] ?? null;
      if (Number.isFinite(rawVal)) {
        if (matchedUnit && spec.unitConversions && spec.unitConversions[matchedUnit] !== undefined) {
          rawVal = rawVal * spec.unitConversions[matchedUnit];
        }
        if (rawVal >= spec.range[0] && rawVal <= spec.range[1]) {
          matched = {
            name: spec.name,
            value: Number(rawVal.toFixed(2)),
            unit: matchedUnit,
            rawTextMatch: m[0],
          };
          break;
        }
      }
    }

    // 2. Keyword anchoring (e.g. "压强: 101.3")
    if (!matched && spec.keywords && spec.keywords.length > 0) {
      const kwPattern = spec.keywords
        .map((k) => k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'))
        .join('|');
      const kwRegex = new RegExp(
        `(?:${kwPattern})[:\\s]*\\b([+-]?(?:\\d+\\.\\d+|\\d+))\\b`,
        'i',
      );
      const kwMatch = clean.match(kwRegex);
      if (kwMatch && kwMatch[1]) {
        const rawVal = parseFloat(kwMatch[1]);
        if (Number.isFinite(rawVal) && rawVal >= spec.range[0] && rawVal <= spec.range[1]) {
          matched = {
            name: spec.name,
            value: Number(rawVal.toFixed(2)),
            unit: spec.primaryUnit ?? null,
            rawTextMatch: kwMatch[0],
          };
        }
      }
    }

    // 3. Standalone float fallback within bounds (excluding already claimed values)
    if (!matched) {
      const standaloneMatches = clean.matchAll(/\b[+-]?(?:\d+\.\d+|\d+)\b/g);
      for (const sm of standaloneMatches) {
        const val = parseFloat(sm[0]);
        if (Number.isFinite(val) && val >= spec.range[0] && val <= spec.range[1]) {
          // Verify not already used by another quantity
          const alreadyUsed = Object.values(quantities).some((q) => q.value === val);
          if (!alreadyUsed) {
            matched = {
              name: spec.name,
              value: Number(val.toFixed(2)),
              unit: null,
              rawTextMatch: sm[0],
            };
            break;
          }
        }
      }
    }

    if (matched) {
      quantities[spec.name] = matched;
    }
  }

  return {
    quantities,
    rawText: text,
    cleanText: clean,
  };
}
