# RQT-669 — Finite Modular Action and Pell Subgroup Closure

## Executive finding

The exact affine integer-lattice stabilizer derived in RQT-668 is a **subgroup** of the norm-one Pell unit group. Each admitted unit defines an affine transformation
[
\binom{t'}{k'}=A\binom{t}{k}+b, \quad y=r_1t+r_3+Dk,\ D=|2r_0|,
]
with
[
A=\begin{pmatrix}U+Vr_1&VD\\ V(a-r_1^2)/D&U-Vr_1\end{pmatrix},\quad
b=\binom{Vr_3+(U-1)h/a}{((U-Vr_1-1)r_3+Vh-r_1(U-1)h/a)/D}.
]

The exact RQT-668 gate is:
1. `U²−aV²=1`;
2. `a | (U−1)h`;
3. `D | V(a−r1²)`;
4. `D | (U−Vr1−1)r3+Vh−r1((U−1)h/a)`.

These conditions are **necessary and sufficient for preserving the entire affine integer-coordinate chart**. They make every entry of A and b integral; the determinant of A is `U²−aV²=1`. Products of such integer affine automorphisms and their inverses remain integer affine automorphisms, and Pell-unit multiplication composes the maps. This proves identity, closure, inverse, and finite reductions modulo every positive modulus.

**Important qualification:** This is the exact subgroup preserving the entire affine chart, not a minimal subgroup for only those points on a specific quadratic norm level. It does not establish existence of a nontrivial unit or seed in any of the original 27 unresolved charts.

## Numerical synthetic demonstration

For the separate synthetic equation `u²−2t²=1`, the original Pell unit is `(U,V)=(3,1)` for `a=8`, with affine matrix
```
A = [[3,2],
     [4,3]],  b = [0,0], det(A)=1.
```
Its inverse comes from `(3,−1)`, and both left/right compositions are the exact identity. Each of the first 16 unit powers agrees with direct affine-matrix multiplication and maps `(t,u)=(0,1)` to an integer solution of the synthetic equation.

Exhaustively enumerate every `(t,u)` modulo each m and decompose the resulting finite permutation into cycles:

| m | Points | Order of permutation | Cycle length: count |
|---:|---:|---:|---|
| 2 | 4 | 1 | 1:4 |
| 4 | 16 | 2 | 1:4, 2:6 |
| 8 | 64 | 4 | 1:4, 2:14, 4:8 |
| 16 | 256 | 8 | 1:4, 2:14, 4:24, 8:16 |
| 32 | 1,024 | 16 | 1:4, 2:14, 4:24, 8:48, 16:32 |
| 64 | 4,096 | 32 | 1:4, 2:14, 4:24, 8:48, 16:96, 32:64 |

The period doubling here is a **verified finite synthetic observation**, not a theorem asserted for every modulus or any original unresolved chart.

## Exact reproduction

- Source: original RQT-619 data, SHA-256 `97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021`.
- `research/rqt669.py`: Python 3 standard library, direct integer arithmetic; all 27 source charts, 243 identity-coordinate checks, 16 synthetic unit powers, finite permutations of 4–4096 points and full cycle decompositions.
- `research/RQT-669-results.json`: complete exact certificate, locally verified SHA-256 `1e755bad074cc79dbc60a36ba4320dbec2990c44cf03a303a0ba9b9347b65f17`.
- The original 27 charts were audited symbolically and at identity; **the finite nonidentity numerical actions are synthetic only**.

## Status and next bound

No discovered original nontrivial unit or ordinary norm−2 integer root; no new all-scale exclusion. Selected ledger **82/135 excluded (60.74%), 53 unresolved across 27 canonical sign-orbits. Root 19 OPEN; original 22D Wall NOT REPLAYED.**

**RQT-670 next natural bound:** Construct exact finite congruence **obstruction screens for candidate Pell units and seed pairs** in the actual 27 charts, using the subgroup gates and original quadratic integrality, but do not treat absence of candidates under a finite search as an all-scale exclusion.

`{{i}} · .dlw`
