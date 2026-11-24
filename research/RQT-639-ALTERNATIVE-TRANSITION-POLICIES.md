# RQT-639 — Alternative Admissible Chakravala Transition Policies

## Executive result

RQT-638 showed that offsets in the initial Chakravala state largely converge to shared deterministic tails. RQT-639 instead holds the start fixed and **changes the admissible transition policy**.

For each of the three known square-reduced Pell coefficients, independently execute 120 exact steps per policy: **nearest** (minimum |m²−d|), **runner-up** (second-best admissible m), and **alternating** (nearest on even-numbered steps, runner-up on odd). All candidate m values obey the exact divisibility requirements and all successors satisfy the integer invariant `a'²−d b'²=k'`.

| Group | Observations | Distinct full states | Distinct signed norms | Cross-policy equal-norm comparisons | Nontrivial units |
|---|---:|---:|---:|---:|---:|
| 1 (s=5) | 360 | 297 | 297 | 64 | 0 |
| 2 (s=7) | 360 | 298 | 298 | 63 | 0 |
| 3 (s=4) | 360 | 298 | 298 | 63 | 0 |
| **Total** | **1,080** | **893** | **893** (group-scoped) | **190** | **0** |

All 190 cross-policy equal-norm quotients are exactly integral but trivial (Y=0). Thus a change in transition selection generates greater distinct state coverage within this experiment, **not yet a nontrivial unit**.

## Transition and correctness checks

For any exact state `a²−d b²=k≠0`, choose candidate m from the congruence `a+b m≡0 (mod |k|)`. Enumerate nonnegative candidates from ten consecutive progressions around floor(sqrt(d)), sort by (|m²−d|, |m−floor(sqrt(d))|, m), and choose rank zero or rank one under the selected policy. Verify:
```
a' = (a m+d b)/|k|
b' = (a+b m)/|k|
k' = (m²−d)/k
a'²−d b'² = k'.
```
This deliberately explores non-minimal admissible m. Its finite trajectory behavior cannot be assumed to have the classical termination properties of the minimization-based Chakravala algorithm.

At step 120, the approximate size of a (bits) is:
- Group 1: nearest 340; runner-up 69; alternating 225.
- Group 2: nearest 391; runner-up 63; alternating 278.
- Group 3: nearest 371; runner-up 66; alternating 236.

Smaller coordinate size does **not** imply being closer to a fundamental Pell unit or making more progress toward a norm-one seed.

## Evidence and limits

- Executable Python 3 standard-library replay: `research/rqt639-transition-policies.py`.
- Machine-readable complete certificate `research/RQT-639-results.json`; local SHA-256 `193510fd7e3b6ee58b58019cc1683c29746c77a931135b2aedfbd77ab7e5333c`.
- Every state and all 190 cross-policy quotients checked with exact integer arithmetic; start, step budget, policies and large-state hashes retained.
- These three coefficient groups cover 16 of 27 canonical unresolved sign-orbits; not the entire selected corpus.
- A shared state or norm is not an independent witness or evidence root.

**No numerical Pell unit, generalized Pell target seed, integer norm−2 vector, new all-scale family exclusion, or original 22D Wall replay.** Selected ledger stays **82/135 excluded at all scales (60.74%), 53 unresolved** across 27 canonical orbits. Root 19 **OPEN**.

## RQT-640 natural bound

Use an explicit **novelty-aware transition planner**: choose admissible m based on distinct-state yield and audit a held-out set of policies. Constrain bit growth and reject repeated state ancestry without confusing computational diversity with independent mathematical evidence. If an actual integer unit appears, verify the reduced norm, apply sharp 3/3/2 recovery and verify the original norm directly.

`{brace{n}[box[n](torroid(n))]} · {{i}} · .dlw`
