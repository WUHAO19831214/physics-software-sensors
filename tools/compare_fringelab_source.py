#!/usr/bin/env python3
"""Compare preserved algorithms with the fixed source commit, not its working tree."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / 'packages/fringelab'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--source', type=Path, required=True)
parser.add_argument('--write-golden', action='store_true')
args = parser.parse_args()
provenance = json.loads((PACKAGE / 'source-files.json').read_text())
with tempfile.TemporaryDirectory(prefix='fringelab-fixed-source-') as directory:
    lib = Path(directory) / 'lib'
    lib.mkdir()
    for spec in provenance['files']:
        original = subprocess.check_output(['git', 'show', f"{provenance['commit']}:{spec['source_path']}"], cwd=args.source)
        if hashlib.sha256(original).hexdigest() != spec['sha256']:
            raise SystemExit(f"Source hash mismatch: {spec['source_path']}")
        destination = (PACKAGE / spec['destination']).read_text()
        def normalize_imports(text):
            return re.sub(r'(["\'])(\.\.?/[^"\']+)\1', lambda m: m[1] + m[2].removesuffix('.js').removesuffix('.ts').replace('../core/', './') + m[1], text)
        if normalize_imports(original.decode()) != normalize_imports(destination):
            raise SystemExit(f"Extracted module changed beyond import paths: {spec['destination']}")
        (lib / Path(spec['source_path']).name).write_bytes(original)
    for spec in provenance.get('fixtures', []):
        original = subprocess.check_output(['git', 'show', f"{provenance['commit']}:{spec['source_path']}"], cwd=args.source)
        if hashlib.sha256(original).hexdigest() != spec['sha256']:
            raise SystemExit(f"Source fixture hash mismatch: {spec['source_path']}")
    harness = ROOT / 'tools/fringelab-golden-harness.mjs'
    source = json.loads(subprocess.check_output(['node', '--experimental-strip-types', str(harness), str(lib), '.ts'], text=True))
    extracted = json.loads(subprocess.check_output(['node', str(harness), str(PACKAGE / 'dist/src/core')], text=True))
    if source != extracted:
        raise SystemExit('FAIL: source/package numeric or failure-state output differs')
    golden = PACKAGE / 'tests/fixtures/source-golden.json'
    if args.write_golden:
        golden.write_text(json.dumps({'source_commit': provenance['commit'], 'results': source}, ensure_ascii=False, indent=2) + '\n')
    elif json.loads(golden.read_text())['results'] != extracted:
        raise SystemExit('FAIL: checked-in fixed-source golden changed')
    print(f"PASS: {len(provenance['files'])} source hashes; calculator, ROI, manual/multi-point ruler, 4 automatic-ruler scenes, profile/features, simulation, optics and analysis match fixed source")
