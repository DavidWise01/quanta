# RQT-666 — Conditional Pell Recurrence & Exact Seed Construction Gate

## Executive result

Reopened RQT-619's exact six-coefficient source certificate (SHA-256 `97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021`). For each of the 27 canonical unresolved sign-orbits, constructed its exact generalized Pell coefficients:
```
a=r1²−4r0*r2, h=r1*r3−2r0*r4, c=r3²−4r0*r5, N=h²−a*c
z=a*t+h; z²−a*y²=N.
```
Checked the first **128 exact convergents p/q of sqrt(a)** in each orbit—**3,456 convergents** overall. All coefficients a were positive and nonsquare. The norm `p²−a*q²` was calculated exactly.

| Measurement | Result |
|---|---:|
| Canonical orbits | 27 |
| Convergents per orbit | 128 |
| Exact convergents checked | **3,456** |
| Norm +1 convergents | **0** |
| Norm −1 convergents | **0** |
| Generalized target norm N matches | **0** |
| Integral parameter recoveries | **0** |
| Original integral (u,t) seeds | **0** |

## Mathematical recurrence theorem (conditional)

If `U²−aV²=1` and `z²−ay²=N`, then
```
z' = U*z + a*V*y
y' = V*z + U*y
```
satisfies `z'²−a*y'²=N` exactly by expansion. However, a valid original chart solution also requires
```
(z'−h) % a == 0
t'=(z'−h)//a
(-r1*t'−r3 ± y') % (2*r0) == 0
u'=(-r1*t'−r3 ± y')//(2*r0)
G(u',t')=0.
```
**A Pell recurrence need not preserve these latter congruences**, and no verified unit or starting seed was produced within this finite convergent search. No recurrence trajectory is claimed to be instantiated.

Even a legitimate norm −1 unit can be squared to produce a norm +1 unit, but this experiment found no convergents of either norm in the tested prefix.

## Scope

- A continued-fraction prefix is **not** a proof of the absence of Pell units. In particular, this does not exclude a fundamental unit at a larger index.
- The first 128 convergents of sqrt(a) are not a complete search for inhomogeneous Pell seeds.
- The all-scale selected family ledger remains **82/135 excluded (60.74%), 53 unresolved across 27 canonical sign-orbits**.
- No new whole-family exclusion, original integer norm−2 seed, or original 22D Wall replay. **Root 19 OPEN.**

## Evidence

Exact standalone Python verifier: `research/rqt666.py`; full `research/RQT-666-results.json` is the machine-readable 27-orbit certificate with all unit/target records; SHA-256 `78eb19434ee48c8bbef6d5bd81f88a2d895323fddc1a0d19a819396e53571d88`.

## RQT-667 — Next natural bound

Determine **which exact congruence subgroup of Pell norm-one transformations preserves both z≡h (mod a) and the original-coordinate integrality gate**. Build this algebraically and test it on synthetic exact seeds before claiming it advances the still-open original equations. Prioritize proof of mechanism and root recovery, not repeated convergent enumeration.

`{{i}} · .dlw`
