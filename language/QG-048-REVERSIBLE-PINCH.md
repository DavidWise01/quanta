# QG-048 — Reversible Pinch

```text
ORIGINAL n+1 V, 2n E
           |
           | CONTRACT C -- R0
           v
SUCCESSOR n V, 2n-3 E
           |
           +---- SUCCESSOR ONLY -> ORIGINAL UNDETERMINED
           |
           +---- PRESERVE PREIMAGE + EDGE LINEAGE
                         |
                    UNFOLD EXACTLY
                         |
                 ORIGINAL IDs + EDGES
```

## Core invariant

`unfoldPinch(freezePinch(n)) = sourceGraph(n)` byte-for-byte as structured data under deterministic JSON comparison.

The original wheel graph is contracted using the **QG-047** operation, including removal of one loop and deduplication of two parallel edges. The QG-048 packet stores a full original graph plus source-to-successor vertex and edge lineage and a deterministic contraction certificate. Reversal checks these witnesses against the independently regenerated expected contraction. Without the preimage, a successor graph **does not uniquely determine** original labels, split edge ownership, or provenance. A stripped successor is deliberately rejected as insufficient.

The model admits single rim-center contact at `s=1` and tests `n=3,4,5,8,13`; multi-contact samples are rejected by the underlying QG-047 surgery. The original and successor both have Euler characteristic 2, but differ in cell counts. No new physical topology or phase change is asserted.

## Trust boundary

These packets are self-consistent data. A coordinated forgery that replaces the source and all evidence may pass unless authenticated against an external immutable witness or signature. This local value-based append ledger is **not** itself a cryptographic commitment or independent archival store.

Run: `node --test tests/post-contact-reconstruction.test.mjs tests/reversible-pinch.test.mjs`.
