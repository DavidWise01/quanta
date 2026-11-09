# QG-034 — Witness Lineage

**Carrier:** `||||` · **Upstream:** QG-033 verified three-witness root ledger.

Three different domains are not three independent origins. A witness may quote a report, which quotes an archive, which quotes the same original statement as another witness. We preserve all reports while reducing the **effective count of independent lineages**.

## Rule

`|||| → three witnesses → trace their roots → discover shared ancestry → compare → preserve ||||`

Each QG-033 witness becomes a node with the same ID and exact source URL. A directed `parents` edge points backward to a cited ancestral record or terminal origin. Each terminal origin has no parents. All intermediate records require at least one parent. Provenance is declared metadata, not independently authenticated.

Trace every witness to its reachable terminal origins. If any two witnesses share an origin, they are dependent. Build connected components across witnesses where a shared origin creates an edge; use these components as **conservative lineage counts**, including transitive overlap. The raw number of unique origin IDs is reported separately and is not interchangeable with the component count.

An origin attribution does not prove actual independent reporting. Unspecified ancestry is not a valid terminal origin by default: mark an explicitly investigated, documented origin, or withhold a three-independent finding. Invalid, cyclic, mismatched and incomplete graphs are rejected. An origin identifier is a caller-assigned reference; identical historical origins given different IDs will evade detection without human review.

## Invariants

1. Valid, replay-verified QG-033 source; exact matching witness IDs and source URLs.
2. Exactly three witness nodes; at most 96 total nodes, deterministic sorted canonical form.
3. Acyclic ancestry directed backward, no dangling references, no fabricated implicit ancestors.
4. Distinct original source hosts do not guarantee distinct historical origins.
5. An origin is counted once no matter how many witness paths reach it.
6. Shared-origin connected components define conservative effective lineage count (1–3).
7. Full QG-033 source and all original witness statements retained; lineage is a separate append-only trace and optional review event.
8. `interpretationProven:false` always; no promotion of historical truth.
9. Plain JSON event replay detects inconsistent edits but does **not** provide cryptographic tamper resistance.

## Cases

- A→archive, B→archive, C→archive: three witnesses, **one** lineage.
- A→archive, B→archive, C→other: three witnesses, **two** lineages.
- A→archive1, B→archive2, C→archive3: three declared independent lineages, pending source authentication and human assessment.
- A→archive1, B→archive1 and archive2, C→archive2: transitive shared ancestry means **one** lineage (even with two unique origins).

## Artifacts

- [Kernel](./witness-lineage.mjs)
- [Eight regression tests](../tests/witness-lineage.test.mjs)
- [Interactive ancestry viewer](../witness-lineage.html)
