# RQT-395 — The Integer Gate

Date: 2026-11-15. Parent: RQT-394, exact global cone.

## Mathematical distinction

The root-19 vector in the fixed RQT-388 basis is B(x,y,z). Its exact norm condition is

f z² + 2(cx+ey)z + (ax²+2bxy+dy²+2) = 0,

where (a,b,c,d,e,f) are the six independent entries of Q=BᵀF₄B.

The RQT-394 corridor is **necessary** for all integral solutions:

177065/100000 < x/y < 178600/100000, y ≠ 0.

Let L=cx+ey and D=L²-f(ax²+2bxy+dy²+2).

For z to be an integer, exact arithmetic requires D=t²≥0 for an integer t,
and at least one of (-L+t) or (-L-t) must be divisible by f.
Then z=(-L±t)/f. Direct norm substitution is the final witness.

The example (x,y)=(16,9) has positive nonsquare D, so it fails.

## Verification boundaries

The script research/rqt395-integer-gate.py performs finite enumeration
inside the globally proven slope wedge for 1 ≤ y ≤ --max-y. It does not
prove global exclusion. A true root19 requires the exact original F₄ norm
and the independent H₄ orthogonality already encoded by the RQT-388 kernel.

Root18: first-stage accepted. Root19: OPEN. Root20: OPEN.
Root21: conditional. The full 21-reflection word: OPEN.

## Visual story

The continuous amber cone crosses a discrete cyan lattice. Only points
passing a perfect-square discriminant and integral third-coordinate test
can reach the root19 door. The conceptual illustration is not proof.

The full-resolution JPG and an HTML with an embedded JPEG are available as
conversation artifacts. This repository record intentionally does not
claim the binary JPG was uploaded.
