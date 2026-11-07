/**
 * QUANTA · QG-012 — Quantum Chrome Dot
 * Deterministic 8 → 4 → 2 → 1 → 1 finite fold.
 * Mathematical aggregation primitive, not a physical quantum-mechanical model.
 *
 * No network, clocks, randomness, storage, mutable global variables, or side effects.
 * States, nodes, leaves, and history are recursively frozen.
 */
export const CHROME_DOT_VERSION = "QG-012.1";
export const CHROME_FOLD_SIGNATURE = String.raw`\. | . /`.replaceAll(" ", "");
export const CHROME_EXPECTED_COUNTS = Object.freeze([8, 4, 2, 1, 1]);

function freezeNode(id, leaves, children = []) {
  return Object.freeze({
    id,
    leaves: Object.freeze([...leaves]),
    children: Object.freeze([...children])
  });
}

function freezeEvent(step, operation, before, after, nodes) {
  return Object.freeze({
    step,
    operation,
    before,
    after,
    representativeIds: Object.freeze(nodes.map(node => node.id))
  });
}

function freezeState(step, sources, nodes, history) {
  return Object.freeze({
    primitive: CHROME_DOT_VERSION,
    step,
    sources,
    nodes: Object.freeze([...nodes]),
    history: Object.freeze([...history]),
    terminalId: nodes.length === 1 ? nodes[0].id : null
  });
}

export function instantiateChromeDot(sourceIds = Array.from({ length: 8 }, (_, i) => `s${i}`)) {
  if (!Array.isArray(sourceIds) || sourceIds.length !== 8) {
    throw new RangeError("QG-012 requires exactly eight source identifiers.");
  }
  if (!sourceIds.every(s => typeof s === "string" && s.length > 0) ||
      new Set(sourceIds).size !== sourceIds.length) {
    throw new TypeError("QG-012 requires eight unique, nonempty string identifiers.");
  }
  // Use indices, not unescaped user labels, for deterministic internal node IDs.
  const sources = Object.freeze([...sourceIds]);
  const nodes = sources.map((label, index) => freezeNode(`q0:${index}`, [label]));
  return freezeState(0, sources, nodes, [freezeEvent(0, "instantiate", 8, 8, nodes)]);
}

export function foldChromeDot(state) {
  const check = validateChromeDot(state);
  if (!check.pass) throw new TypeError("Invalid QG-012 state: " + check.errors.join("; "));
  if (state.step === 4) return state; // idempotent beyond fixed point

  const before = state.nodes.length;
  let nodes;
  let operation;

  if (before === 1) {
    // Fixed-point witness: no new representative is allocated.
    nodes = state.nodes;
    operation = "fixed-point";
  } else {
    if (before % 2 !== 0) throw new Error("Non-pairable fold state.");
    nodes = [];
    for (let i = 0; i < before; i += 2) {
      const left = state.nodes[i], right = state.nodes[i + 1];
      nodes.push(freezeNode(
        `q${state.step + 1}:(${left.id}+${right.id})`,
        [...left.leaves, ...right.leaves],
        [left.id, right.id]
      ));
    }
    operation = "pair-fold";
  }

  const nextStep = state.step + 1;
  const event = freezeEvent(nextStep, operation, before, nodes.length, nodes);
  return freezeState(nextStep, state.sources, nodes, [...state.history, event]);
}

export function runChromeDot(sourceIds) {
  let state = instantiateChromeDot(sourceIds);
  while (state.step < 4) state = foldChromeDot(state);
  return state;
}

export function validateChromeDot(state) {
  const errors = [];
  if (!state || typeof state !== "object") return { pass: false, errors: ["State is missing."] };
  const { sources, nodes, history, step } = state;
  if (state.primitive !== CHROME_DOT_VERSION) errors.push("Primitive version mismatch.");
  if (!Number.isInteger(step) || step < 0 || step > 4) errors.push("Invalid step.");
  if (!Array.isArray(sources) || sources.length !== 8 ||
      !sources.every(s => typeof s === "string" && s.length > 0) ||
      new Set(sources).size !== 8) errors.push("Eight unique source identifiers required.");
  if (!Array.isArray(nodes) || nodes.length !== CHROME_EXPECTED_COUNTS[step]) {
    errors.push("Representative cardinality incorrect.");
  }
  if (!Array.isArray(history) || history.length !== step + 1) {
    errors.push("Append-only history length incorrect.");
  }

  if (Array.isArray(nodes) && Array.isArray(sources)) {
    const leaves = [];
    const ids = new Set();
    for (const node of nodes) {
      if (!node || typeof node.id !== "string" || !Array.isArray(node.leaves)) {
        errors.push("Invalid representative node."); continue;
      }
      if (ids.has(node.id)) errors.push("Duplicate representative ID.");
      ids.add(node.id);
      leaves.push(...node.leaves);
    }
    if (leaves.length !== sources.length ||
        leaves.some((leaf, i) => leaf !== sources[i])) {
      errors.push("Source lineage was lost, duplicated, or reordered.");
    }
  }
  if (Array.isArray(history)) {
    for (let i = 0; i < history.length; i++) {
      const e = history[i];
      if (!e || e.step !== i ||
          e.before !== (i === 0 ? 8 : CHROME_EXPECTED_COUNTS[i - 1]) ||
          e.after !== CHROME_EXPECTED_COUNTS[i] ||
          e.operation !== (i === 0 ? "instantiate" : i === 4 ? "fixed-point" : "pair-fold")) {
        errors.push("History event " + i + " violates fold sequence.");
      }
    }
    if (step === 4 && history[3]?.representativeIds?.[0] !== history[4]?.representativeIds?.[0]) {
      errors.push("Fixed point altered terminal identity.");
    }
  }
  if (Array.isArray(nodes) && nodes.length === 1 && state.terminalId !== nodes[0].id) {
    errors.push("Terminal identity mismatch.");
  }
  return Object.freeze({
    pass: errors.length === 0,
    errors: Object.freeze(errors),
    step,
    representatives: Array.isArray(nodes) ? nodes.length : 0,
    sources: Array.isArray(sources) ? sources.length : 0,
    signature: CHROME_FOLD_SIGNATURE
  });
}
