# QG-021 — Corpus Memory and Source Lineage

Carrier: ||||. QG-021 is an append-only computational representation of complete QG-020 corpus revisions.

## Natural invariant
Each revision holds a complete immutable QG-020 source snapshot. Each later revision points to its immediate predecessor by ID r0000, r0001, etc. Earlier records remain addressable. Revision IDs are local sequence labels rather than global unique hashes.

## Source lineage
Per-transition paragraph correspondences include previous and next addresses, a change state (unchanged, edited, created, retired), and a basis (same-address, explicit, address). Same-address matches are automatic; changes to addresses must use explicit one-to-one mappings. Text equality does not by itself prove source identity.

Created and retired refer to the active source address set. Neither destroys historical snapshots. Exact source versions are recovered through recoverCorpusRevision, lookups through lookupCorpusAtRevision, and backward trace through traceCorpusLineage.

## Rules
Instantiate with instantiateCorpusMemory. Append with appendCorpusRevision(memory, newSource, {comment, lineage}). Verify through verifyCorpusMemory. Export the full JSON ledger if durable memory is needed: the browser does not automatically save anything.

Each paragraph retains QG-020's four geometry levels (4 full source strokes, 3 vertices, 2 endpoints, 1 Chrome Dot view). The visible dot cannot reconstruct the underlying corpus without the stored source witness.

## Validation gates
1. Every version reconstructs exactly.
2. An append never modifies earlier revision snapshots.
3. Every parent ID, source snapshot and correspondence is checked.
4. Explicit moved-address mapping remains traceable.
5. Changed parent pointers, lineage arrays and nested corpus records fail validation.
6. Serialized JSON history can be recovered.
7. Empty corpus can grow without losing the initial revision.

Structural validation is not cryptographic authenticity: a completely rewritten self-consistent ledger can still pass. This is not a persistent autonomous agent or a physics model.

## Artifacts
- [Corpus memory kernel](./corpus-memory.mjs)
- [Regression tests](../tests/corpus-memory.test.mjs)
- [Memory viewer](../memory.html)