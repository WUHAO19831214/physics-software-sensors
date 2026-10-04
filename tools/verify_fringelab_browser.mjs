/** Run with AGENT_BROWSER_BIN=/path/to/agent-browser and a built preview at 4173. */
import { execFileSync } from 'node:child_process';
import assert from 'node:assert/strict';
import { writeFileSync, mkdirSync } from 'node:fs';
import path from 'node:path';
const binary = process.env.AGENT_BROWSER_BIN ?? 'agent-browser';
const session = 'fringelab-verification';
const run = (...args) => execFileSync(binary, ['--session', session, ...args], { encoding: 'utf8', timeout: 60000 }).trim();
const results = [];
function ref(role, label) {
  const snapshot = run('snapshot','-i');
  const line = snapshot.split('\n').find(line => line.includes(`${role} "${label}"`) && line.includes('ref='));
  assert.ok(line, `Missing ${role}: ${label}`);
  return '@' + line.match(/ref=([^,\]]+)/)[1];
}
const click = label => run('click',ref('button',label));
const fill = (label,value,role='spinbutton') => run('fill',ref(role,label),String(value));
const evaluate = expression => JSON.parse(JSON.parse(run('eval',`JSON.stringify(${expression})`)));
function check(name, action) { action(); results.push({ check: name, status: 'pass' }); console.log(`PASS: ${name}`); }
const url = process.argv[2] ?? 'http://127.0.0.1:4173';
run('open',url); run('wait','--load','networkidle'); run('set','viewport','1280','900');
check('production page and expected controls',()=>{assert.ok(evaluate('document.body.innerText.includes("FringeLab 可复用工具台")'));assert.equal(evaluate('!!document.querySelector("vite-error-overlay,[data-nextjs-dialog]")'),false);});
check('calculator arithmetic, independent IDs and Esc focus restoration',()=>{
  click('打开计算器');fill('计算表达式','(12+8)/5','textbox');run('press','Enter');assert.equal(evaluate('document.querySelector(".fl-calculator-output").textContent'),'= 4');
  click('打开第二个计算器');assert.equal(evaluate('document.querySelectorAll(".fl-floating").length'),2);assert.equal(evaluate('new Set(Array.from(document.querySelectorAll(".fl-floating input"),e=>e.id)).size'),2);
  run('press','Escape');assert.equal(evaluate('document.querySelectorAll(".fl-floating").length'),1);assert.equal(evaluate('document.activeElement.textContent'),'打开第二个计算器');
  click('关闭 辅助计算器');assert.equal(evaluate('document.activeElement.textContent'),'打开计算器');
});
check('manual ruler confirmation and synthetic optical inversion',()=>{
  click('手动虚拟尺');click('核对并应用尺标');click('核对参数并计算');const text=evaluate('document.querySelector(".measurement").textContent');const wavelength=Number(text.match(/λ ([\d.]+)/)?.[1]);assert.ok(Math.abs(wavelength-650)<13,text);
  fill('缝屏距 L (m)',2);assert.ok(evaluate('document.querySelector(".measurement").textContent.includes("等待")'));click('载入示例');assert.ok(evaluate('document.querySelector("[data-testid=calibration-status]").textContent.includes("未确认")'));
});
check('rotated ROI updates without stale computation',()=>{fill('ROI 角度 (°)',12);assert.equal(evaluate('document.querySelectorAll("svg.fl-overlay polygon").length'),1);fill('ROI 角度 (°)',0);});
check('multi-point manual calibration and editable drafts',()=>{
  click('多点尺标');run('scrollintoview','.image-stage');
  for(const [x,mm] of [[80,0],[330,10],[830,30]]) {fill('下一点读数 (mm)',mm);const rect=evaluate('(()=>{const r=document.querySelector(".image-stage").getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height}})()');run('mouse','move',String(Math.round(rect.x+x/960*rect.w)),String(Math.round(rect.y+401/540*rect.h)));run('mouse','down');run('mouse','up');}
  assert.equal(evaluate('document.querySelectorAll(".anchor-list label").length'),3);click('核对并应用尺标');click('核对参数并计算');assert.ok(evaluate('document.querySelector(".measurement").textContent.includes("λ")'));
});
check('automatic ruler runs in a Worker and stays a candidate',()=>{
  click('载入示例');click('自动检测刻线');run('wait',1200);assert.ok(evaluate('document.querySelector(".status").textContent.includes("核对真实长度")'));assert.ok(evaluate('document.querySelector("[data-testid=calibration-status]").textContent.includes("未确认")'));
});
check('390px layout and floating calculator remain inside viewport',()=>{
  run('set','viewport','390','844');run('scroll','up','2000');click('打开计算器');assert.ok(evaluate('document.documentElement.scrollWidth<=window.innerWidth'));
  const r=evaluate('(()=>{const p=document.querySelector(".fl-floating").getBoundingClientRect();return {left:p.left,right:p.right,top:p.top,bottom:p.bottom}})()');assert.ok(r.left>=0&&r.right<=390&&r.top>=0&&r.bottom<=844,JSON.stringify(r));run('screenshot','/tmp/fringelab-mobile.png');click('关闭 辅助计算器');
});
run('set','viewport','1280','1000');run('scroll','up','2000');click('手动虚拟尺');click('核对并应用尺标');click('核对参数并计算');
const root=path.resolve(new URL('..',import.meta.url).pathname);
mkdirSync(path.join(root,'docs/assets'),{recursive:true});run('screenshot',path.join(root,'docs/assets/fringelab-toolkit.png'),'--full');
const errors=run('errors');assert.equal(errors,'',errors);
writeFileSync(path.join(root,'benchmarks/results/fringelab-browser-verification.json'),JSON.stringify({date:'2026-10-05',url,backend:'agent-browser / headless Chrome',fixture:'synthetic sample, no physical camera',checks:results,consoleErrors:[]},null,2)+'\n');
run('close');
