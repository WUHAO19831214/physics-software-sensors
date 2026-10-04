/** Local synthetic performance evidence, not a real-photo accuracy benchmark. */
import { performance } from 'node:perf_hooks';
import os from 'node:os';
import { writeFileSync } from 'node:fs';
import { extractStripProfile } from '../packages/fringelab/dist/src/core/signal.js';
import { detectPhysicalRuler } from '../packages/fringelab/dist/src/core/ruler-detection.js';
import { simulateDiffraction } from '../packages/fringelab/dist/src/core/simulator.js';
import { syntheticRuler } from '../packages/fringelab/dist/tests/fixtures/scenes.js';
const simulated = simulateDiffraction({ kind:'double-slit',width:960,height:540,mmPerPixel:.04,slitWidthMm:.04,slitSeparationMm:.25,screenDistanceM:1.5,wavelengthNm:650,seed:9173,noiseStd:.008,gamma:1.2,saturationLevel:.9 });
const ruler = syntheticRuler({ body:[235,235,230],ink:[18,18,18] });
function measure(action) {
  for(let i=0;i<5;i++) action();
  const values=Array.from({length:30},()=>{const start=performance.now();action();return performance.now()-start;}).sort((a,b)=>a-b);
  return { samples:values.length,warmup:5,median_ms:values[14],p95_ms:values[28],min_ms:values[0],max_ms:values.at(-1) };
}
const result={date:'2026-10-05',environment:{node:process.version,platform:process.platform,arch:process.arch,cpu:os.cpus()[0]?.model},kind:'local synthetic algorithm latency',strip_profile:measure(()=>extractStripProfile(simulated.frame,{channel:'r',roi:{centerX:480,centerY:240,width:768,height:64,angleDeg:0}})),ruler_ticks:measure(()=>detectPhysicalRuler(ruler,{sourceType:'image'})),ruler_size:{width:ruler.width,height:ruler.height},profile_size:{width:960,height:540},real_photo_error:'not measured',hardware_precision:'not measured'};
writeFileSync(new URL('../benchmarks/results/fringelab-latency.json',import.meta.url),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
