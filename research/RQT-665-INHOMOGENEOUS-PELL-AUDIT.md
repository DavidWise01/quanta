# RQT-665 — Inhomogeneous Pell Identity and Normalized Near-Square Audit

## Executive result

All 27 canonical original integer quadratic charts were replayed for every integer parameter in `-100000 <= t <= 100000`, a total of **5,400,027 parameter–orbit checks**. Exactly **5,398,223** discriminants were nonnegative. **Zero** were perfect squares, so no original integer-coordinate seed was recovered in this finite window. An additional **276 distinct parameter probes outside the interval** were selected by taking plus/minus the first twelve continued-fraction denominators of `sqrt(a)` and their immediate neighbors, deduplicating and excluding the bounded interval. None had a square discriminant or an integer seed. These 276 probes are *not* an exhaustive outer search and are not claimed to solve the inhomogeneous Pell equation.

## Exact Pell identity

For each original equation `G(u,t)=r0*u^2+r1*u*t+r2*t^2+r3*u+r4*t+r5=0`, define:

```
a=r1^2-4*r0*r2
h=r1*r3-2*r0*r4
c=r3^2-4*r0*r5
F(t)=a*t^2+2*h*t+c
z=a*t+h; N=h^2-a*c
```

The exact identity `z^2-a*F(t)=N` was checked at every evaluated parameter. For the nearest square `y^2`, the generalized Pell residual is exactly `z^2-a*y^2-N = a*(F(t)-y^2)`. A genuine integer root requires `F(t)=y^2` and the coordinate recovery `(−r1*t−r3 ± y)/(2*r0)` to be integral, followed by the original `G(u,t)=0` substitution.

## Scale-aware near-square ranking

For nonnegative `F(t)`, let `s=isqrt(F(t))` and `gap=min(F(t)-s^2,(s+1)^2-F(t))`. The normalized gap is the exact rational `gap/(2*s+1)`. Candidates were ranked using **integer cross-multiplication**, not floating point.

| Rank | Orbit | t | Absolute gap | Adjacent-square spacing | Gap / spacing (approx.) |
|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 68,501 | 12,359,540,640,053 | 54,468,026,810,289,965,217,333 | 2.26914e-10 |
| 2 | 81 | 15,784 | 1,209,984,708,698,152 | 12,264,822,420,711,449,878,937 | 9.86549e-8 |
| 3 | 35 | 14,195 | 1,962,413,133,754,237 | 8,481,691,988,641,633,507,521 | 2.31370e-7 |
| 4 | 34 | 42,905 | 7,822,644,987,074,463 | 25,677,782,846,452,272,584,067 | 3.04646e-7 |
| 5 | 37 | −14,931 | 4,163,127,360,760,160 | 8,948,967,107,055,976,475,687 | 4.65208e-7 |

The previous absolute-gap record (orbit 67 at `t=0`) remains valid for **absolute** distance, but is not the smallest **normalized** miss. Neither metric constitutes an integer root.

## Scope and provenance

- Input certificate `RQT-619-results.json` SHA256: `97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021`.
- Exact standard-library verifier: `research/rqt665.py`.
- Full local JSON: `RQT-665-results.json` SHA256: `89f64930cf22fd6761dc774d79be42394e708c81742460115d85af1bf1fee2db`.
- No new all-scale family exclusion, ordinary integer norm−2 seed, or original 22D Wall replay.
- **Selected-family ledger unchanged: 82/135 excluded (60.74%), 53 unresolved across 27 canonical orbits, Root 19 OPEN.**

## RQT-666 natural bound

Use exact inhomogeneous Pell reduction to propose **candidate seeds outside a fixed t-window** by algebraically constrained arithmetic recurrences, not a generic continuation of brute force; validate original-coordinate integrality and the full quadratic before admitting any root.

`{{i}} · .dlw`