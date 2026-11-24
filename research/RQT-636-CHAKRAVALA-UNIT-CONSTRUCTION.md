# RQT-636 — Exact Chakravala Unit Construction Attempt

## Executive summary
RQT-636 shifts away from continued-fraction convergent enumeration to the **Chakravala integer recurrence** for the three known square-factor reduced Pell coefficients. It tests 10,000 deterministic arithmetic steps per group, **30,000 total**, while maintaining the exact invariant
```text
a_n² − d b_n² = k_n
```
at every iteration.

| Reduced group | Removed factor s | Sharp recovery power E | Steps | Last k | Final a bits |
|---|---:|---:|---:|---:|---:|
| 1 | 5 | 3 | 10,000 | 28593118985286961 | 24,637 |
| 2 | 7 | 3 | 10,000 | −19593923905788665 | 24,942 |
| 3 | 4 | 2 | 10,000 | 34613556081881122 | 24,762 |

No state reaches `k=+1` or `k=−1` in these finite paths; **no numerical norm-one unit is constructed**. This is *not an all-scale obstruction* and does not establish that no unit exists.

## Exact transition
Given integer (a,b,k) satisfying `a²−db²=k`, select nonnegative integer `m` satisfying `a+b m ≡ 0 (mod |k|)`; among the candidates nearest √d on the resulting arithmetic progression, select the one minimizing `|m²−d|`. Then set
```
a'=(a m+d b)/|k|
b'=(a+b m)/|k|
k'=(m²−d)/k
```
Check every division and `a'²−d b'²=k'` using exact integers. The script asserts these conditions at every stage. It records checkpoints at steps 1,2,3,10,100,1000,5000 and 10000, including norm k, bit lengths and SHA256 of positive integer coordinates represented unsigned big-endian. No floating-point computations.

If `k=+1`, the (a,b) pair is a verified reduced norm-one unit. If `k=−1`, its square has norm +1. Only then should the sharp recovery power E=(3,3,2) be used, followed by direct original norm verification for `D=s²d`.

## Evidence and limits
- Reproducer: `research/rqt636-chakravala.py`.
- Complete local certificate: `RQT-636-results.json`, SHA256 `f9f74012bfc2b5ed2f96669cb8eef5289b27ea689382baa830518534863efba0`.
- Three reduced groups represent 16 of 27 canonical unresolved sign-orbits, not the entire 27.
- No new whole-family exclusions, generalized Pell target seed, exact integer norm−2 root, or original 22D Wall replay.

Selected-family ledger remains **82/135 excluded all-scale (60.74%), 53 unresolved** across 27 canonical sign-orbits. **Root 19 OPEN.**

## RQT-637
Investigate constructive algebraic shortcuts, compact invariant-cycle proofs or a factor-assisted unit computation. Require direct integer norm equality before declaring a constructed unit. Do not equate a finite Chakravala nonfinding with a proof of nonexistence.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
