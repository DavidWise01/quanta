# RQT-645 — Generalized Pell Targets and Exact Integer-Coordinate Recovery

## Result

Reopened the original exact RQT-619 27-family binary norm coefficient certificate and RQT-626 27-target generalized Pell certificate. Verified all six integer coefficients for every identity and the target relation `N=h²-ac`.

For `Q(u,t)=2(r0u²+r1ut+r2t²+r3u+r4t+r5)=0`, write `L=r1t+r3`, `F(t)=at²+2ht+c`, with `a=r1²-4r0r2`, `h=r1r3-2r0r4`, `c=r3²-4r0r5`. Then
```
F(t) = L(t)² - 4r0(r2t²+r4t+r5)
z = at+h,   N=h²-ac
z² - aF(t) = N.
```
If `y²=F(t)`, the exact integer coordinate is
```
u = [-L(t) ± y] / (2r0).
```
It is integral if and only if `y ≡ ±L(t) (mod |2r0|)`. Given this congruence, the recovered u satisfies Q(u,t)=0 **exactly** (not merely modulo a finite base). Every actual integer norm−2 root in these selected corridors must pass both Pell and coordinate gates.

## Exact modular preview

Enumerated all `(t,y) mod m` with `y²≡F(t) mod m`, retaining only pairs satisfying the **necessary coordinate congruence modulo gcd(m, |2r0|)**. Summed across 27 canonical orbits:

| m | Pell square compatible pairs | Coordinate-compatible pairs | Pell-compatible t residues | Recovery-compatible t residues |
|---:|---:|---:|---:|---:|
| 8 | 680 | 386 | 216 | 216 |
| 16 | 1728 | 1544 | 432 | 432 |
| 32 | 3552 | 3232 | 784 | 704 |
| 121 | 6182 | 6182 | 2992 | 2992 |
| 169 | 8658 | 8658 | 4329 | 4329 |

At modulus 32, precisely ten orbits lose eight t-residues each: **28,31,34,37,55,61,64,67,109,112**; each shrinks **24→16**. This is a necessary modular projection only; it is not a new whole-family exclusion and the square-root congruence modulo m is weaker than a genuine integer square.

All 27 orbit equations have the same **absolute original coordinate denominator** `|2r0|=9603309702921447656` in their archived coordinates. Nothing about the shared denominator makes the 27 independent mathematical source roots.

## Reproducibility

- Exact standard-library verifier: `research/rqt645-pell-coordinate-gates.py`; consumes the original exact RQT-619 and RQT-626 JSON certificates.
- Full local `RQT-645-results.json` SHA256: `d3d6049713859a25c0779dac48c15562452d4c8b38815bc97b2be298e7fa48ee`.
- Both input fingerprints are preserved in the complete local certificate, with results for all 27 orbits and five modular bases.

**Status:** 82/135 selected corridors excluded all scale (60.74%); 53 unresolved in 27 canonical sign-orbits. No new exclusion, actual integer norm−2 seed or original 22D Wall replay. **Root 19 OPEN**.

## RQT-646 next bound

Lift the ten newly sharpened mod-32 parameter gates to mod-64 and mod-128, checking whether additional square-compatible residues fail the original-coordinate recovery condition. Preserve exact ancestry and avoid confusing finite congruence exclusions with full-family impossibility.

`{brace{n}[box[n](torroid(n))]} · {{i}} · .dlw`