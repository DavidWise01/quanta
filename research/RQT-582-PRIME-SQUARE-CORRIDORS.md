# RQT-582 — Prime-Square Corridor Reduction

**Exact verified all-scale square-class result.** Recomputed all 135 discriminant families Δ(t)=At²+Bt+C from the RQT-575 reduced rank-four Gram and RQT-581 rays/offsets. Each polynomial was checked by direct Gram evaluation at positive and negative scales.

The 15 previously excluded infinite families from RQT-581 were independently rechecked. New exhaustive square-residue tests for every t modulo p², with p prime ≤250, found **40 NEW exclusions**. A separate prime-power screen had first identified 30 of these (2-adic and other powers included). An independent direct enumeration of t and all square residues validates every exclusion certificate.

| Certificate modulus p² | New all-scale exclusions |
|---|---:|
| 7²=49 | 14 |
| 17²=289 | 4 |
| 19²=361 | 2 |
| 23²=529 | 10 |
| 53²=2809 | 2 |
| 59²=3481 | 2 |
| 83²=6889 | 4 |
| 163²=26569 | 2 |
| **Total new** | **40** |

**Selected-family ledger:** 135 total = 55 excluded at every integer t (15 previously + 40 new), 80 unresolved. Certified exclusion fraction 55/135 = 40.74%; this is NOT a measurement of how close we are to proving Root 19.

Proof: if Δ(t) were an integer square, it would lie in the quadratic-residue set modulo every p². For each excluded family, exhaustive t modulo its identified p² produces no square residue. Thus **no integer scale on that ray-offset family** can yield norm−2 via the eliminated-coordinate quadratic. No global nonrepresentation theorem follows: this parametrization is not all of Z⁴, and the remaining 80 are not proved solvable.

Original 22D Gram/Wall replay **not performed**, no new integral norm−2 root, no 19th root certificate and no completed 21-reflection word. The triple-nested {{i}} and arc-arc-degree{{n}} architecture indexes the research but was not proven to generate lattice vectors in this test.

Local conversation files: executable exact `rqt582.py`, full `results.json` (135 families with 40 new modular certificates/source hashes), research Markdown, original zen laboratory JPEG and standalone HTML with embedded JPEG. This GitHub research edition is text only. GitHub Pages and JPEG repository upload remain unverified.

**RQT-583 next bound:** examine the 80 surviving families using exact Pell/conic arithmetic and primitive valuations; if an integral vector is found, back-map and verify against original 22D Wall ordering.