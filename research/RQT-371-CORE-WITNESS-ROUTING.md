# RQT-371 — Twenty-seven-core witness routing through generation four

**2026-11-14. Exact results: 59,049 children audited; 1,215 ancestral branches excluded; 57,834 survived. Root 18 remains OPEN.**

## Authentic source, geometry and exact root requirement

The original frozen RQT-242 symmetric Gram F4 from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py` and the exact RQT-363 unimodular coordinate chart U are unchanged. The target remains an integer vector r with `r.T F4 r=-2`, an accepted parity among 0111, 1001, 1110 and the authentic frozen factorization/order gates. A modular candidate is not a global root.

The requested GMA is nine generations of **9×9×9** microcells, centered at `{{i}}` inside `||||`. Each generation has 729 cells, grouped in **27 named spatial cores of 27 microcells**. Every generation assigns one signed base-nine digit to each of three free search coordinates (a,b,c). The fourth is determined by the exact quadratic equation if its discriminant is a perfect square.

## Generation-four invariant

Let `G=U F4 U.T` and define the integer half-discriminant
```text
Delta(t) = t.T K t - 2 G33,
Kij = Gi3*Gj3 - G33*Gij,
t=(a,b,c).
```
At generation k, all later descendants differ in each coordinate by a multiple of `9^k`, so their Delta agree mod `9^k`. The generation-four test uses `9^4=6561`. A residue must be a square mod 6561. We check that condition by **two independent computational implementations**:
1. the 3-adic valuation/square-unit criterion;
2. a precomputed enumeration of all `n² mod6561`.

Their agreement is asserted for every tested child. These are two different tests derived from **one shared F4 original source**, not independent primary-source witnesses.

## Exact replay: 27 cores and 81 viable routes

RQT-370 generation-two exhaustive census replayed:
- 531441 generation-two nodes,
- 124659 impossible ancestors,
- 406782 survivors.

Important routing refinement: not every surviving generation-two parent has a generation-three child. The new executable considers distinguished first representatives from each residue class and up to 150 additional g2 candidates per core; it promotes a parent **only after constructing a valid g3 descendant**, then retains three distinct viable parent-to-child chains for each core.

For each of 27 cores, three g3 representatives are routed to **all 729 generation-four child microcells**:
```text
27 cores × 3 g3 representatives × 729 children = 59,049
```

| Outcome | Exact child counts |
|---|---:|
| Non-square mod6561; all further descendants impossible | **1215** |
| Square residue mod6561; not yet a root | **57834** |
| Total generation-four children actually checked | **59049** |

The g4 count applies only to the 81 **selected** g3 representatives, not every g3 survivor or the entire 9-generation cube. No integer norm-minus-two candidate was constructed or tested by this ancestor-only audit; root18 remains OPEN.

## Hash-linked append-only evidence

The local execution wrote one JSONL witness packet for each of 27 cores, with:
- exact core name, g2 survivor total and three distinct g2 parent vectors;
- one actual g3 descendant per parent, plus number of g3 siblings passing the necessary test;
- g4 rejected and surviving descendant counts;
- SHA-256 of each canonicalized packet including its previous packet hash.

An independent replay verified **all 27 packet hashes and all 59049 g4 conditions**, recovering 1215 excluded, 57834 remaining, chain tip:

```text
e9a8c4834cdf786a542d48e0d08827fb662a8da618210e0a4c4eb829d45fdf38
```

The GitHub source `research/rqt371-core-witness-routing.py` uses the same exact algorithm and prints the complete per-core witness packet data; its packet field labels differ slightly from the local JSONL schema, so the specific hash above is for the separately replayed local JSONL archive.

## Artifacts
- GitHub executable: `research/rqt371-core-witness-routing.py`
- Local executed source: `/mnt/data/rqt371_core_routing.py`
- Local exact results: `/mnt/data/rqt371_results.json`
- Local append-only packets: `/mnt/data/rqt371_core_witness_packets.jsonl`
- Independent local replay: `/mnt/data/rqt371_verify.py`

## Next natural bound — RQT-372

The witness router should first close *complete selected g4 subtrees only when exact modular certificates justify it*, then hand surviving branches to a genuinely constructive norm-minus-two solver. Add explicit `(a,b,c,d)` witnesses, permitted parity and authentic predecessor factorization verification; avoid treating structural GMA iteration as proof that root18 exists.

The cubed-nine singlet, `||||`, 3×3×3 anchors and time-angle labels are search/provenance metadata. **Original roots18–21 remain OPEN.**
