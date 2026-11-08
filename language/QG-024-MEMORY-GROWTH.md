# QG-024 — Convergent Memory Growth

**Carrier:** `||||`. After QG-023's two-parent merge, the merged source can become a new ancestry node and produce its own independent descendants. All earlier nodes stay available.

## Natural boundary
QG-021 uses a linear chain; QG-023 compares a pair of chains. QG-024 holds a **directed acyclic ancestry graph** of complete source snapshots. Each node has either 0 parents (origin), 1 parent (branch), or 2 parents (convergence). Nodes are appended in topological order and assigned `n0000`, `n0001`, and so on.

## Core rules
1. Each node retains a complete, canonical QG-020 snapshot. No ancestor is overwritten.
2. Every parent must precede the new child in the graph; a node cannot parent itself or reach a future node.
3. Branch nodes preserve exactly one parent and may contain any valid QG-020 corpus source.
4. Convergence nodes have exactly two **distinct** parents and an explicit common ancestor.
5. Common ancestor selection is deterministic: the most recently created node reachable backward from both parents. This does not claim a unique graph-theoretic lowest common ancestor in every possible DAG.
6. Convergence reuses QG-023's three-way paragraph comparison and refuses text conflicts without explicit left/right/base/custom resolution.
7. QG-023.1 still requires equal corpus structure and source paragraph addresses at the ancestor and both heads. Structural merges remain out of scope.
8. The graph can be serialized to JSON and structurally replay-validated, including every parent link and recomputed merge result.

## Example
```text
         n0000 origin
         /          \
   n0001 A         n0002 B
         \          /
        n0003 convergence
         /          \
   n0004 C         n0005 D
         \          /
        n0006 convergence
```

The `4→3→2→1` geometric projection per source remains available through the nested QG-020 paragraph transport. A single dot is a projection pointer, not a self-contained history.

## Constraints
QG-024.1 limits graphs to 32 nodes and depends on the same existing ASCII paragraph grammar. IDs are local labels, **not** hashes, identity proofs, permanent network addresses or automatic persistence. The current browser lab holds state only for its session unless the ledger JSON is exported.

## Artifacts
- [Executable memory growth kernel](./memory-growth.mjs)
- [Regression tests](../tests/memory-growth.test.mjs)
- [Interactive growth lab](../growth.html)