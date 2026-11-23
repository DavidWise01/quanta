# RQT-599 — Exact Pell Period and Seed Gate

## Family 28
Certified squarefree coefficient from RQT-597:
```
d = 3580734425344222227352852171253793
N = 100*d = 4*A
X² − d Z² = K
X ≡ B (mod 2A)
Z ≡ 0 (mod 10)
```

## Exact finite computation
Using the standard exact continued-fraction recurrence for √d, with `m₀=0,q₀=1,a₀=floor(√d)`:
```
m_(n+1) = q_n a_n − m_n
q_(n+1) = (d−m_(n+1)²)/q_n
a_(n+1) = floor((a₀+m_(n+1))/q_(n+1))
```
Two million exact steps were executed. **The period did not close** within this bound. The terminal recurrence state was:
```
m = 48319755305916816
q = 23577184610196697
a = 4
```
For a nonsquare positive integer, the first occurrence of `a=2a₀` closes the period. The smallest positive Pell norm-one unit arises at the end of that period if even, or at twice the period if odd. Since no period closure was found in the first 2 million steps, **no norm-one unit is obtained among those initial convergents**. This is a finite computational bound; it does not refute the existence of a fundamental unit.

Separately, exact integer discriminant-square search on family 28 over `−50000≤t≤50000` checked **100001** parameters and found zero square discriminants and zero generalized Pell seeds in that window.

The executable code and machine-readable certificate are conversation artifacts, with step checkpoints and source-result SHA-256s.

## Correct interpretation
- A nontrivial integral norm-one Pell unit is guaranteed to exist for every positive nonsquare d. **It has not yet been explicitly computed here**.
- No generalized Pell seed has been recovered from the stated finite window.
- The RQT-598 conditional universal congruence stabilizer remains valid, but no actual orbit with an admissible seed has been certified.
- No new infinite-family exclusion; selected-ray ledger **82/135 excluded (60.74%), 53 unresolved**. These corridors do not exhaust the 4D integer lattice.
- Original 22D Wall replay not performed. Root19 OPEN.

## Next natural bound — RQT-600
Replace linear continued-fraction stepping with a faster exact infrastructure/continued-fraction period algorithm or a verified class-group/Pell solver able to return a compact *certified* fundamental unit. Keep independent coordinate-seed recovery as a separate gate; do not confuse the unit's existence with any solution of the inhomogeneous generalized Pell equation.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
