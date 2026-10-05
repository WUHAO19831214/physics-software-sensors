/** Structured OCR candidates. Parsing alone does not establish measurement accuracy. */
export interface QuantitySpec {
  name: string;
  units: readonly string[];
  /** Range in the returned unit, after any configured conversion. */
  range: [number, number];
  keywords?: readonly string[];
  unitConversions?: Record<string, number>;
  primaryUnit?: string;
  /** Additional bounds for a returned unit (e.g. nonnegative absolute temperature). */
  unitRanges?: Record<string, [number, number]>;
  /** Opt in only for a dedicated, unitless ROI. Disabled for mixed instrument text. */
  allowUnitless?: boolean;
}

export interface ExtractedQuantityValue {
  name: string;
  value: number;
  /** Unit of value; sourceUnit preserves the spelling/unit before conversion. */
  unit: string | null;
  sourceUnit: string | null;
  rawTextMatch: string;
}

export interface QuantityExtractionResult {
  quantities: Record<string, ExtractedQuantityValue>;
  rawText: string;
  cleanText: string;
}

export const GAS_LAB_QUANTITY_SPECS: Record<'pressure' | 'temperature', QuantitySpec> = {
  pressure: {
    name: 'pressure', units: ['kPa', 'Pa'], range: [50, 300],
    keywords: ['压强', '压力', 'P'], unitConversions: { Pa: 0.001 }, primaryUnit: 'kPa',
  },
  temperature: {
    name: 'temperature', units: ['K', '℃', '°C', 'C'], range: [-50, 500],
    keywords: ['温度', 'T'], primaryUnit: 'K', unitRanges: { K: [0, 500] },
  },
};

export function normalizeQuantityText(text: string): string {
  return text
    .replace(/(?<=\d)[Oo](?=\d|[.,\s]|$)/g, '0')
    .replace(/[Oo](?=\d)/g, '0')
    .replace(/[Il|](?=\d)/g, '1')
    .replace(/[，,]/g, '.')
    .replace(/：/g, ':')
    .replace(/[−–]/g, '-');
}

const escapeRegex = (value: string): string => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
// The left boundary precedes the sign, so -20 never becomes +20.
const NUMBER = '(?<![A-Za-z0-9_.+\\-])([+\\-]?(?:\\d+(?:\\.\\d*)?|\\.\\d+)(?:[eE][+\\-]?\\d+)?)';

export function extractQuantities(text: string, specs: readonly QuantitySpec[]): QuantityExtractionResult {
  const clean = normalizeQuantityText(text);
  const quantities: Record<string, ExtractedQuantityValue> = {};
  const claimed: Array<[number, number]> = [];
  const available = (start: number, end: number): boolean =>
    !claimed.some(([a, b]) => start < b && end > a);

  const store = (spec: QuantitySpec, m: RegExpMatchArray, rawUnit: string | null, assumedUnit: string | null = null): boolean => {
    const start = m.index ?? 0;
    if (!available(start, start + m[0].length)) return false;
    let value = Number(m[1]);
    let unit = rawUnit ?? assumedUnit;
    if (rawUnit) {
      const canonical = spec.units.find(u => u.toLowerCase() === rawUnit.toLowerCase());
      if (!canonical) return false;
      unit = canonical;
      const conversion = Object.entries(spec.unitConversions ?? {})
        .find(([u]) => u.toLowerCase() === rawUnit.toLowerCase());
      if (conversion) {
        if (!spec.primaryUnit || !Number.isFinite(conversion[1])) return false;
        value *= conversion[1];
        unit = spec.primaryUnit;
      }
    }
    const unitRange = unit ? spec.unitRanges?.[unit] : undefined;
    if (!Number.isFinite(value) || value < spec.range[0] || value > spec.range[1]
      || (unitRange && (value < unitRange[0] || value > unitRange[1]))) return false;
    quantities[spec.name] = {
      name: spec.name, value: Number(value.toFixed(2)), unit,
      sourceUnit: rawUnit, rawTextMatch: m[0],
    };
    claimed.push([start, start + m[0].length]);
    return true;
  };

  // Explicit units take precedence across every spec, independent of spec order.
  for (const spec of specs) {
    if (!spec.units.length) continue;
    const units = [...spec.units].sort((a, b) => b.length - a.length).map(escapeRegex).join('|');
    const regex = new RegExp(`${NUMBER}\\s*(${units})(?![A-Za-z0-9_])`, 'gi');
    for (const m of clean.matchAll(regex)) {
      if (store(spec, m, m[2] ?? null)) break;
    }
  }

  for (const spec of specs) {
    if (quantities[spec.name] || !spec.keywords?.length) continue;
    const keywords = spec.keywords.map(escapeRegex).join('|');
    const regex = new RegExp(`(?<![A-Za-z0-9_])(?:${keywords})[:\\s]*${NUMBER}(?![A-Za-z0-9_.])`, 'gi');
    for (const m of clean.matchAll(regex)) {
      // Never reinterpret an explicitly labelled, rejected value as a unitless one.
      if (/^\s*[A-Za-z%°℃]/.test(clean.slice((m.index ?? 0) + m[0].length))) continue;
      if (store(spec, m, null, spec.primaryUnit ?? null)) break;
    }
  }

  // Fallback is restricted to a dedicated numeric ROI with no labels/noise.
  if (/^[\s\d.eE+\-;:]+$/.test(clean)) {
    for (const spec of specs) {
      if (quantities[spec.name] || !spec.allowUnitless) continue;
      for (const m of clean.matchAll(new RegExp(`${NUMBER}(?![A-Za-z0-9_.])`, 'g'))) {
        if (store(spec, m, null)) break;
      }
    }
  }
  return { quantities, rawText: text, cleanText: clean };
}
