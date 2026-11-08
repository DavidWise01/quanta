# QG-022 — Memory Projection

Carrier: `||||`. Boundary: one visible Chrome Dot selects one revision in a complete QG-021 corpus memory ledger.

## Primitive
Projection is an *addressed view*, not an information compressor. The dot is a visual representative. A revision ID binds the view to an existing immutable memory snapshot. Its full structured source is recovered from the separately supplied ledger, never inferred from the dot alone.

Workflow: `|||| corpus@r0002 → •(r0002) → unfold(ledger,r0002) → corpus@r0002 → history(r0002→r0001→r0000) ||||`.

## Invariants
1. Exactly one selected revision per projection record.
2. The visible terminal is one dot; the ledger, not the dot, retains the full source.
3. `4→3→2→1` remains the geometric presentation ladder; all four states remain addressable.
4. Projection metadata is recomputed against the selected immutable snapshot, rejecting mismatched revision IDs or corrupted phase records.
5. Unfolding recovers the *exact structured corpus* for the selected historical version.
6. Backward history walks stop at `r0000` with verified parent pointers.
7. A paragraph can be traced through explicit historical address mappings.

## Limits
QG-021's revision IDs are ledger-local numeric sequence labels, not global content hashes. Structural verification does not detect a completely substituted self-consistent ledger. A browser can import or export the JSON ledger, but this implementation does not autonomously persist memory.

## Artifacts
- [Executable projection kernel](./memory-projection.mjs)
- [Seven regression tests](../tests/memory-projection.test.mjs)
- [Interactive projection lab](../projection.html)