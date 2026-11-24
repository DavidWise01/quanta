# RQT-664 — Exact Near-Square and Continued-Fraction Audit

## Executive result
Reopened the original RQT-619 JSON certificate, SHA-256 `97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021`, and evaluated the exact discriminant `F(t)` of every one of the **27 canonical quadratic equations** for all integer `-100000 <= t <= 100000`.

For `G(u,t)=r0*u²+r1*u*t+r2*t²+r3*u+r4*t+r5=0`, the required square polynomial is
```
F(t) = (r1²−4r0*r2)t² + 2(r1*r3−2r0*r4)t + r3²−4r0*r5.
```
With `y=floor(sqrt(F))` for `F>=0`, the integer square gap is `min(F−y²,(y+1)²−F)`. If a gap is zero, the code attempts `u=(-r1*t-r3 ± sqrt(F))/(2*r0)` with exact integrality and original `G(u,t)=0` checks.

**Observed:** 5,400,027 parameter–orbit checks; 5,398,223 nonnegative discriminants; **0 exact squares** and **0 recovered integer roots** in this finite interval. This independently recovers the main zero-square outcome of RQT-663 using an unsieved direct scan.

## Five closest absolute square gaps

| Canonical orbit | t | Absolute nearest-square gap |
|---:|---:|---:|
| 67 | 0 | 1,353,594,672 |
| 2 | 68,501 | 12,359,540,640,053 |
| 34 | -359 | 560,215,866,793,865 |
| 112 | -3 | 1,096,164,598,285,245 |
| 81 | 15,784 | 1,209,984,708,698,152 |

**Comparability warning:** absolute gaps should not be compared as if they were normalized approximation quality across different coefficient scales. The full JSON records exact gap numerators and adjacent-square spacing denominators for the five best cases per orbit.

## Continued-fraction context

The audit computes **12 exact convergents of sqrt(a)** for each orbit (324 records total), where `a=r1²−4r0r2>0` is the leading coefficient of `F`. Every convergent stores its integers `p,q` and exact Pell residual `p²-aq²`. These are diagnostic approximations to the associated *homogeneous quadratic irrational*, **not solutions to the inhomogeneous generalized Pell target**. The search for actual roots still depends on `F(t)` being an exact square followed by integral original-coordinate reconstruction.

This experiment is a **bounded near-square census**, not a new all-scale exclusion, global Diophantine approximation theorem, or proof that no integer solutions exist outside the interval. No original 22D Wall replay.

## Reproduction

- `research/rqt664.py`: Python 3 standard-library exact audit (no floating point).
- `research/RQT-664-results.json`: complete per-orbit five-closest gaps and all 324 exact CF convergents.
- Result SHA-256: `ebe9a6757a21e958ee91f07f8628f2d1b13c8057f32809fc6ffd1b12b661da6c`.
- Distinct image style: cyanotype natural-history scientific plate, available as conversation JPEG.
- All source claims derive from the inherited owned RQT corpus; repeated computations are not independent witnesses.

**Classification unchanged:** 82/135 selected families excluded all-scale (60.74%); 53 unresolved across 27 canonical orbits; **Root 19 OPEN**.

## RQT-665 — Next natural bound
Target the inhomogeneous generalized Pell equation directly using exact reduction and arithmetic congruences; compare near-square metrics normalized by adjacent-square spacing. Only promote a found `(u,t)` if integer reconstruction and original norm checks both pass.

`{{i}} · .dlw`
