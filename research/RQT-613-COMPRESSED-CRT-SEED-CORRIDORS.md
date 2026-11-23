# RQT-613 — Compressed CRT Seed Corridors

## Verified execution
RQT-613 independently reopened the RQT-611 all-exponent 7-adic seed filters, the rederived RQT-591 exact 4×4 Gram, the original RQT-583 Pell equations and RQT-612 finite search certificate.

For selected families **2** and **24**, the necessary parameter restrictions are, respectively:
- family 2: t mod 49 ∈ {13,20,27,34}
- family 24: t mod 49 ∈ {15,22,29,36}

The script independently recomputes these classes from the full norm equation **modulo 343** before constructing the wheel. Beware: the norm equation modulo 49 alone allows seven t-classes; the four-class condition is a projection of the stronger modulo-343 norm gate.

The compressed CRT wheel combines modulus 49 and primes 31,29:
```
M=49*31*29=44051
allowed residues in each family = 4*17*16 = 1088
wheel SHA256 of comma-separated ascending residues (family 2):
6d181f89dab733ac7694ba23877c88924358f7dc29796a9489e50a1ce30b68b0
```
The wheel preserves **1088 / 44051 ≈ 2.4699%** of t residues.

## Exact regression and wider search
Both families reproduce RQT-612's **[-1,000,000,+1,000,000]** baseline, with 49,397 wheel candidates and zero final survivors by prime 97.

The new exact interval for **each family** is **[-20,000,000,+20,000,000]**, totaling **80,000,002 family-parameter values** across the two families. Each wheel initially enumerates **987,942** t candidates by arithmetic progressions. After the same RQT-612 prime filters, **8** candidates per family remain at prime 97. All are known *not to have integer-square discriminants*. Additional independently computed prime-residue gates 101,103,107,109 reduce survivors per family to **3,2,1,0**.

Final surviving t candidates: **0/2 families**. This is a **finite exact exclusion certificate** for the two expanded search intervals. The generated machine-readable file `RQT-613-results.json` records ascending CRT wheel residues, hashes, stage counts and rejected discriminant residues; its SHA256 is
`b74e24fd0d60f61583cf8c224ba9ea003eed66767257df448fc1c1c8b2c99a94`.

## Honest scope and status
- All-scale selected-family exclusions: **82 of 135 (60.74%)**, unchanged.
- Selected unresolved: **53**, unchanged.
- New full-family exclusion: **0**.
- The 135 corridors do not exhaust the rank-four lattice.
- No exact integer norm−2 vector, no original 22D Wall replay.
- Root 19 remains **OPEN**.

## Next bound — RQT-614
Shift from repeatedly enlarging finite windows toward compact arithmetic structure: test discriminant congruence periodicity and generalized Pell orbit restrictions against the surviving local CRT progressions; keep a finite-window certificate separate from any theorem about all t.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
