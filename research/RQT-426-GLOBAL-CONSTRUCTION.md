# RQT-426 — Denominator-Free Global Rational Construction Gate
Date: 2026-11-16. Full original RQT-401 candidate-successor Gram; predecessor18 position unverified.

## New global theorem
For a primitive integer four-vector (w,d) satisfying w^T A w=-d² with d>0, gcd of the three spatial numerator coordinates w must be 1. Indeed g=gcd(w) implies g² divides d², hence g divides d. If g>1 the four-vector is not primitive. So the primitive spatial numerators alone exhaust all primitive rational witnesses, without independently enumerating denominators.

## Executed full-matrix search
Use the unimodular transformed form C=T^T(Q/2)T, T=[[-9,-25,0],[-5,-14,0],[0,0,1]]. Enumerate every primitive spatial vector in [-120,120]^3. Compute N=-w'^T C w' exactly, pass it through lossless modular-square filters (64,63,65,11,17,19), and check integer-square N with isqrt. Any witness would then be verified by direct F4 backmapping.

- Primitive numerators checked: 11,608,130
- Positive N: 11,596,542
- Modular-square survivors: 45,780
- Exact squares N=d²: 0
- Verified rational witnesses: 0

**Bound:** any primitive rational witness has at least one transformed numerator coordinate with absolute value >=121. No bound on denominator d was imposed. This is a finite numerator-height exclusion, not a global impossibility proof.

## Complete but not effective construction
Increasing radius indefinitely enumerates every primitive spatial numerator, and the RQT-414 rational-existence theorem guarantees a rational witness occurs at some finite radius. There is no known effective bound for its size from these results, and this runtime only executed radius 120.

## ASCII
```
         RQT-426 :: DENOMINATOR-FREE SIEVE
      +------------------------------------+
      |    C = T^T (Q/2) T                |
      |                |                   |
      |   primitive w' in [-120,120]^3    |
      |                |                   |
      |        N = -w'^T C w'             |
      |                |                   |
      |    11,608,130 primitive triples   |
      |    11,596,542 positive N          |
      |       45,780 pass square filters  |
      |                |                   |
      |          N = d^2 ?                |
      |               NO                   |
      |         ROOT19 OPEN               |
      +------------------------------------+
```

Rational existence PROVEN abstractly. Explicit rational witness NOT YET FOUND. Root19 OPEN, root20 OPEN, root21 conditional. All mirrored owned corpus artifacts have one source ancestry. The separate generated JPG is conceptual, not proof.
