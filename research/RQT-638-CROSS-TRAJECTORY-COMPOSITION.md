# RQT-638 — Cross-Trajectory Chakravala Composition and Path Coalescence

## Verified exact experiment
Reused the reduced exact coefficients and deterministic Chakravala recurrence of RQT-636/637. For **each of three** coefficient groups (square factors s=5,7,4), initialized three distinct integer seeds
```
a0 = floor(sqrt(d)) + offset,  b0 = 1,
offset ∈ {1,2,3},  k0 = a0²−d,
```
then executed **600 checked states for each starting trajectory**. Every state satisfies exactly `a²−db²=k`, checked with Python integers; each arithmetic transition is checked. Across 9 starts: **5,400 exact state observations**. These three reduced coefficients cover **16 of 27 canonical unresolved sign-orbits**.

## Results

| Reduced group | State observations | Distinct signed k | Cross-start equal-k comparisons | Integral quotient checks | Trivial quotients | Nontrivial units |
|---|---:|---:|---:|---:|---:|---:|
| 1 | 1800 | 602 | 1796 | 1796 | 1796 | 0 |
| 2 | 1800 | 602 | 1796 | 1796 | 1796 | 0 |
| 3 | 1800 | 602 | 1796 | 1796 | 1796 | 0 |
| **Total** | **5400** | **1806** group-scoped | **5388** | **5388** | **5388** | **0** |

The 5388 are **pairwise comparisons**, not independent source witnesses or newly constructed nontrivial units. Each exact quotient is integral and has `Y=0`; equivalently it is the trivial norm-one unit `±1`. Distinct starts rapidly share the same deterministic arithmetic tail, so varying the initial a alone fails to construct independent unit-discovery paths.

## Exact same-norm theorem

For two states of equal signed norm `k != 0`, define
```
X=(a₁ a₂ − d b₁ b₂)/k,
Y=(b₁ a₂ − a₁ b₂)/k.
```
Whenever both numerators are divisible by k, these are integers with `X²−dY²=1`. For the 5388 exact cross-start matches here, every quotient is **trivial**: `Y=0`. Thus no reduced norm-one unit requiring sharp recovery powers 3/3/2 was discovered.

## Reproducibility
- Standalone Python 3 script: `research/rqt638-cross-trajectory.py`.
- Exact JSON certificate: `research/RQT-638-results.json`.
- Complete local result SHA256: `8c77e8e94979cdf7b0d4c9659b7c93133772b8fde115f32fecb542c6e954728b`.
- Fixed offsets, fixed 600-state budget, exact signed-k pairing and integer quotient assertions.

## Evidence and limits

A shared deterministic arithmetic trajectory is not independent mathematical confirmation. These data demonstrate **finite path coalescence in the tested starts**, not that all Chakravala starting conditions coalesce or that nontrivial Pell units are impossible.

No new all-scale family exclusion, numerical nontrivial unit, generalized Pell target seed, integer norm−2 root, or original 22D Wall replay. Selected-family ledger stays **82/135 excluded all-scale (60.74%), 53 unresolved** in 27 canonical orbits. Root 19 **OPEN**.

## RQT-639 natural bound
Switch from mere seed offsets to genuinely different transitions—e.g. alternative admissible m selection policies or composition of provably distinct ideals/norm classes. Certify whether new paths produce nontrivial norm-one quotients before counting them as additional search coverage.

`{brace{n}[box[n](torroid(n))]} · {{i}} · .dlw`
