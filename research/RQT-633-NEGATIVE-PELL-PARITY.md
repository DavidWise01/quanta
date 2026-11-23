# RQT-633 — Reduced Pell Period Parity and All-Scale Norm−1 Obstructions

## Source and exact verification

Reopened the archived RQT-632 numerical results and checked SHA-256 `0c5cc30a499222457339908b0ff6556f898bd83ce0a7b0e17df2549b70286ed2`. The three reduced nonsquare coefficients `d` are:

| Group | s | Reduced d | Modular obstruction |
|---|---:|---:|---|
| 1 | 5 | 3580734425344222227352852171253793 | d ≡ 0 (mod 3) |
| 2 | 7 | 3052276138155931189813514017685481 | d ≡ 0 (mod 3) |
| 3 | 4 | 9883422432841335200465913703575047 | d ≡ 3 (mod 4) |

Every norm−1 equation `x²−dY²=−1` is therefore **impossible for all integers**:
- If 3 divides d, the equation would require `x²≡−1≡2 (mod 3)`, impossible.
- If d≡3 (mod 4), it would require `x²≡−1≡3 (mod 4)`, impossible.

This is an exact **all-scale theorem about negative Pell units for all three reduced coefficients**, not a bounded computational inference and not a whole-family exclusion.

## Even period parity theorem

For a positive nonsquare integer d, the simple continued-fraction expansion of √d has **odd period length if and only if** `x²−dY²=−1` has an integer solution. Since all three negative-unit equations are impossible, all three periods are **provably even**.

Additionally, exact standard continued-fraction period-state recurrences tested 100,000 states per d, 300,000 total, with no period-ending state. Therefore each period has **length strictly greater than 100,000** as a finite bound; the period is not computed. The period parity proof does not depend on this finite search.

## Certificates and honesty

Local machine-readable certificate: `RQT-633-results.json` SHA256 `3db06c964de016db7417e32df3deeeb6cfe7c1cdd58ac706809d4ca8fcfb353f`. Reproducer: `research/rqt633-period-parity.py` (Python standard library). Original numerical RQT-632 convergent bounds are preserved, not reinterpreted as a fundamental-unit certificate.

**No actual nontrivial norm+1 unit**, generalized Pell target seed, integer norm−2 root, or 22-dimensional Wall replay has been established. The 135 selected corridors do not exhaust the rank-four lattice. Selected-family ledger remains **82/135 all-scale excluded (60.74%), 53 unresolved**, representing 27 canonical orbits. Root 19 **OPEN**.

## RQT-634 next bound

Use the parity constraints to search for norm+1 units via certified even-period midpoint structure or algebraic infrastructure. Prefer a constructed norm+1 unit and exact original norm check over further unbounded brute-force searches. Maintain `Y≡0 (mod s)` when lifting reduced units to original coefficients.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
