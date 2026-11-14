# RQT-348 — Automated bad-prime obstruction sieve (authentic frozen lattice)

**Status:** exact executable sieve passed locally. 31 rational adjacent-slope ternary planes tested; **16 proven irrationally isotropic-free**, **15 inconclusive under this bounded sieve**. Original integral roots 18–21 OPEN.

## Primary source
The exact original F4 is from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`; original determinant `-8281492574115056973770683990411769007319047636247715225543944839911172` asserted. No bridge substitution. Source ancestry remains one frozen lattice.

## Complete executable range
The script enumerates lower-side `m=n-1, 188<=n<=204` (17 planes) and upper-side `m=n+1, 837<=n<=850` (14 planes), total 31. For each it derives the exact ternary Gram `G=T^T F4 T` with `x=(-m a,b,n a,c)`. Every odd prime `3<=p<20000` is tested.

## Certified local obstruction
For each p:
1. `p|det G`, `p²∤det G`;
2. leading binary minor `h=G00 G11-G01²` nonzero modulo p;
3. `-h` a quadratic **nonsquare** modulo p.

The form over F_p has rank two anisotropic quotient; its primitive isotropic residues must lie in its radical. Invert the leading 2×2 block to construct `v=(v0,v1,1)`, verify `Gv=0 mod p`, and verify `v^T Gv=0 mod p` but `v^T Gv != 0 mod p²`. Consequently no primitive residue lifts to an isotropic vector modulo p², so the whole rational ternary plane is anisotropic over Q. Every recorded certificate is independently recomputable from its prime and radical.

The leading-minor criterion is **sufficient only**, not a complete local-global solver. Missing a small prime is NOT evidence of rational isotropy.

## Results
The 16 excluded slopes and a prime certificate for each:

| slope | prime certificate |
|---|---:|
|189/190|17|
|190/191|13|
|191/192|5147|
|193/194|23|
|195/196|97|
|197/198|9127|
|198/199|137|
|202/203|23|
|203/204|13|
|838/837|83|
|842/841|23|
|843/842|773|
|846/845|179|
|847/846|17|
|848/847|17|
|850/849|13|

Some slopes have multiple independently valid arithmetic certificates. Fifteen of the 31 are INCONCLUSIVE in this scan, not roots. Notably `187/188`, `839/838` and `840/839` were already excluded in RQT-347 by larger primes outside the present <20000 window. Thus an inconclusive scan output must be reconciled against upstream evidence.

**Exact local execution**: `/mnt/data/rqt348_bad_prime_sieve.py` and JSON ledger `/mnt/data/rqt348_results.json`. Canonical GitHub source: `research/rqt348-automated-bad-prime-sieve.py`. This is a bounded automated obstruction scanner, not a general rational-point solver.

## Next natural advance RQT-349
Collect and reconcile known exclusion certificates into a single per-slope provenance ledger, then implement a certified rational isotropy solver for unresolved planes or the original full four-variable form. No exact original root18 exists in this output; all roots 18–21 remain OPEN. One true rational isotropic vector with divisibility one would activate the exact RQT-334 Bézout step. The 3x3x3 cubit, Josophene/Juliet and time-angle labels are indexing metadata, not mathematical proof.
