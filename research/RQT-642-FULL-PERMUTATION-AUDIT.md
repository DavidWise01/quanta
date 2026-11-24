# RQT-642 — Full 24-Permutation Held-Out Novelty Audit

## Executive summary

Exact integer replay of the RQT-641 four-policy methodology extended the four cyclic orders to **all 24 permutations**, keeping three reduced Pell coefficients, held-out offsets 4, 5, 6, and **60 exact transitions per policy**. All states satisfy `a²−db²=k`, all selected transitions satisfy the exact integer successor identity.

**Total:** 3 coefficient groups × 3 offsets × 24 orders × 4 policies × 60 observations = **51,840** exact state observations. Summing **distinct full (a,b,k) states within each independent four-policy run** gives **38,254**. The latter is **not a globally deduplicated 51,840-observation corpus**. **Zero norm ±1 unit events** were found.

## Full-order policy results

Each policy ran **216 times**, appearing 54 times in each of the four positions.

| Policy | Marginal new states, summed over runs | Candidate-inspection proxy bit-work | New states per 1,000 proxy units | Mean final a bits |
|---|---:|---:|---:|---:|
| Nearest | 8,134 | 29,152,272 | 0.279018 | 195.333 |
| Runner-up | 9,612 | 13,137,480 | 0.731647 | 62.333 |
| Alternating | 7,710 | 21,330,960 | 0.361446 | 139.111 |
| **Adaptive** | **12,798** | **15,762,130** | **0.811946** | 85.972 |

The adaptive policy generated **3,186 more ordered marginal states than runner-up**, or approximately **33.1%** more. In this design, it also has a larger marginal novelty/work-proxy ratio (0.812 vs 0.732), while runner-up has smaller mean final a-bit length.

Every policy contributes exactly **3,240 new states when executed first**, since the first policy starts from an empty visited-state ledger for each run. This is a useful position-balance check.

## Method limits

1. The adaptive policy is **ledger-dependent**: its trajectory can change with policy ordering. Marginal new-state totals are averages over all 24 orders rather than a mathematical order-invariant value of any fixed trajectory.
2. Unique states are counted within each independently reset run and summed across runs. Repeated states from separate runs are not globally deduplicated.
3. The bit-work proxy is the sum of bit lengths of inspected operands `a, b, |k|, m`. It is **not CPU time, memory, real energy, or a proven asymptotic bit-operation cost**.
4. The candidate set checks ten admissible progression positions near floor(√d), not every admissible integer m.
5. The experiment covers **three reduced coefficients representing 16 of the 27 canonical unresolved sign-orbits**. The other 11 were not studied in this test.
6. Novelty improves exploration of finite arithmetic states; it does not imply a nontrivial Pell unit or exact norm−2 integer root.

## Reproducibility

- Exact standalone Python 3: `research/rqt642-all-permutations.py`
- Local complete JSON: `RQT-642-results.json`
- Complete output SHA-256: `207e23d0bfc0d6a3a70711de6e9a83257413e96942e6dbd91421d7650b507ae2`
- Quanta Pages viewer: `rqt642.html`
- Distinct style JPEG: `RQT-642-Art-Nouveau-Orbital-Wheel.jpg`

**Global ledger unchanged:** 82/135 selected families excluded at all scales (60.74%); 53 unresolved represented by 27 canonical orbits. The selected corridors do not cover the entire rank-four lattice. No actual numerical Pell unit, generalized target seed, integer norm−2 root, new whole-family exclusion or original 22D Wall replay. **Root 19 OPEN**.

## RQT-643 — Next natural bound

Measure **globally deduplicated** state coverage across all permutation runs, benchmark actual elapsed time and peak memory separately, and implement an order-independent marginal contribution audit. Then evaluate whether improved novelty yields arithmetic progress toward viable Pell seed conditions. Do not optimize a proxy indefinitely without a genuine mathematical target.

`{brace{n}[box[n](torroid(n))]} · {{i}} · .dlw`
