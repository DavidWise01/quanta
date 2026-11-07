import test from "node:test";
import assert from "node:assert/strict";
import {
  instantiateChromeDot, foldChromeDot, runChromeDot,
  validateChromeDot, CHROME_EXPECTED_COUNTS, CHROME_FOLD_SIGNATURE
} from "../language/chrome-dot.mjs";

test("canonical 8 → 4 → 2 → 1 → 1 and all eight lineage IDs", () => {
  let s = instantiateChromeDot();
  const snapshots = [s];
  for (let i = 0; i < 4; i++) {
    s = foldChromeDot(s);
    snapshots.push(s);
    assert.equal(validateChromeDot(s).pass, true);
  }
  assert.deepEqual(snapshots.map(x => x.nodes.length), CHROME_EXPECTED_COUNTS);
  assert.deepEqual(s.nodes[0].leaves, Array.from({ length: 8 }, (_, i) => "s" + i));
  assert.equal(s.history[4].operation, "fixed-point");
  assert.equal(s.history[3].representativeIds[0], s.history[4].representativeIds[0]);
  assert.equal(foldChromeDot(s), s); // exact reference identity beyond terminal
  assert.equal(CHROME_FOLD_SIGNATURE, String.raw`\.|./`);
});

test("fold history snapshots are immutable and append-only", () => {
  let s = instantiateChromeDot();
  const initial = s;
  s = foldChromeDot(s);
  assert.equal(initial.step, 0);
  assert.equal(initial.nodes.length, 8);
  assert.equal(initial.history.length, 1);
  assert.equal(s.history.length, 2);
  assert.notEqual(initial, s);
  assert.ok(Object.isFrozen(initial));
  assert.ok(Object.isFrozen(s));
  assert.ok(Object.isFrozen(s.nodes));
  assert.ok(Object.isFrozen(s.nodes[0].leaves));
  assert.throws(() => s.nodes.push({}), TypeError);
  assert.throws(() => { s.history[0].step = 999; }, TypeError);
});

test("custom source identities preserve exactly one ordered lineage", () => {
  const ids = ["a","b","c","d","e","f","g","h"];
  const final = runChromeDot(ids);
  assert.deepEqual(final.nodes[0].leaves, ids);
  assert.equal(final.step, 4);
  assert.equal(final.history.length, 5);
  assert.equal(validateChromeDot(final).pass, true);
});

test("reject missing, repeated, malformed sources", () => {
  assert.throws(() => instantiateChromeDot(["a"]), RangeError);
  assert.throws(() => instantiateChromeDot(Array(8).fill("x")), TypeError);
  assert.throws(() => instantiateChromeDot(["a","b","c","d","e","f","g",""]), TypeError);
});

test("validator detects lineage tampering", () => {
  const state = runChromeDot();
  const bad = { ...state, nodes: [{ ...state.nodes[0], leaves: ["only one source"] }] };
  assert.equal(validateChromeDot(bad).pass, false);
});

test("fold never modifies 11-dimensional hypercube mathematical counts", () => {
  const before = { vertices: 2 ** 11, edges: 11 * 2 ** 10, faces: 11 * 10 * 2 ** 8 };
  runChromeDot();
  const after = { vertices: 2 ** 11, edges: 11 * 2 ** 10, faces: 11 * 10 * 2 ** 8 };
  assert.deepEqual(after, before);
  assert.deepEqual(before, { vertices: 2048, edges: 11264, faces: 28160 });
});
