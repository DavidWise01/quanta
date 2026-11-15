# RQT-391 — The Interior Search: exact two-coordinate cylinder for root19

**2026-11-15 | Exact original F4 PASS | Root19 OPEN.**

## The new mathematical advance

RQT-386 produced an explicit original integer norm−2 root; RQT-387 proved its first-stage rank/order reduction. RQT-388 built its exact saturated rank-three Wall successor kernel, with a reduced integral basis B. RQT-389/390 globally excluded x=0, y=0, z=0 in these fixed reduced coordinates.

This turn conducts an **exact 400,000,000-pair cylinder scan** in the still-open interior. Its distinctive feature is that **the third coordinate z is unrestricted**. It does not expand a three-dimensional finite box.

Let the exact original restricted Gram be Q=B.T F4 B and r19=B(x,y,z). Then

```text
r19.T F4 r19 = zvec.T Q zvec = -2
r19.T H4 r18 = 0  by construction of saturated B.
```

Writing
```text
a=Q00, b=Q01, c=Q02,
d=Q11, e=Q12, f=Q22,
```
solving for the third coefficient gives
```text
f*z² + 2(c*x+e*y)*z + (a*x²+2*b*x*y+d*y²+2) = 0.

Blin = c*x+e*y
Cpoly= a*x²+2*b*x*y+d*y²+2
Delta=Blin²-f*Cpoly.
z=(-Blin±sqrt(Delta))/f.
```

For each (x,y), an integer z requires Delta to be a **nonnegative exact integer square** and the numerator to be divisible by f. The program checks those conditions using arbitrary precision Boost `cpp_int`. It first rejects only discriminants which are **provably nonsquares modulo** any of 18 exact moduli (256,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61).

## Complete bounded two-coordinate cylinder

Search **all** (x,y) with both nonzero and within −10,000 to +10,000 inclusive. There are 20,001² total pairs and **400,000,000 interior pairs** after excluding 40,001 pairs on coordinate axes already ruled out globally by RQT-389.

| Exact outcome | Count |
|---|---:|
| Interior pairs tested | **400,000,000** |
| Reject by necessary quadratic-residue sieve | **399,991,618** |
| Survive modular sieve | **8,382** |
| Negative exact discriminant | **8,372** |
| Nonnegative but nonsquare exact discriminant | **10** |
| Perfect-square discriminants | **0** |
| Exact norm−2 root19 vectors | **0** |

The only ten pairs reaching nonnegative discriminants were:
```text
(-7715,-4353), (-7120,-4012), (-4702,-2636),
(-4241,-2389), (-1548,-872), (1548,872),
(4241,2389), (4702,2636), (7120,4012), (7715,4353).
```
For each one, the independent verifier recomputed Delta from the original F4-projected Gram and checked with exact `math.isqrt` that it was **not** a square. Those points appear in opposite pairs, as expected from quadratic symmetry. Another 2,000 seeded checks independently rebuilt the discriminant from its full Gram expression and confirmed the modular sieve never rejected a square.

**Certified finite conclusion**: Any exact root19 in this recorded, unimodular reduced rank-three coordinate system must satisfy
```text
max(|x|,|y|) >= 10001.
```
The third coordinate z was **not bounded at any stage**. This does NOT imply no root19 exists beyond that two-dimensional cylinder or in another coordinate basis.

## Reproduction

1. Regenerate the original reduced Gram and its saturated kernel:

```bash
python research/rqt388-exact-second-key.py --bound 30 --out /tmp/rqt388.json
```

2. Compile the exact C++ scanner and feed it all six independent Gram coefficients:

```bash
g++ -O3 -std=c++17 research/rqt391-root19-interior-cylinder.cpp -o /tmp/rqt391
python research/rqt391-gram-input.py /tmp/rqt388.json | /tmp/rqt391 10000 | tee /tmp/rqt391.log
```

3. Independently verify all ten nonnegative cases and 2,000 exact coefficient identities against frozen original F4/H4:

```bash
python research/rqt391-verify-cylinder.py /tmp/rqt388.json /tmp/rqt391.log
```

Machine-readable counts and the ten borderline coordinates are in `research/RQT-391-results.json`. The locally executed exact scan and replay output are conversation artifacts `/mnt/data/RQT-391-cylinder-results.txt` and `/mnt/data/RQT-391-replay.json`.

## Three-dimensional visual story

The new JPG **RQT-391-The-Interior-Search-3D.jpg** depicts a three-dimensional volumetric 9×9×9 GMA lattice around the glowing `||||` singlet, previous three excluded coordinate planes, a scanning probe through the remaining interior, and the locked root19 portal. The artwork is explanatory, not an original-root coordinate plot. The conversation includes the actual JPG; a self-contained 3D-style HTML story page is committed to `rqt391.html`. The JPEG binary is not yet in the GitHub repository.

## Next natural target — RQT-392

Rather than merely grow the next cylinder, investigate whether the exact ternary quadratic can be solved constructively by **rational conic/inhomogeneous norm methods**, incorporating the three permitted mod-2 coefficient classes and nonzero coordinate restrictions. Full root19 acceptance requires an explicit original integer vector meeting `r19.T F4 r19=-2` and `r19.T H4 r18=0`. Then root20 is a rank-two successor and root21 follows by the conditional cofactor theorem.

**Root18: first-stage accepted. Root19: OPEN. Root20: OPEN. Root21: conditional. Full 21-reflection word: OPEN.**
