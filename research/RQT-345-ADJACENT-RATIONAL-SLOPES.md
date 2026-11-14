# RQT-345 — Adjacent rational slopes: exact denominator thresholds and local-survival limits

**Status:** Exact arithmetic certificate completed on original frozen stoicheion RQT-242 F4. No rational isotropic vector or integral root 18 has been constructed; roots 18–21 remain OPEN.

## Original source and coordinate change
The original F4 from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py` is checked by its exact determinant. From RQT-344, any rational isotropic vector must have a defined slope `k=-x0/x2` with
```
19893/20000 < k < 2503/2500.
```
Write `k=m/n` in lowest terms, with `n>0`. A full-support ternary slice uses
```
x=(-m*a,b,n*a,c)
T(m,n)=[[-m,0,0],[0,1,0],[n,0,0],[0,0,1]],
G(m,n)=T^T F4 T.
```
For the smallest numerator differences `d=m-n=+-1`, the strict inequalities give:

| d | slope | denominator threshold |
|---:|---|---:|
| -1 | 1-1/n | n>20000/107; minimum integer **187** |
| +1 | 1+1/n | n>2500/3; minimum integer **834** |

These are **necessary real-cone thresholds**, not a guarantee of isotropy.

## Exhaustive primitive local census

For every `d in {-1,+1}`, for every denominator residue `n mod32`, compute the exact restricted Gram `G(n+d,n)` modulo 32. Enumerate all `32^3=32768` ternary residues `(a,b,c)`, requiring at least one coordinate odd, and check `(a,b,c)^T G(a,b,c)=0 mod32`. In **every one of the 32 denominator classes** exactly **2048** primitive residues survive.

Repeat for every `n mod25`, checking all `25^3=15625` triples with at least one coordinate prime-to-5. In **every one of the 25 denominator classes** exactly **600** primitive solutions survive.

Hence **no denominator residue class is excluded by these particular 2-adic and 5-adic conditions** for adjacent slopes. This is unlike the integer-indexed slopes of RQT-343; the change of primitive slope family matters.

Survival at modulo32 and modulo25 is not rational solvability, and these two computations both derive from **one authentic frozen source F4**. A rational point requires all local places and an exact global witness.

## Reproducibility
Run `python research/rqt345-adjacent-rational-slopes.py` with SymPy. Exact local execution confirmed the two denominator thresholds and all 114 primitive-residue counts (two differences × (32+25)). Full local artifact: `/mnt/data/rqt345_adjacent_slope.py`.

A handful of exploratory SymPy ternary-diophantine solver calls for first admissible denominators returned no witness; these calls are **not** treated as proof of anisotropy. A larger exploratory batch did not finish and is **not** used as evidence.

## RQT-346 next natural target
A rigorous local-global ternary isotropy test on selected rational slopes, including bad discriminant primes, or a four-variable rational quadric solver with an explicitly checked primitive integer vector. If the rational isotropic vector is constructed, clear denominators and certify `gcd(F4u)=1`; then apply the RQT-334 Bézout parity gate and downstream RQT-257 Wall-completion conditions. Keep all statuses OPEN until an exact witness is produced.

3×3×3 tensor and time-angle cubit are metadata and have no bearing on the mathematical proof.
