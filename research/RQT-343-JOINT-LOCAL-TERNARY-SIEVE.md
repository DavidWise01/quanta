# RQT-343 — Joint 2-adic / 5-adic ternary slice exclusion

**Status: exact exhaustive primitive congruence calculations PASS; original rational isotropic witness and integral roots 18–21 OPEN.**

## Frozen provenance

Use the authentic original rank-four symmetric even Gram F4 of `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`; no synthetic bridge substitution. Parameterize non-coordinate three-dimensional slices by `x=(-k*a,b,a,c)`, i.e. `x0=-k*x2`. The restricted Gram is `T_k^T F4 T_k`. This family retains all four original coordinates whenever `k,a,b,c` are nonzero.

If a nonzero rational isotropic vector exists in such a slice, clearing denominators and dividing by the three-coordinate content yields a primitive integral vector `(a,b,c)` of exact norm zero. Reduction modulo every prime power must therefore have a solution with at least one coordinate not divisible by that prime.

## Exact exhaustive modular checks

The verifier enumerates all `32^3=32768` ternary residues for each of 32 classes k mod32, discarding residues that are simultaneously even, and tests the ternary norm modulo 32. The result is exactly `2048` primitive solutions in every allowed k class and **zero** in every excluded one. The allowed condition simplifies to

```text
k even OR k=5 mod8.
```

This strengthens the modulo16 exclusion `k=3 mod4` and additionally eliminates `k=1 mod8`. Extra tests modulo64 and modulo128 with exact Hensel branching found no additional k exclusions; the release theorem needs only modulo32.

Separately, reproduce the complete RQT-342 modulo25 census: all `25^3=15625` ternary residues for each of 25 classes k mod25, excluding triples all divisible by five. There are exactly `600` primitive solutions when `k != 1 mod5` and **zero** when `k=1 mod5`.

By CRT, combine the necessary k restrictions. Because the first depends only on k mod8 and the second only on k mod5, the complete selection has period 40. Exactly 20 of 40 classes survive:

```text
0, 2, 4, 5, 8, 10, 12, 13, 14, 18,
20, 22, 24, 28, 29, 30, 32, 34, 37, 38.
```

No nonzero rational isotropic vector can lie in any excluded slice. Exclusion applies to **infinitely many integer k**, but it does **not** prove that any surviving slice has a rational isotropic point, nor does it prove any global nonrepresentation in F4.

## Reproduction

`python research/rqt343-joint-2adic-5adic-sieve.py` with SymPy; all residue enumerations are performed with integer arithmetic and full assertions. Local execution also passed as `/mnt/data/rqt343_joint_local_sieve.py`.

## Next RQT-344

Try a certified rational-point solver on a surviving full-support slice (e.g. k=2,4,5,8) or a four-variable quadric algorithm. Do not infer rational solvability from the existence of local modulo32/25 residues; other primes or the real place can obstruct. Once a rational point is constructed, check exact F4 norm zero, primitive integral normalization, gcd(F4u)=1, and RQT-334 root parity/Wall compatibility before announcing root18.

## Evidence ancestry

The two modular tests are computationally independent local primes but both derived from the same frozen F4. Preserve their one-source ancestry. The 3×3×3 cubit, {{i}}, {{j}}, {{n}}, Josophene/Juliet and time-angle indices remain iteration metadata, not arithmetic proof substitutes.
