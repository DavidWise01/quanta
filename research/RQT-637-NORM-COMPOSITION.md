# RQT-637 — Exact Norm-Composition Shortcut Audit

## Executive summary
RQT-637 independently reconstructed the 10,000-step Chakravala trajectory for each of the **three known square-reduced Pell coefficients** from RQT-636 (30,000 exact states). Every state was checked against its original integer norm equation `a²−d b²=k`. We tested two algebraically different, exact routes to a norm+1 unit **without needing a state of norm 1**.

### Conditional theorem A — square and divide
For any integer triple `a²−d b²=k≠0`, the square in `Z[√d]` has norm `k²`. Therefore if `|k|` divides **both** `a²+d b²` and `2ab`, then
```
X=(a²+d b²)/|k|, Y=2ab/|k|
X²−dY²=1.
```
These divisibility conditions were checked exactly for every replayed triple. No state qualified.

### Conditional theorem B — equal signed-norm quotient
If two triples satisfy `a₁²−d b₁²=k` and `a₂²−d b₂²=k`, then
```
X=(a₁a₂−d b₁b₂)/k,
Y=(b₁a₂−a₁b₂)/k
```
has norm +1 **when X and Y are integers**. This is the quotient of their algebraic integers. Every group had 10,000 distinct signed k values, so no nontrivial equal-norm state pair was available within these paths. This does not exclude other trajectories or a longer search.

### Exact replay metrics

| Group | Removed s | Checked states | Distinct signed k | Square shortcut | Minimum |k| encountered |
|---|---:|---:|---:|---:|---:|
| 1 | 5 | 10,000 | 10,000 | 0 | 1,198,289,044,897 |
| 2 | 7 | 10,000 | 10,000 | 0 | 3,086,797,639,875 |
| 3 | 4 | 10,000 | 10,000 | 0 | 26,709,460,509,542 |

The final signed k and final a bit counts independently reproduce RQT-636: `28593118985286961` (24,637 bits), `−19593923905788665` (24,942 bits), `34613556081881122` (24,762 bits).

### Reproducibility and scope

- Python 3 standard-library replay: `research/rqt637-norm-composition.py`.
- Exact JSON certificate: `research/RQT-637-results.json`.
- Locally generated JSON SHA-256: `387979b84d3935fb689e98c1f6e906367e20cb6318b42b0fdb69408dd80b12eb`.
- Three reduced coefficients represent 16 of 27 canonical unresolved sign-orbits; the other 11 have **not** been checked here.
- **No numerical unit, generalized Pell target seed, norm−2 root, or new whole-family exclusion.** Original 22D Wall not replayed.
- Overall selected ledger remains **82/135 excluded at all scales (60.74%), 53 unresolved**, mapped to 27 canonical orbits; selected corridors do not exhaust the full lattice. Root 19 **OPEN**.

## Next natural bound — RQT-638

Try *cross-trajectory* norm composition: generate independently seeded Chakravala paths and locate small signed norms with compatible quotient integrality. Check both coordinates exactly, preserve source ancestry, and only report a Pell unit after `X²−dY²=1` succeeds. If a numerical unit emerges, apply recovery exponents 3/3/2 and verify original norm.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
