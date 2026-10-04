#!/usr/bin/env python3
"""Build FringeLab/core tgz, two documentation bundles and a clean-install consumer."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import zipfile

ROOT=Path(__file__).resolve().parents[1]
def run(*args,cwd=ROOT):
    return subprocess.run(args,cwd=cwd,check=True,text=True,capture_output=True).stdout.strip()
def record(path):
    return {'filename':path.name,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
def bundle(sensor_id,output,sha):
    name=f'{sensor_id}-0.1.0.zip';target=output/name
    files=run('git','ls-files',f'sensors/{sensor_id}','examples/web-fringelab-toolkit').splitlines()
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as archive:
        for relative in files:
            p=ROOT/relative
            if not p.is_file() or p.name=='package-lock.json':continue
            dest='sensor/'+relative.split('/',2)[2] if relative.startswith('sensors/') else 'example/'+relative.split('/',2)[2]
            value=p.read_bytes()
            if dest=='example/package.json':
                package=json.loads(value);package['dependencies']['@physics-software-sensors/core']='file:../physics-software-sensors-core-0.3.0.tgz';package['dependencies']['@physics-software-sensors/fringelab']='file:../physics-software-sensors-fringelab-0.1.0.tgz';value=(json.dumps(package,indent=2)+'\n').encode()
            archive.writestr(dest,value)
        archive.writestr('README.md',f'# {sensor_id} 0.1.0\n\n[Sensor Page](sensor/README.md) · [Source](sensor/SOURCE.md) · [Install](INSTALL.md)\n\nDocumentation/example bundle; implementation comes from the two accompanying tgz files. Canonical links: https://github.com/WUHAO19831214/physics-software-sensors/tree/{sha}/sensors/{sensor_id}\n')
        archive.writestr('INSTALL.md','Place both accompanying tgz files beside this INSTALL.md, then run `cd example && npm install && npm run dev`. The example package.json points to those local tgz files. Its README also documents running from the source repository. No registry or server upload is required.\n')
        archive.writestr('DEPENDENCIES.json',json.dumps({'required_packages':['@physics-software-sensors/core 0.3.0','@physics-software-sensors/fringelab 0.1.0'],'bundled_package_code':False,'runtime_download_boundary':'OCR may download engine/language resources; HEIC decoder is optional.'},indent=2))
        archive.writestr('BUNDLE.json',json.dumps({'schema_version':'1.0.0','sensor_id':sensor_id,'sensor_version':'0.1.0','git_sha':sha,'evidence_level':'E2','status':'dry-run-not-published','contract_version':'1.0.0','entrypoint':f'@physics-software-sensors/fringelab/sensors.{"StripProfileSensor" if sensor_id.startswith("image.") else "RulerTicksSensor"}'},indent=2))
    return target

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,default=ROOT/'build/fringelab');args=parser.parse_args();output=args.output.resolve();output.mkdir(parents=True,exist_ok=True)
    artifacts=[]
    for relative in ['packages/typescript','packages/fringelab']:
        run('npm','run','build',cwd=ROOT/relative)
        packed=json.loads(run('npm','pack','--json','--pack-destination',str(output),cwd=ROOT/relative));artifacts.append(output/packed[0]['filename'])
    # Node imports cover algorithms, Sensors, browser helpers and SSR-safe closed calculator.
    with tempfile.TemporaryDirectory(prefix='fringelab-consumer-') as tmp:
        consumer=Path(tmp);(consumer/'package.json').write_text('{"type":"module","private":true}')
        run('npm','install','--omit=optional','--cache',str(output/'npm-cache'),*map(str,artifacts),'react@19.2.6','react-dom@19.2.6','typescript@5.9.3','@types/react@19','@types/react-dom@19',cwd=consumer)
        (consumer/'smoke.mjs').write_text('''import assert from 'node:assert/strict';
import { calculateExpression, Signal } from '@physics-software-sensors/fringelab';
import { StripProfileSensor, RulerTicksSensor } from '@physics-software-sensors/fringelab/sensors';
import { BrowserCameraSource, RulerDetectionRunner, recognizeRulerReadings } from '@physics-software-sensors/fringelab/browser';
import { FloatingCalculator } from '@physics-software-sensors/fringelab/react';
import React from 'react'; import { renderToString } from 'react-dom/server';
assert.equal(calculateExpression('(12+8)/5'),4);assert.equal(new StripProfileSensor().describe().sensorId,'image.strip-profile');
assert.equal(new RulerTicksSensor().describe().sensorId,'vision.ruler-ticks');assert.equal(typeof Signal.extractStripProfile,'function');
assert.equal(new BrowserCameraSource().describe().sensorId,'camera.capture');assert.equal(typeof RulerDetectionRunner,'function');assert.equal(typeof recognizeRulerReadings,'function');
assert.ok(renderToString(React.createElement(FloatingCalculator)).includes('打开计算器'));
for(const suffix of ['core/signal','core/ruler','styles.css'])assert.ok(import.meta.resolve('@physics-software-sensors/fringelab/'+suffix));
console.log('PASS: clean tgz consumer, all entry points and SSR');
''')
        smoke=run('node','smoke.mjs',cwd=consumer)
        (consumer/'smoke.ts').write_text('''import type { ProcessorSensor, SourceSensor } from '@physics-software-sensors/core';
import { StripProfileSensor, RulerTicksSensor } from '@physics-software-sensors/fringelab/sensors';
import { BrowserCameraSource } from '@physics-software-sensors/fringelab/browser';
import { calculateExpression } from '@physics-software-sensors/fringelab';
const sensors: ProcessorSensor[] = [new StripProfileSensor(),new RulerTicksSensor()];
const camera: SourceSensor = new BrowserCameraSource();
const result: number = calculateExpression('2^3'); void sensors;void camera;void result;
''')
        run(str(consumer/'node_modules/.bin/tsc'),'--noEmit','--strict','--skipLibCheck','--target','ES2022','--module','NodeNext','--moduleResolution','NodeNext','smoke.ts',cwd=consumer)
    sha=run('git','rev-parse','HEAD');artifacts.extend(bundle(sid,output,sha) for sid in ['image.strip-profile','vision.ruler-ticks'])
    manifest={'status':'dry-run-not-published','git_sha':sha,'artifacts':[record(p) for p in artifacts],'clean_install':smoke,'types':'PASS','optional_heic_installed':False,'registry_published':False}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(output/'SHA256SUMS').write_text(''.join(f'{record(p)["sha256"]}  {p.name}\n' for p in artifacts))
    print(json.dumps(manifest,indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
