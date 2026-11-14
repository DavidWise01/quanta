# RQT-346 — Authentic adjacent-slope prime-square descent

**Status: exact executed local obstructions and sharp real-cone thresholds. Original integral roots 18–21 remain OPEN.**

## Authentic source and coordinate family
Use the unmodified F4 from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`. For integers n>0 and d in {-1,+1}, define m=n+d and ternary plane vectors `x=(-m*a,b,n*a,c)`. Its Gram is `G(n,d)=T(n,d)^T F4 T(n,d)`.

Let `K` be the exact Schur complement after eliminating coordinates (x1,x3). Since the eliminated 2x2 block is negative definite, the maximum attainable real norm for fixed (x0,x2)=(-(n+d),n) equals `cone(n,d)=[-m,n] K [-m,n]^T`. A rational isotropic vector is possible only if this maximum is nonnegative.

## Refined first real-feasible denominators
The exact verifier checks the complete integer range below each threshold:

| m-n | Last real-infeasible denominator | First with positive Schur maximum | Slope |
|---:|---:|---:|---|
| -1 | 187 | **188** | 187/188 |
| +1 | 836 | **837** | 838/837 |

This refines but does not contradict RQT-345's outward rational interval thresholds of 187 and 834; those earlier values were necessary, not sufficient.

## Local obstruction lemma
Let p be prime and x a primitive ternary vector modulo p. If `x^T G x=0 mod p` and the gradient `2Gx` vanishes modulo p, then for every lift `x+pz` the quadratic norm is unchanged modulo p². Thus a primitive mod-p solution is *not* liftable to mod p² if its norm modulo p² is nonzero. If the gradient is nonzero modulo p, a solution lifts by choosing a digit in one coordinate. Therefore counting smooth mod-p roots and singular roots whose norm already vanishes modulo p² is a complete primitive p²-solvability test.

## Exact executed residue census

| Plane | Prime p | Primitive zeros modulo p | Smooth zeros | Singular zeros lifting modulo p² | Conclusion |
|---|---:|---:|---:|---:|---|
| 189/190 (n=190,d=-1) | 17 | 16 | 0 | 0 | **No rational isotropic vector in this plane** |
| 838/837 (n=837,d=+1) | 83 | 82 | 0 | 0 | **No rational isotropic vector in this plane** |
| 187/188 (n=188,d=-1) | 3 | 14 | 12 | 2 | No obstruction at p=3 |
| 839/838 (n=838,d=+1) | 3 | 14 | 12 | 2 | No obstruction at p=3 |

All `p^3-1` nonzero ternary residues are traversed for each p, including p=83. For the excluded cases, every primitive residue root has zero gradient modulo p and a norm nonzero modulo p². No primitive p² root exists. An actual rational isotropic point, normalized to a primitive integer ternary triple, would give a primitive solution modulo p², contradiction.

**Do not infer rational isotropy from local survival** at p=3; additional places and the global equation remain unverified.

## Verification
Reproducible Python/SymPy: `research/rqt346-prime-square-descent.py`. The independently executed local original-lattice certificate is `/mnt/data/rqt346_bad_prime_certificate.py`. All comparisons, quadratic norms and residue tests are exact integers/rationals.

## Next RQT-347
Construct an explicit full-rank rational isotropic point, or implement a general ternary rational-isotropy test with prime factors of the discriminant for promising slopes. Avoid extrapolating from a handful of tested primes or treating local witnesses as exact integer roots. If a primitive integer isotropic u with gcd(F4u)=1 appears, apply the RQT-334 Bezout construction, verify original root18's norm/parity/divisibility, then test the Wall orthogonality of roots19–21.

## Provenance
All modular computations descend from one original F4/H4 source, not independent original witnesses. The 3x3x3 cubit and Josophene/Juliet time-angle constructs are iteration metadata.
