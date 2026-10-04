'use client';
import { useEffect, useId, useRef, useState, type ReactNode, type RefObject } from 'react';
import { createPortal } from 'react-dom';
import { calculateExpression } from '../core/calculator.js';

export function FloatingPanel({ anchor, title, onClose, children }: { anchor: RefObject<HTMLElement | null>; title: string; onClose(): void; children: ReactNode }) {
  const panel = useRef<HTMLElement>(null);
  const [position, setPosition] = useState({ left: 16, top: 80 });
  const drag = useRef<{ x: number; y: number; left: number; top: number } | null>(null);
  const bounded = (left: number, top: number) => ({ left: Math.max(8, Math.min(left, window.innerWidth - (panel.current?.offsetWidth ?? 300) - 8)), top: Math.max(8, Math.min(top, window.innerHeight - (panel.current?.offsetHeight ?? 400) - 8)) });
  useEffect(() => {
    const place = () => { const a = anchor.current?.getBoundingClientRect(); if (a) setPosition(bounded(a.right + 12, a.top)); };
    const escape = (event: KeyboardEvent) => { if (event.key === 'Escape' && panel.current?.contains(event.target as Node)) { onClose(); anchor.current?.focus(); } };
    const previous = document.activeElement as HTMLElement | null;
    place(); panel.current?.querySelector<HTMLInputElement>('input')?.focus({ preventScroll: true });
    window.addEventListener('resize', place); window.addEventListener('scroll', place, { passive: true }); window.addEventListener('keydown', escape);
    return () => { window.removeEventListener('resize', place); window.removeEventListener('scroll', place); window.removeEventListener('keydown', escape); if (panel.current?.contains(document.activeElement)) previous?.focus(); };
  }, [anchor, onClose]);
  return createPortal(<section ref={panel} className="fl-floating fl-surface" role="dialog" aria-label={title} style={position}>
    <header className="fl-floating-header">
      <span role="button" tabIndex={0} aria-label={`移动 ${title}`} onKeyDown={event => { const delta = { ArrowLeft: [-10, 0], ArrowRight: [10, 0], ArrowUp: [0, -10], ArrowDown: [0, 10] }[event.key]; if (delta) { event.preventDefault(); setPosition(p => bounded(p.left + delta[0]!, p.top + delta[1]!)); } }} onPointerDown={event => { event.currentTarget.setPointerCapture(event.pointerId); drag.current = { x: event.clientX, y: event.clientY, ...position }; }} onPointerMove={event => { if (drag.current) setPosition(bounded(drag.current.left + event.clientX - drag.current.x, drag.current.top + event.clientY - drag.current.y)); }} onPointerUp={() => { drag.current = null; }} onPointerCancel={() => { drag.current = null; }}>{title} ⠿</span>
      <button type="button" className="fl-button" aria-label={`关闭 ${title}`} onClick={() => { onClose(); anchor.current?.focus(); }}>关闭</button>
    </header>{children}
  </section>, document.body);
}

export interface FloatingCalculatorProps { title?: string; triggerLabel?: string; initialExpression?: string; onResult?(value: number, expression: string): void }
export function FloatingCalculator({ title = '辅助计算器', triggerLabel = '打开计算器', initialExpression = '', onResult }: FloatingCalculatorProps) {
  const [open, setOpen] = useState(false), [expression, setExpression] = useState(initialExpression), [result, setResult] = useState('');
  const trigger = useRef<HTMLButtonElement>(null);
  const id = useId();
  const close = useRef(() => setOpen(false));
  const calculate = () => { try { const value = calculateExpression(expression); setResult(`= ${Number(value.toPrecision(12))}`); onResult?.(value, expression); } catch (error) { setResult(error instanceof Error ? error.message : String(error)); } };
  return <>
    <button ref={trigger} type="button" className="fl-button" aria-haspopup="dialog" aria-expanded={open} onClick={() => setOpen(!open)}>{open ? '收起计算器' : triggerLabel}</button>
    {open && <FloatingPanel anchor={trigger} title={title} onClose={close.current}>
      <p className="fl-note">支持四则、括号、^ 乘方和 e 科学计数。</p>
      <label className="fl-field" htmlFor={id}>计算表达式<input id={id} maxLength={300} value={expression} onChange={event => { setExpression(event.target.value); setResult(''); }} onKeyDown={event => { if (event.key === 'Enter') calculate(); }} placeholder="例如：(12 + 8) / 5" /></label>
      <output className="fl-calculator-output" aria-live="polite">{result || '等待计算'}</output>
      <div className="fl-calculator-keys">{['7','8','9','÷','4','5','6','×','1','2','3','−','0','.','^','+','(',')','e','⌫'].map(key => <button className="fl-button" type="button" key={key} onClick={() => { setExpression(value => key === '⌫' ? value.slice(0, -1) : (value + key).slice(0, 300)); setResult(''); }}>{key}</button>)}</div>
      <div className="fl-row"><button className="fl-button fl-primary" type="button" onClick={calculate}>计算</button><button className="fl-button" type="button" onClick={() => { setExpression(''); setResult(''); }}>清空</button></div>
    </FloatingPanel>}
  </>;
}
