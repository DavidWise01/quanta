# RQT-640 — Novelty-Aware Transition Planning

## Executive result

Four exact transition policies were compared across three square-reduced Pell coefficients, each for 120 states: nearest, runner-up, alternating, and adaptive novelty-aware. The deterministic adaptive policy ranks each admissible m by (1) whether the successor full state has been seen in the *earlier policy ledger*, (2) whether its signed norm has been seen, (3) coordinate bit length, (4) absolute norm, and (5) candidate rank. Exact integer norm invariants were checked for each transition.

**Total: 1,440 state observations and 1,250 distinct full (a,b,k) states. No nontrivial norm-one unit was found.**

| Group | Distinct full states | Equal-k cross-policy comparisons | Nontrivial quotients |
|---|---:|---:|---:|
| 1 (s=5) | 416 | 67 | 0 |
| 2 (s=7) | 417 | 66 | 0 |
| 3 (s=4) | 417 | 66 | 0 |
| **Total** | **1,250** | **199** | **0** |

All 199 same-norm quotients were integral and trivial (Y=0). The group state counts measure computation, not independent source witnesses.

## Ordered policy contribution

| Policy (executed in this order) | New states across 3 groups |
|---|---:|
| Nearest | 360 |
| Runner-up | 357 |
| Alternating | 176 |
| Adaptive novelty-aware | 357 |

**No novelty advantage over runner-up was demonstrated** by this fixed-order comparison. The adaptive policy chose the rank-1 candidate on 119/120 transitions for each group and rank 2 once: it strongly resembled the runner-up path. Its final a-coordinate bit lengths were **65, 64, 68** for the three groups, versus **340, 391, 371** for nearest and **69, 63, 66** for runner-up. These are size observations, not convergence theorems.

The policy's novelty score was computed against previously visited states from earlier policies, so ordered contributions are **not invariant to swapping policy order**. A future held-out, order-balanced comparison is essential.

## Reproducibility

- Exact Python 3 standard-library source: `research/rqt640-novelty-planner.py`.
- Full local JSON certificate: `RQT-640-results.json`.
- Candidate m enumeration is exhaustive **only within a ten-position arithmetic progression window around floor sqrt(d)**.
- Every candidate is checked for divisibility and every successor for `a'^2 - d b'^2 = k'`.
- All cross-policy same-norm quotients are checked for integer coordinates and norm +1.

## Scope

Three reduced coefficients cover **16 of the 27** canonical unresolved sign-orbits. The other 11 are not tested in this experiment. No new whole-family exclusion, numerical nontrivial Pell unit, generalized target seed, integer norm−2 root, or original 22D Wall replay.

Selected-family ledger remains **82/135 excluded all-scale (60.74%), 53 unresolved** across 27 canonical sign orbits. **Root 19 OPEN.**

## Next natural bound — RQT-641

Run an **order-balanced held-out novelty test** across permuted policy orders and new seed classes; quantify genuinely new mathematical states per 1,000 integer-bit operations, rather than optimizing one fixed ordering. An actual norm-one unit is admissible only after exact reduced and original norm verification using recovery powers 3/3/2.

`{brace{n}[box[n](torroid(n))]} · {{i}} · .dlw`
