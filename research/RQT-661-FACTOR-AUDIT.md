# RQT-661 — Certified n+1 Factor Audit and Bounded Direct-Cofactor Search

## Executive summary

Replayed the exact RQT-660 archive for the two still-unproved large primality targets, zero-based indices **23** and **28**. Each target n has an exact factorization n−1 = F_old × R inherited from RQT-659/660. This iteration independently factors a certified portion of **n+1**, using exact divisibility and direct trial-division proofs of every identified prime.

| Quantity | Index 23 | Index 28 |
|---|---|---|
| Target n (bits) | 160 | 179 |
| Certified part F+ of n+1 | 57,346,503,214 | 8,073,084 |
| Exact factors of F+ | 2×7×11×13×3709×7723 | 2²×3×672757 |
| Unresolved remainder (n+1)/F+ | 16486230120291507571698842720004456521 | 89689378601022631701591554916055761112780124141 |
| F+² > n | **No** | **No** |
| New direct factor of blocking R | **None found** | **None found** |

A deterministic bounded Pollard-rho scan was also run directly on each blocking R, using constants c=1,3,5,7,11, with at most 12,000 iterations per constant. No nontrivial factor was recovered.

## Proof boundary

- All 9 prime-power entries are backed by exact primality trial division and exact multiplication against n+1.
- The simple square-root factor threshold fails on both targets. Moreover, a decomposition of n+1 by itself is **not** a primality proof; appropriate Lucas/BLS conditions and a sufficiently large certified factorization would need to be established.
- Failure of a bounded factor search is not proof of primality or irreducibility.
- This is an exact **negative bounded experiment**, not a proof that the two targets cannot be certified by other means.
- Full JSON and deterministic Python verifier: `research/RQT-661-results.json` and `research/rqt661.py`.

No new prime target is certified. The inherited 130 recursive prime nodes remain as previously reported, not newly replayed in this iteration. The selected-family ledger remains **82/135 all-scale excluded (60.74%), 53 unresolved in 27 canonical sign-orbits**, with **Root 19 OPEN**. No ordinary integer norm−2 seed and no original 22D Wall replay.

## Next natural bound — RQT-662

**Direct modular root-candidate gate:** prioritize original integer-coordinate equations, avoiding more expensive factorization without a clear route to a global integer seed. If primality work continues, require a complete theorem-specific certificate rather than relying on a partial n+1 product alone.

`{{i}} · .dlw`