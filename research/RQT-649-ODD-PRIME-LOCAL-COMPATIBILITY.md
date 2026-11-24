# RQT-649 — Odd-Prime Local Compatibility and Singular Exceptions

## Executive result

Reopened the exact RQT-619 integer-coefficient quadratic archive, `G(u,t)=r₀u²+r₁ut+r₂t²+r₃u+r₄t+r₅=0`, for all **27 canonical sign-orbits** representing 53 unresolved selected family IDs. Exhaustively enumerated solutions in `F_p²` for **13 distinct odd primes p=3,5,7,11,13,17,19,23,29,31,37,41,43**, giving **351 prime–orbit checks**.

Every orbit has at least one mod-p root for every tested prime. **349 of 351 checks have a nonsingular root**, meaning at least one partial derivative `G_u=2r₀u+r₁t+r₃` or `G_t=r₁u+2r₂t+r₄` is nonzero mod p. Holding the other variable fixed, the ordinary one-variable Hensel theorem proves existence of a solution in `Z_p` at every precision. An exact integer recurrence independently constructs each of the 349 witnesses through `p^6`.

## Exceptional singular-only cases

| Canonical orbit | Prime p | Number of mod-p roots | Nonsingular roots | Compatible lifts modulo p² |
|---|---:|---:|---:|---:|
| 2 | 7 | 1 | 0 | 49 |
| 28 | 31 | 1 | 0 | 961 |

These two cases have many exact `p²` lifts, but the nonsingular Hensel argument does **not** apply. The reported `p²` lifting does not certify indefinite lifting or a `Z_p` root. A separate singular-lifting or valuation proof is required.

## Per-prime audit totals

| p | Orbits with roots | Orbits with nonsingular roots | Total mod-p roots | Total nonsingular roots |
|---:|---:|---:|---:|---:|
| 3 | 27 | 27 | 116 | 110 |
| 5 | 27 | 27 | 141 | 140 |
| 7 | 27 | 26 | 186 | 183 |
| 11 | 27 | 27 | 292 | 290 |
| 13 | 27 | 27 | 333 | 333 |
| 17 | 27 | 27 | 472 | 472 |
| 19 | 27 | 27 | 546 | 544 |
| 23 | 27 | 27 | 642 | 642 |
| 29 | 27 | 27 | 818 | 817 |
| 31 | 27 | 26 | 811 | 810 |
| 37 | 27 | 27 | 1,012 | 1,012 |
| 41 | 27 | 27 | 1,104 | 1,104 |
| 43 | 27 | 27 | 1,150 | 1,150 |

## Reproducibility and evidence boundary

- Standalone Python 3 code: `research/rqt649-odd-prime-audit.py`.
- Local detailed certificate: `RQT-649-results.json`, SHA-256 `55396b479cf4b4396cf09e44de2a8be4be892e34fd5e0cab9a952dc6ef8399dc`.
- Input RQT-619 fingerprint: `97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021`.
- All calculations exact in finite fields and integers; no randomness or floating-point tolerance.
- These are local results only for the 13 stated primes, not for every prime. Nonsingular lifting proves local solvability for those 349 prime-orbit cases but **does not** produce a shared ordinary integer solution satisfying all primes at once.
- The selected family ledger remains **82/135 all-scale excluded (60.74%), 53 unresolved across 27 canonical orbits**. No new whole-family exclusion, ordinary norm−2 seed, or original 22D Wall replay. **Root 19 OPEN**.

## Next natural bound — RQT-650

Analyze the two exceptional singular prime cases by exact valuation-based lifting through higher powers and distinguish local p-adic existence from ordinary integer solvability. Avoid claiming that many roots at p² automatically imply an infinite root.

`{brace{n}[box[n](torroid(n))]} · {{i}} · .dlw`
