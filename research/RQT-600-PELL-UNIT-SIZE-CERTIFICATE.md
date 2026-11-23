# RQT-600 — Exact Pell Unit Size Certificate

## Independently replayed
RQT-599 squarefree family-28 coefficient:
`d=3580734425344222227352852171253793`.

Replayed the exact continued fraction of √d for **2,000,000** steps, independently matching four archived checkpoints (10,000; 100,000; 1,000,000; 2,000,000). There was no period closure. Terminal (m,q,a) = `(48319755305916816,23577184610196697,4)`.

Let L be the period length. The exact recurrence shows **L > 2,000,000**. The first positive norm-one Pell solution `x²-dy²=1` comes from continued fraction convergent index L−1 when L is even, or 2L−1 when L is odd. Therefore that index is at least 2,000,000. All partial quotients beyond the first are at least one, so convergent denominators satisfy `q_n ≥ F_(n+1)`, where F is Fibonacci.

Hence **y ≥ F_2000001 ≥ 10^417975**. Fast-doubling exact arithmetic independently certifies that `F_2000001` has **1,388,484 bits** and **417,976 decimal digits**. Thus the fundamental norm-one Pell unit's y-coordinate has **at least 417,976 decimal digits**.

This is a size certificate, not a constructed or compressed fundamental unit. No suitable accelerated Pell solver (PARI/GP, Sage, cypari2, flint) was available in the execution environment.

## Limits
- Explicit integral Pell norm-one unit: **NOT CONSTRUCTED**.
- Generalized Pell seed: **NOT FOUND**.
- Original 22D Wall replay: **NOT PERFORMED**.
- Selected-family ledger: **82/135 excluded (60.74%), 53 unresolved** — no new exclusion.
- Selected corridors do not exhaust the rank-four lattice.
- Root 19: **OPEN**.

## Next bound — RQT-601
Seek a compact, independently checkable Pell infrastructure/class-group representation or prioritize generalized Pell seeds directly. A large fundamental unit does not imply absence of generalized Pell solutions.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
