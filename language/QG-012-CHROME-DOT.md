# QG-012 — Quantum Chrome Dot: Fixed-Point Folding

**Notation:** `\\.|./` (proposed visual fold primitive)

**Fold path:** `8 → 4 → 2 → 1 → 1`

**Status:** Proposed QUANTA representation and finite-state algorithm, *not* a demonstrated physical quantum particle, quantum state, or compactification.

## Canonical fold

Take eight separately identified source positions. A fold stage pairs positions in a declared stable order and assigns each pair a representative together with a lineage reference.

- Stage 0: **8** distinct indexed positions.
- Stage 1: **4** pair-group representatives.
- Stage 2: **2** representatives.
- Stage 3: **1** representative, the **Quantum Chrome Dot**.
- Stage 4: **1** again. This final unchanged cardinality records a **fixed point**, rather than another compression.

For the **count-only** folding map:

\[
F(n)=\max(1,\lceil n/2\rceil),\quad n\in\mathbb{Z}_{\ge1}.
\]

Specifically, `F(8)=4`, `F(4)=2`, `F(2)=1`, and `F(1)=1`.

**Important:** This is a finite-state aggregation rule. It is many-to-one if only the output representatives are stored. The full source cannot be reconstructed without preserving the hierarchical pairing tree or equivalent external lineage data.

## Formal witness and lineage invariant

Let each source have an immutable identity `s0…s7`. Define each representative as a node with children `[left,right]` and a stable ID. The terminal node has eight distinct leaf-source IDs. The next fold of one returns the same node identity and does **not** allocate a new node.

Invariants:

1. **Leaf coverage:** the final representative has precisely the original eight source leaves, each once.
2. **No source loss in recorded history:** original nodes and all pairing edges remain addressable in the fold ledger.
3. **Cardinality:** the five visible states have widths `[8,4,2,1,1]`.
4. **Idempotence at one:** `F(F(1))=F(1)=1`.
5. **No dimensional assertion:** the reduction in representative count does **not** reduce the mathematical dimension of a hypercube by itself.

## Optional chrome-dot interpretation

The label **chrome** can refer to a *visualized, reflective terminal witness*; the label **quantum** is project terminology until a physical state, dynamics, measurement procedure and falsifiable prediction have been defined. No quantum-mechanical behavior is implied by this counting algorithm.

## Relationship to QG-011

QG-011's `H₁₁` has 2,048 unique vertices and 11,264 edges. QG-012 is an **aggregation overlay** that can act on groups of eight selected addresses; it does **not** change the underlying 11-cube incidence graph. A visual dot on screen is therefore a compressed group view rather than a new graph vertex.

## Test vector

```text
8  [s0] [s1] [s2] [s3] [s4] [s5] [s6] [s7]
4  [s0,s1] [s2,s3] [s4,s5] [s6,s7]
2  [s0..s3] [s4..s7]
1  [s0..s7]
1  [s0..s7]  ← same stable identity, no new merge
```

The dot has one displayed location while its lineage retains all eight source addresses.

**Proposed rule QG-012:** Fold, preserve, and stop at the stable one.
