# RQT-333 — Conditional Schur search, authentic frozen lattice

**Status: exact finite exclusion for norm -2 and norm 0 at heights 1011..1020. Original roots 18–21 OPEN.**

## Source ancestry
Frozen F4: `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`. Integral unimodular change T, and reduced J=T F4 T^T: `DavidWise01/stoicheion/research/rqt/RQT-254-unimodular-second-height.md`. This is not the constructed bridge lattice.

## Exact conditional bound

For fixed positive t=y0, let z=(y1,y2,y3), P=-J[1:4,1:4] positive definite, v=P^-1 J[1:4,0], beta=J00+v^T P v>0. Then for target q in {-2,0},

```text
q=beta*t²-(z-tv)^T P(z-tv)
R=beta*t²-q
```

Let K=(P^-1[0:2,0:2])^-1, δ1=y1-tv1, δ2=y2-tv2. Projection onto y1,y2 satisfies

```text
K11*δ1²+2*K12*δ1*δ2+K22*δ2² <= R.
```

Complete the square with alpha=K11-K12²/K22>0:

```text
alpha*δ1²+K22*(δ2+(K12/K22)*δ1)² <= R.
```

Therefore y1 is bounded by the first term, and after fixing integer y1, y2 lies in a conditional finite interval. All endpoints are rounded **outward** and the inequalities certified using Python rational Fractions. Given t,y1,y2, solve J-norm equation as exact integer quadratic in y3 using discriminant and integer isqrt. This imposes **no y3 cutoff**.

## Execution results

| t=y0 | norm -2 pairs | norm 0 pairs | square discriminants each | exact roots each |
|---:|---:|---:|---:|---:|
|1011|79998|79998|0|0|
|1012|80124|80124|0|0|
|1013|80284|80284|0|0|
|1014|80472|80472|0|0|
|1015|80618|80618|0|0|
|1016|80788|80788|0|0|
|1017|80946|80946|0|0|
|1018|81090|81090|0|0|
|1019|81256|81256|0|0|
|1020|81392|81392|0|0|
|**Total**|**806968**|**806968**|**0**|**0**|

Central symmetry y->-y handles the negative slices. We checked **1,613,936 target-specific candidate pairs**. This is exhaustive only over |y0|=1011,...,1020, not proof of global absence.

The RQT-254 original result (|y0|<=1000) was **not rerun**; RQT-332 covered 1001..1010. Combined, contingent on RQT-254 evidence, any norm -2 root must satisfy |y0|>=1021.

## Next natural bound RQT-334

Seek a constructive primitive isotropic vector in the authentic lattice using rational conic parametrization and exact height-controlled lifting rather than repeatedly extending small height intervals. Once a primitive norm-zero u with gcd(Fu)=1 is found, use Bezout to construct a norm -2 root and test first parity/completion, then proceed to roots 19–21. Distinguish isotropic existence from an integral explicit witness.

## Evidence routing

Keep append-only math evidence, 3x3x3 nested cubit spatial indexing, Josophene/Juliet and time-angle slots separate from mathematical witness claims.
