# RQT-342 — Exact 5-adic obstruction for an infinite family of full-support ternary slices

**Verified, finite modular proof with infinite-family consequence.** Original integer roots 18–21 remain OPEN.

## Frozen provenance

The original symmetric even Gram F4 is taken from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`, and authenticated by the known determinant. No synthetic bridge or substituted form is used.

## Coordinate three-space, without deleting a coordinate

For each integer k, consider the rational three-plane
```
x0 = -k*x2,
x=(-k*a,b,a,c), with a,b,c rational.
```
This plane can have full coordinate support and is not one of the four coordinate hyperplanes ruled out by RQT-341. Its exact ternary Gram is
```
T_k=[[-k,0,0],[0,1,0],[1,0,0],[0,0,1]],
J_k=T_k^T F4 T_k.
```

Any nonzero rational isotropic vector in this plane can be cleared of denominators and divided by its coordinate gcd to give a nonzero **primitive integer ternary** vector (a,b,c) with `(a,b,c) J_k (a,b,c)^T=0`. Therefore such a vector would necessarily reduce to a primitive solution modulo 25 (at least one coordinate nonzero mod 5).

## Exact exhaustive modular result

Since `J_k mod25` depends only on `k mod25`, testing all 25 residue classes proves a statement about **every integer k**. For each k residue, enumerate all `25^3=15,625` ternary residues, excluding those where all coordinates are divisible by five. Test the exact norm congruence mod25.

| k residue mod5 | primitive solutions mod5 | primitive solutions mod25 | result |
|---|---:|---:|---|
| 1 | 4 | **0** | **Rational isotropic vector impossible** |
| 0,2,3,4 | 24 | 600 | Mod25 test inconclusive |

Specifically, the five k classes `{1,6,11,16,21} mod25` have **zero primitive modulo25 roots**. Every k≡1 (mod5) falls in one of these, so the following is a rigorous **infinite-family** exclusion:
```
k ≡ 1 mod5  =>  no nonzero rational isotropic vector
in the original F4 plane x0=-k*x2.
```

For all other k classes, the existence of 600 primitive solutions modulo25 does **not** establish a rational isotropic point. Local solutions can fail to extend globally; their status is OPEN.

## What changed

RQT-340 found one anisotropic rational two-plane through a 2-adic squareclass. RQT-341 proved all coordinate hyperplanes exclude exact null vectors. RQT-342 now handles an **infinite family of non-coordinate three-planes**, using a new 5-adic obstruction. The earlier unsuccessful ternary-solver run is not relied upon.

## Source and witness scope

The 25 mod25 tests use the **same original Gram ancestry**; their arithmetic checks are reproducible, not independent source documents. The full rank-four F4 can still be rationally isotropic: excluded slices do not imply a global no-go theorem. No explicit root18 has been produced.

## Next natural target RQT-343

Focus exact rational solvers on `k not ≡1 (mod5)`, ideally with certified local-global ternary algorithms, or use a true four-variable rational quadric solver. If a rational null vector is found, primitive-integralize it and verify `gcd(F4u)=1`, RQT-334 root parity, and original Wall residual. Preserve literal integer coordinates and exact proof before declaring a successful root.

The nested {{i}}/{{j}}/{{n}} 3×3×3 construction and time/angular addresses are provenance metadata, not substitutes for rational or integral arithmetic certificates.
