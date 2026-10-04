/** Verify actual local/published Pages and GitHub README rendering. */
import { execFileSync } from 'node:child_process';
import assert from 'node:assert/strict';
import { writeFileSync, readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
const binary = process.env.AGENT_BROWSER_BIN ?? 'agent-browser';
const session = 'fringelab-publication';
const run = (...args) => execFileSync(binary, ['--session',session,...args], {encoding:'utf8',timeout:60000}).trim();
const evaluate = expression => JSON.parse(JSON.parse(run('eval',`JSON.stringify(${expression})`)));
const base = (process.argv[2] ?? 'http://127.0.0.1:4180').replace(/\/$/, '');
const results = [];
const ids = ['camera.capture','screen.capture','ocr.number','tracker.color-marker','tracker.spot-centroid','tracker.template','tracker.yolo','vector.compose-3d','image.strip-profile','vision.ruler-ticks','calibration.scale-1d','signal.profile-features','optics.fringe-wavelength'];
try {
  for(const [language,route] of [['en','/'],['zh-CN','/zh-CN/'],['ja','/ja/']]) {
    const url=base+route;run('open',url);run('wait','--load','networkidle');run('set','viewport','1280','900');
    const data=evaluate('({text:document.body.innerText,headings:Array.from(document.querySelectorAll("h3"),e=>e.textContent),images:Array.from(document.images,e=>({src:e.getAttribute("src"),width:e.naturalWidth,loaded:e.complete})),links:Array.from(document.querySelectorAll("a"),e=>e.getAttribute("href")),source:document.querySelector("meta[name=source-readme-sha256]")?.content})');
    const sourceFile=language==='en'?'README.md':`README.${language}.md`;
    assert.equal(data.source,createHash('sha256').update(readFileSync(new URL('../'+sourceFile,import.meta.url))).digest('hex'),`${language}: stale deployed source`);
    assert.ok(ids.every(id=>data.text.includes(id)),`${language}: missing capability`);
    assert.ok(data.text.includes('13/13')&&data.text.includes('@physics-software-sensors/fringelab'));
    assert.ok(data.headings.some(text=>text.startsWith('FringeLab ')),`${language}: missing visible component heading`);
    const images=data.images.filter(image=>image.src.includes('capability-showcase.png')||image.src.includes('fringelab-toolkit.png'));
    assert.equal(images.length,2);assert.ok(images.every(image=>image.loaded&&image.width>0),`${language}: unloaded images`);
    assert.ok(data.links.some(link=>link.includes('examples/web-fringelab-toolkit/README.md')));
    evaluate('(()=>{Array.from(document.querySelectorAll("h3")).find(e=>e.textContent.startsWith("FringeLab ")).scrollIntoView();return true;})()');
    run('screenshot',`/tmp/fringelab-publication-${language}.png`);
    results.push({language,url,capabilities:'13/13',images:'2/2 loaded',componentTable:'present',source_readme_sha256:data.source});console.log(`PASS ${language}: visible toolkit introduction, 13 capabilities and both images`);
  }
  if(base.startsWith('https://')) {
    const url='https://github.com/WUHAO19831214/physics-software-sensors';run('open',url);run('wait','--load','networkidle');
    const present=evaluate('Array.from(document.querySelectorAll("h3")).some(e=>e.textContent.includes("FringeLab image and optics toolkit"))');
    assert.equal(present,true,'GitHub default branch README has no toolkit showcase');
    results.push({github:url,componentHeading:'visible'});console.log('PASS GitHub: component heading visible on default branch');
  }
  const report={verified_at:new Date().toISOString(),base,checks:results};
  if(process.argv[3])writeFileSync(process.argv[3],JSON.stringify(report,null,2)+'\n');
} finally {run('close');}
