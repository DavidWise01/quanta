# RQT-641 — Order-Balanced Held-Out Novelty Verification

## Exact experiment

Reopened RQT-640's exact policy implementation and coefficient groups. Three previously untested initial offsets `δ∈{4,5,6}` were applied to three square-reduced Pell equations; four policies were executed in each of **four cyclic permutations** of policy order. Each policy executes **60 exact transitions** per run.

Total: **3 groups × 3 offsets × 4 orders × 4 policies × 60 = 8,640 exact state observations**. Every state and transition satisfies the integer norm identity `a²−d b²=k`. The sum of unique full states *within each 4-policy run* is **6,512**. This is **not** a global unique-state count across runs, where duplicates could recur. No encountered state had norm ±1 with nonzero b, and no numerical Pell unit was constructed.

## Balanced policy results

Each policy was executed 36 times (three groups × three held-out offsets × four cyclic orders), including nine runs in first position. Order-specific new full-state contributions are:

| Policy | Ordered new states | Proxy bit-work | New states/1,000 proxy units | Mean final a bits |
|---|---:|---:|---:|---:|
| Nearest | 1,292 | 4,858,712 | 0.265914 | 195.333 |
| Runner-up | 1,602 | 2,189,580 | 0.731647 | 62.333 |
| Alternating | 1,485 | 3,555,160 | 0.417703 | 139.111 |
| **Adaptive** | **2,133** | **2,529,740** | **0.843170** | 80.250 |

Every policy adds exactly 540 new states when first in the run: no special first-position advantage. The adaptive policy yields the most new states overall and the most per proxy-bit-work unit under **this fixed experiment design**. Runner-up still ends with smaller mean a-coordinates.

The **proxy bit-work** is defined as the sum over candidate inspection of the bit lengths of the current `a`, `b`, `|k|`, and candidate `m`. It is **not measured runtime, a physical energy metric, or an asymptotic bit-complexity proof**. It is used consistently for all policies.

## Methods and caveats

- Policy orders are the four *cyclic rotations* of nearest, runner-up, alternating, adaptive, **not all 24 permutations**.
- The novelty ledger resets between independent (group, offset, order) runs. Within each run, it accumulates visited full states from earlier policies.
- The adaptive rule scores candidate transitions by unseen next full state, unseen signed k, coordinate bit length, |k| and stable rank.
- The candidate set is restricted to ten admissible arithmetic progression positions around floor sqrt(d). No exhaustiveness claim beyond this window.
- More unique states does **not** establish independent evidence ancestry, a nontrivial Pell unit or an integer norm−2 vector.

## Artifacts and scope

- Reproducer: `research/rqt641-order-balanced.py`.
- Full JSON certificate and retro-observatory JPEG are available as conversation downloads.
- Certificate SHA-256: `8e93c6d3f8a71c287d116a3d9d5b7c65c2fde30261b86c03be7e7a1d0f834a72`.
- Three reduced coefficients represent 16 of 27 canonical unresolved sign-orbits. The remaining 11 are outside this comparison.

No new whole-family exclusion, numerical norm-one Pell unit, generalized Pell target seed, integer norm−2 root, or original 22D Wall replay. Selected ledger stays **82/135 excluded all-scale (60.74%), 53 unresolved** across 27 canonical sign-orbits. **Root 19 OPEN.**

## RQT-642 natural bound

Test all 24 orders or use order-invariant marginal coverage; hold out additional transition policies, compare actual timing and memory rather than only operand-bit proxy, and protect genuine integer norm checks. Stop optimizing novelty if the discovered states do not improve viable seed constraints.

`{brace{n}[box[n](torroid(n))]} · {{i}} · .dlw`
