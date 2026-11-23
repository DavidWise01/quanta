# RQT-621 — Third-Level Singular 2-Adic Branch Reduction

## Exact result
The RQT-620 source certificate was reopened with its SHA-256 confirmed as `c23027155b581a22983649642141ba95d0a00c081ece6c8b1215443a2f97b7b3`.

There are six canonical cases whose second normal form `S` has a singular root modulo 2: **29, 30, 56, 62, 81, 92**. For each singular root `(u0,t0)`, both gradient entries are even, giving
`S(u0+2x,t0+2y) ≡ S(u0,t0) (mod 4)`.
The six split rigorously:

- Families **56,62,81,92** have `S(u0,t0) ≡ 2 (mod 4)`. Every lift of *that fixed singular residue branch* fails `S ≡ 0 (mod 4)`. This proves an all-scale obstruction for these four **branches only**; their families retain other regular 2-adic branches.
- Families **29,30** have `S(u0,t0) ≡ 0 (mod 4)` and admit the exact integer third normal form
```
S(u0+2x,t0+2y) = 4T(x,y).
Q = 8S = 32T on the corresponding translated coordinates.
```
The reduced `T mod 2` has **two nonsingular roots for family 29**, and **one for family 30**. Each regular root was explicitly Hensel-lifted to `T=0 (mod 2^13)`; the translated S identities and norms were independently checked.

## New all-exponent lower bounds
For k≥6, the third-level regular roots contribute new disjoint solution classes beyond the first-level R and second-level S regular branches:
```
C_29(k) >= 6 × 2^k.
C_30(k) >= 5 × 2^k.
```
These are certified lower bounds, not claims that every possible branch has been exhausted.

The third-level T of **family 29** also has **one singular mod-2 root** whose deeper behavior remains unclassified. Family 30's T has no singular mod-2 root. Four blocked S branches are not whole-family exclusions.

## Reproducibility
- Standard-library script `research/rqt621-third-level.py` consumes exact RQT-620 JSON and verifies each translation, root classification, Hensel lifts and archived finite counts.
- Locally generated full `RQT-621-results.json` SHA-256: `5d0a88735d0bdb0d7cc9ca3a51381475debb5e580cc8233e85a68711d3c1be92`.

## Scope
No exact ordinary integer norm −2 root, no original 22D Wall replay. Selected family ledger unchanged: **82/135 all-scale excluded (60.74%), 53 unresolved across 27 canonical sign-orbits**. The 135 corridors do not exhaust the full rank-four lattice. **Root19 OPEN.**

## Next natural bound — RQT-622
Investigate the remaining singular root of family-29 third-level T: exact mod-4 obstruction or a fourth integral normal form, then derive the corresponding all-exponent contribution. Track the terminal status of the **branch**, not the family, and preserve immutable evidence ancestry.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`