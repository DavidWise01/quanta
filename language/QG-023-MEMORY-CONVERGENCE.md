# QG-023 — Memory Convergence

**Carrier:** `||||`. **Boundary:** two independently appended QG-021 corpus-memory histories diverge from a shared, *identical* revision prefix, and converge in one **two-parent** record while both complete histories remain available.

## Invariants
1. The ancestor is the most recent **structurally identical full revision** in the common prefix; matching local ID alone is insufficient.
2. Each branch remains immutable. Convergence retains each full branch and its own parent history; the combined record has explicit left and right parent references.
3. Three-way comparisons use the common ancestor, left head and right head.
4. Identical changes, unchanged cells, and changes on only one branch resolve automatically.
5. If left and right change one paragraph differently, the comparison returns an explicit **conflict**; no silent winner.
6. A conflict requires an explicit selection of `left`, `right`, `base`, or `custom` text. Every selected result must satisfy the existing paragraph grammar.
7. A convergence can be replayed and checked against its two source histories and explicit resolution records. Earlier sources stay recoverable through QG-021.

## QG-023.1 scope boundary
Only **paragraph text** may differ. The three compared corpus snapshots must have matching document/chapter/section IDs, titles, paragraph addresses, and explicit reference topology. A structural rewrite is deliberately rejected rather than guessed into a merge. Cross-structure lineage and text-independent semantic reconciliation are future tasks.

## Example

```text
                        ancestor r0000
                         /        \
            left r0001 ◉          ◉ right r0001
               edit A                edit B
                         \        /
                       convergence
                      /    |       \
                merged source    both ledgers
```

Two `r0001` labels are branch-local. Each convergence parent is identified as `left` or `right` with its full retained branch ledger, not a globally unique hash.

## Implementation
- [Executable kernel](./memory-convergence.mjs)
- [Adversarial and round-trip tests](../tests/memory-convergence.test.mjs)
- [Interactive convergence viewer](../convergence.html)

**Not claimed:** Cryptographic authenticity, automatic persistence, Git source control merging, network consensus or machine inference of paragraph meaning. This is an explicit geometric-language source convergence protocol.