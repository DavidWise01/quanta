# RQT-668 — Exact Affine-Lattice Pell Stabilizer

## Executive finding

RQT-667 proved a conservative sufficient Pell-unit gate, `U≡1, V≡0 (mod aD)`, to preserve the integer coordinates of the 27 unresolved canonical quadratic charts. RQT-668 **replaces that bound with exact necessary-and-sufficient arithmetic conditions for preserving the entire affine integer-coordinate chart**, not merely norm-specific solution points.

For the original integral quadratic
```
G(u,t)=r₀u²+r₁ut+r₂t²+r₃u+r₄t+r₅,
a=r₁²−4r₀r₂>0, h=r₁r₃−2r₀r₄,
D=|2r₀|,  z=at+h,
y=2r₀u+r₁t+r₃,
```
a Pell transformation from any integer norm-one unit `U²−aV²=1` acts by
```
z′=Uz+aVy,   y′=Vz+Uy.
```
Let `C=(U−1)h/a`. This transformation maps the **full ambient affine integer-coordinate chart to itself** if and only if:

1. `a | (U−1)h`, so `C∈ℤ`;
2. `D | V(a−r₁²)`;
3. `D | (U−r₁V−1)r₃+Vh−r₁C`.

To prove necessity and sufficiency, substitute `y=r₁t+r₃+Dk`, where t,k are arbitrary integers, into the transformed integer formulas:
```
t′ = Ut+Vy+C,
y′−r₁t′−r₃
  = V(a−r₁²)t
    +(U−r₁V−1)r₃+Vh−r₁C
    +D(U−r₁V)k.
```
The first condition is precisely integer parameter recovery. The latter two are precisely divisibility of the coefficient of t and the constant term by D. Since the transformation has determinant one, its restriction to the preserved full-rank affine lattice is bijective. The norm is automatically preserved by the Pell-unit identity.

**Exact parameter-integrality modulus:** `U≡1 (mod a/gcd(a,h))` (positive gcd). Across all 27 original charts, **canonical orbit 67** has `a|h`, so this parameter-integrality condition is automatic for every integer U; the other 26 have a nontrivial residual modulus. This says nothing about whether any suitable nontrivial Pell unit was found for those charts.

## Synthetic test: 16 → 1

For `G(u,t)=u²−2t²−1`, `a=8,h=0,D=2`. Its actual norm-one unit `(U,V)=(3,1)` already meets the **exact** gate and maps `(u,t)=(1,0)` to `(3,2)` with `3²−2·2²−1=0`.

The RQT-667 conservative gate required `U≡1, V≡0 (mod 16)`, first reached by the **16th power**. The new exact ambient-lattice gate succeeds at the **first power**. All 16 powers were checked by exact original-coordinate substitution, not just Pell norm. This is a synthetic efficiency improvement, **not 16× faster global root discovery**.

## Reproduction and evidence boundary

- Original RQT-619 coefficient source SHA-256: `97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021`.
- Exact per-orbit certificate: `RQT-668-results.json`, SHA-256 `e74a256fc91c1bf3e08818f2d93f1a537e604958b514c216284409fa03b59e13`.
- Python 3 standard-library verification: `research/rqt668.py`, covering 27 coefficient identities, 243 exact identity-map coordinate checks, and 16 synthetic recurrence powers.
- **Not claimed:** this is not minimal among automorphisms restricted only to the norm-equation solution subset. It is exact for the entire ambient integer-coordinate chart. No verified nontrivial unit, original integer seed, new whole-family exclusion, or original 22D Wall replay was found in the 27 real charts.

**Selected ledger unchanged:** 82/135 all-scale excluded (60.74%), 53 unresolved across 27 canonical sign-orbits, **Root 19 OPEN**.

## RQT-669 next natural bound

Compute the finite modular action of *candidate* Pell transformations subject to these three exact conditions, determine subgroup closure and representative orbits for synthetic verifiable cases, and only claim genuine original seeds when both original integer-coordinate recovery and the full norm equation pass.

`{{i}} · .dlw`
