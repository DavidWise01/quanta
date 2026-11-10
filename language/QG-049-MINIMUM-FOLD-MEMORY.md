# QG-049 — Minimum Memory of a Fold

## What is preserved?

```text
FULL QG-048:
    original + full contracted proof + duplicate preimage
            |
      QG-049 COMPRESSION
            |
    contracted successor
    recipe ID (fixed, versioned)
    generating parameter: lobes
            |
    n inferred from successor vertex count
            |
      regenerate original exactly
```

Within the restricted QG-047 generator family, `sourceGraph(n,lobes)` and `contractFirstContact(n,lobes)` are deterministic. The successor has `n` vertices. Given the successor, recipe identifier `QG-047-single-contact-v1`, and the `lobes` parameter, QG-049 independently regenerates the expected original graph and contraction. It accepts **only if** the regenerated successor matches the provided successor exactly. Original vertex names, coordinates and edges thereby recover exactly without duplicating the source graph in the packet.

This is **recipe-relative reconstruction**, not a proof of the minimum possible number of bits across all graphs. The code's stored witness is not necessarily information-theoretically minimal even within the recipe. Some `lobes` choices have sampling aliases in geometry, and coordinate roundoff matters. The claimed compression measure compares JSON string lengths in UTF-16 code units for the produced structures, not encoded network payload size or physical memory.

Removing the witness is deliberately rejected: an arbitrary contracted graph alone does not determine which vertices and edges used to exist before contraction. A deletion of a source-only edge or hidden name may produce the same successor. The fixed generator prior is extra information that makes source identification possible. Therefore this does not contradict QG-048's insufficiency statement.

```text
Invariant: restore(compress(G, recipe)) === G
Acceptance: contracted_successor === regenerate(recipe, witness).successor
```

Tests include five shape sizes, round-trip fidelity, source tampering, recipe mismatch, missing witness, ledger replay, and unsupported simultaneous contacts. No encryption, signatures, physical capacitance, Mandelbrot identification or mathematical universal minimum is asserted.

Run: `node --test tests/minimum-fold-memory.test.mjs`
