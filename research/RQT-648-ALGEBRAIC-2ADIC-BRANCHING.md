# RQT-648 — Algebraic 2-Adic Branching and Hensel Existence

## Executive summary
Reopened the exact RQT-619 archive of 27 canonical binary norm equations (53 original unresolved family IDs) and proved two all-depth local statements.

**Theorem A — zero-or-four pair lifting.** Put `G(u,t)=r0*u²+r1*u*t+r2*t²+r3*u+r4*t+r5`. Let `a=r1²−4r0r2`, `h=r1r3−2r0r4`, `c=r3²−4r0r5`. A paired residue `(t,y)` modulo `m=2^k` satisfies
```
y²−a*t²−2*h*t−c ≡ 0  (mod m)
y ≡ ±(r1*t+r3)       (mod gcd(m,|2r0|)).
```
All 27 archived equations have `v₂(|2r0|)=3`. For `k>=4`, therefore, `gcd(m,|2r0|)=gcd(2m,|2r0|)=8`, so each of the four candidate children `(t+αm,y+βm)` retains the second condition. Their first polynomial differs from the parent's by
```
m*(2βy−2α(at+h)) + m²*(β²−aα²),
```
which is divisible by `2m` for even m. Consequently, **either all four children satisfy the next equation or none do**. This is an exact theorem at every k>=4 for these forms, not merely the RQT-647 finite observation.

**Theorem B — a 2-adic solution for every canonical orbit.** Every one of the 27 archived polynomials G has a mod-2 root `(u0,t0)` with odd derivative `∂G/∂u=2r0*u+r1*t+r3`. Fix t=t0 (an ordinary integer, 0 or 1). By the elementary Hensel step, from `G(u_n,t0)≡0 mod 2^n`, set
```
b_n = (G(u_n,t0)/2^n) mod 2
u_(n+1) = u_n + b_n*2^n.
```
Because the derivative stays odd, this satisfies `G(u_(n+1),t0)≡0 mod 2^(n+1)`. The nested residues define `u∈Z₂` with `G(u,t0)=0`. This proves **local 2-adic solvability in all 27 canonical orbits**. It is not a proof of ordinary integer solvability or an integer norm−2 seed.

## Independent finite checks
- Every Hensel witness was computed exactly through `2^24`.
- The 27-orbit pair-level audit from 16 to 32 contains **1,544 admissible parent pairs**: **736** have zero children and **808** have four children, giving 3,232 next-level compatible pairs.
- None had one, two, or three children.
- All 27 canonical ids are represented; shared source ancestry is not independent corroboration.

## Evidence and scope
- Reproducer `research/rqt648-hensel-branching.py`
- Complete local JSON `RQT-648-results.json`, SHA256 `8d0f8eb7cb5985929af78d14356f3a31fc260fc938d20fc93645901830930440`
- Input exact RQT-619 certificate, SHA256 `97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021`.
- **No ordinary integer norm−2 root, no new whole-family exclusion, no original 22D Wall replay.**

Selected ledger: **82/135 all-scale excluded (60.74%), 53 unresolved**, represented by 27 canonical sign-orbits. Selected corridors do not exhaust the original lattice. **Root 19 OPEN**.

## RQT-649 next natural bound
Audit the difference between 2-adic local existence and original integer solvability by combining distinct odd-prime local restrictions and discriminant-integrality conditions. Focus on actual integer seed recovery, not endlessly extending an already proved 2-adic branch.

`{brace{n}[box[n](torroid(n))]} · {{i}} · .dlw`