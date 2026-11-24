# RQT-643 — Global State Deduplication, Order-Invariant Attribution and Instrumented Performance

## Executive result

The complete RQT-642 four-policy, all-24-permutation experiment was replayed with an **exact globally shared state set** across all three coefficient groups, held-out offsets 4/5/6 and policy orders. A state is identified by `(canonical coefficient group, a, b, k)`, preventing accidental merging of states from different Pell equations.

- Exact state observations: **51,840**.
- Prior RQT-642 distinct count summed within individual runs: **38,254**.
- Actual distinct full states across **all** runs: **1,376**.
- Repeated observations: **50,464** (97.3457% of observations).
- Norm ±1 events with nonzero b: **0**.
- No numerical nontrivial Pell unit constructed.

This corrects an interpretation risk in the previous novelty work: summing within-run uniqueness dramatically overstates total independent arithmetic coverage across repetitions.

## Policy-level exact unions and order-invariant marginal attribution

| Policy | Distinct states in its union | Ordered marginal new states within runs (RQT-642) | Global new states in instrumented execution order | Shapley attribution of combined union |
|---|---:|---:|---:|---:|
| Nearest | 186 | 8,134 | 186 | 111.75 |
| Runner-up | 540 | 9,612 | 531 | 266.75 |
| Alternating | 192 | 7,710 | 87 | 104.25 |
| Adaptive | **1,248** | **12,798** | 572 | **893.25** |
| **Union** | **1,376** | — | **1,376** | **1,376** |

The Shapley contribution is the average of marginal set additions across all 24 orders of **the four aggregate policy state sets**. It does not imply that an adaptive trajectory is order-independent: the collected adaptive set itself depends on which policies ran earlier in each individual run. Global-new-in-execution-order is **order sensitive** and is not presented as intrinsic ranking.

## Real measurements vs proxies

The complete Python 3.13.5 replay ran in one instrumented Linux environment:
- Full wall-clock elapsed time: **10.462342640 seconds**.
- Sum of individually timed policy blocks: nearest **3.244371913 s**, runner-up **1.973740412 s**, alternating **2.845024094 s**, adaptive **2.373786171 s**.
- `tracemalloc` peak tracked Python allocations: **1,043,308 bytes** (~1.04 MB decimal). This is **not process peak RSS**.

**Important:** These are **single-run instrumented timings**, not multi-trial statistical performance estimates and not portable comparisons. `tracemalloc` introduces observer overhead. The per-policy times exclude some outer-loop and bookkeeping overhead and therefore need not sum to the full replay time.

## Scope and provenance

- Reproducer: `research/rqt643-global-dedup.py`.
- Local result: `RQT-643-results.json` SHA-256 `d5e084cf2948758214f7a0794929098ab86c0c41c48040b084b4bfa2f1208d11`.
- Three square-reduced coefficients correspond to **16 of 27 canonical unresolved orbits**, not the complete selected corpus.
- The states across policy orders are repeated computations from one owned arithmetic source and are **not independent evidence witnesses**.
- No generalized Pell target seed, integer norm−2 root, new full-family exclusion, or original 22D Wall replay.

Selected-family ledger unchanged: **82/135 excluded at all scales (60.74%); 53 unresolved**, represented by 27 canonical sign-orbits. **Root 19 OPEN.**

## RQT-644 next natural bound

Move away from optimizing repeated novelty toward **global arithmetic progress**: use only genuinely new states to test exact Pell norm constraints, audit remaining 11 canonical orbits, and make the unit-target compatibility gate decisive. Benchmark timing with repeated runs only if it changes algorithm selection.

`{brace{n}[box[n](torroid(n))]} · {{i}} · .dlw`
