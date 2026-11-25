import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

// Smoke test the ACTUAL compiled Rust WebAssembly binary, not a JS substitute.
const file = process.argv[2] || 'docs/riemann-rust/toroid.wasm';
const bytes = readFileSync(file);
assert.equal(bytes.subarray(0, 4).toString('hex'), '0061736d', 'must be a WASM binary');
const { instance } = await WebAssembly.instantiate(bytes, {});
const w = instance.exports;
assert.equal(w.toroid_version(), 10, 'correct Rust ABI version');
for (const id of ['toroid_radius','toroid_theta','toroid_phi','toroid_closure_mask','toroid_forward_inner']) {
  assert.equal(typeof w[id], 'function', 'missing Rust export '+id);
}
const rows = [
  ['C1_channels_only', [4,0,0,3,1,0],9,1,3,0],
  ['C2_coordinates_only', [4,0,0,1,360,360],10,3,0,0],
  ['C3_global_return', [1,0,0,3,120,120],31,1,0,0],
  ['C4_homeostasis_only', [4,0,0,1,17,23],8,3,17,23],
  ['C5_single_coordinate', [1,0,0,3,120,1],13,1,0,3],
  ['C6_unwrapped_address', [1,361,0,3,120,120],13,1,1,0],
];
for (const [name,args,mask,radius,theta,phi] of rows) {
  assert.equal(w.toroid_closure_mask(...args),mask,name+' mask');
  assert.equal(w.toroid_radius(...args),radius,name+' radius');
  assert.equal(w.toroid_theta(...args),theta,name+' theta');
  assert.equal(w.toroid_phi(...args),phi,name+' phi');
  console.log(name,'PASS','mask='+mask,'state=['+[radius,theta,phi].join(',')+']');
}
assert.deepEqual([0,1,2,3].map(n=>w.toroid_forward_inner(n)),[2,4,6,2]);
console.log('RUST/WASM REAL-BINARY SMOKE: 6/6 cases; 24 state assertions; ABI and channel rotation PASS');
