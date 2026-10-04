import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
test('fixed-source golden remains exact after extraction and includes auto/manual ruler paths', () => {
  const golden = JSON.parse(readFileSync(new URL('../../tests/fixtures/source-golden.json', import.meta.url), 'utf8'));
  const actual = JSON.parse(execFileSync('node', [fileURLToPath(new URL('../../../../tools/fringelab-golden-harness.mjs', import.meta.url)), fileURLToPath(new URL('../src/core/', import.meta.url))], { encoding: 'utf8' }));
  assert.equal(golden.source_commit, '37a8b3996791790a22980b0d562996a65a3a65ef');
  assert.deepEqual(actual, golden.results);
});
