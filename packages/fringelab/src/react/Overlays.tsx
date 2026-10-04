'use client';
import { useRef, type PointerEvent } from 'react';
import { ROI_CORNERS, roiCornerPoint, resizeRoiFromCorner, type Point, type RoiCorner, type RoiGeometry } from '../core/roi.js';
import { generateRulerTicks, moveRuler, resizeRulerEndpoint, type RulerCalibration, type RulerHandle } from '../core/ruler.js';
import { resolveRulerThemeFromSamples, type RulerTheme, type RulerDetectionResult, snapRulerToDetection } from '../core/ruler-detection.js';

function pointer(event: PointerEvent<SVGElement>): Point {
  const svg = event.currentTarget.ownerSVGElement ?? event.currentTarget as SVGSVGElement;
  const matrix = svg.getScreenCTM(); if (!matrix) return { x: 0, y: 0 };
  const p = new DOMPoint(event.clientX, event.clientY).matrixTransform(matrix.inverse()); return { x: p.x, y: p.y };
}
type Size = { width: number; height: number };
export function RoiOverlay({ roi, size, onChange, interactive = true }: { roi: RoiGeometry; size: Size; onChange?(roi: RoiGeometry): void; interactive?: boolean }) {
  const drag = useRef<{ kind: RoiCorner | 'move' | 'rotate'; start: Point; initial: RoiGeometry } | null>(null);
  const begin = (kind: RoiCorner | 'move' | 'rotate', event: PointerEvent<SVGElement>) => { if (!interactive) return; event.currentTarget.setPointerCapture(event.pointerId); drag.current = { kind, start: pointer(event), initial: { ...roi } }; };
  const move = (event: PointerEvent<SVGElement>) => {
    const d = drag.current; if (!d || !onChange) return;
    const p = pointer(event);
    if (d.kind === 'move') onChange({ ...d.initial, centerX: d.initial.centerX + p.x - d.start.x, centerY: d.initial.centerY + p.y - d.start.y });
    else if (d.kind === 'rotate') onChange({ ...d.initial, angleDeg: Math.atan2(p.y - d.initial.centerY, p.x - d.initial.centerX) * 180 / Math.PI + 90 });
    else onChange(resizeRoiFromCorner(d.initial, d.kind, p, { minWidth: 8, minHeight: 4, maxWidth: size.width * 2, maxHeight: size.height * 2 }));
  };
  const release = () => { drag.current = null; };
  const handles = ROI_CORNERS.map(c => roiCornerPoint(roi, c));
  const radians = roi.angleDeg * Math.PI / 180;
  const rotate = { x: roi.centerX + Math.sin(radians) * (roi.height / 2 + 30), y: roi.centerY - Math.cos(radians) * (roi.height / 2 + 30) };
  return <svg className="fl-overlay" viewBox={`0 0 ${size.width} ${size.height}`} aria-label="旋转 ROI" onPointerMove={move} onPointerUp={release} onPointerCancel={release}>
    <polygon points={handles.map(p => `${p.x},${p.y}`).join(' ')} fill="#35e1c018" stroke="#35e1c0" strokeWidth={2} style={{ pointerEvents: interactive ? 'all' : 'none', cursor: 'move' }} onPointerDown={e => begin('move', e)} />
    {interactive && ROI_CORNERS.map((c, i) => <circle key={c} cx={handles[i]!.x} cy={handles[i]!.y} r={7} fill="#fff" stroke="#087466" style={{ pointerEvents: 'all', cursor: 'nwse-resize' }} onPointerDown={e => begin(c, e)} />)}
    {interactive && <circle cx={rotate.x} cy={rotate.y} r={8} fill="#35e1c0" style={{ pointerEvents: 'all', cursor: 'grab' }} onPointerDown={e => begin('rotate', e)} />}
  </svg>;
}
export function RulerOverlay({ ruler, size, onChange, detection = null, interactive = true, theme = resolveRulerThemeFromSamples([200], 'auto') }: { ruler: RulerCalibration; size: Size; onChange?(ruler: RulerCalibration): void; detection?: RulerDetectionResult | null; interactive?: boolean; theme?: RulerTheme }) {
  const drag = useRef<{ kind: RulerHandle; start: Point; initial: RulerCalibration } | null>(null);
  const angle = Math.atan2(ruler.end.y - ruler.start.y, ruler.end.x - ruler.start.x);
  const normal = { x: -Math.sin(angle) * (ruler.tickSide ?? -1), y: Math.cos(angle) * (ruler.tickSide ?? -1) };
  const begin = (kind: RulerHandle, event: PointerEvent<SVGElement>) => { if (!interactive) return; event.currentTarget.setPointerCapture(event.pointerId); drag.current = { kind, start: pointer(event), initial: structuredClone(ruler) }; };
  const move = (event: PointerEvent<SVGElement>) => {
    const d = drag.current; if (!d || !onChange) return;
    const p = pointer(event);
    let next = d.kind === 'body' ? moveRuler(d.initial, p.x - d.start.x, p.y - d.start.y, size) : resizeRulerEndpoint(d.initial, d.kind, p, event.shiftKey ? 15 : undefined);
    const matrix = (event.currentTarget as SVGSVGElement).getScreenCTM();
    const displayScale = matrix ? Math.hypot(matrix.a, matrix.b) : 1;
    if (detection) next = snapRulerToDetection(next, detection, { tickSnapEnabled: true, numberSnapEnabled: true, altKey: event.altKey, displayScale }).ruler;
    onChange(next);
  };
  const release = () => { drag.current = null; };
  return <svg className="fl-overlay" viewBox={`0 0 ${size.width} ${size.height}`} aria-label="虚拟刻度尺" onPointerMove={move} onPointerUp={release} onPointerCancel={release}>
    <line x1={ruler.start.x} y1={ruler.start.y} x2={ruler.end.x} y2={ruler.end.y} stroke={theme.outline} strokeWidth={6} />
    <line x1={ruler.start.x} y1={ruler.start.y} x2={ruler.end.x} y2={ruler.end.y} stroke={theme.stroke} strokeWidth={2} style={{ pointerEvents: interactive ? 'stroke' : 'none', cursor: 'move' }} onPointerDown={e => begin('body', e)} />
    {generateRulerTicks(ruler).map(t => { const length = t.kind === 'major' ? 24 : t.kind === 'medium' ? 16 : 9; return <g key={t.millimetre}>
      <line x1={t.point.x} y1={t.point.y} x2={t.point.x + normal.x * length} y2={t.point.y + normal.y * length} stroke={theme.outline} strokeWidth={5} />
      <line x1={t.point.x} y1={t.point.y} x2={t.point.x + normal.x * length} y2={t.point.y + normal.y * length} stroke={theme.stroke} strokeWidth={2} />
      {t.kind === 'major' && <text x={t.point.x + normal.x * 38} y={t.point.y + normal.y * 38} fill={theme.labelText} stroke={theme.labelFill} paintOrder="stroke" strokeWidth={4} textAnchor="middle" fontSize={13}>{t.millimetre + (ruler.originMm ?? 0)}</text>}
    </g>; })}
    {interactive && (['start', 'end'] as const).map(kind => <circle key={kind} cx={ruler[kind].x} cy={ruler[kind].y} r={8} fill={theme.handleFill} stroke={theme.outline} strokeWidth={3} style={{ pointerEvents: 'all', cursor: 'crosshair' }} onPointerDown={e => begin(kind, e)} />)}
  </svg>;
}
