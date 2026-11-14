# RQT-368 — Certified generation-3 GMA pruning, exact root18 test

**Status:** PASS for the complete three-generation ancestor census; nine-generation continuation is sampled only. Original root18 and roots19–21 remain **OPEN**.

## Original frozen arithmetic
This research uses the authentic stoicheion RQT-242 Gram F4, and the unimodular RQT-363 coordinate chart U. The exact target is `r.T F4 r=-2` with `r=U.T t`, `t=(a,b,c,d)`. The prior accepted parity classes are 0111,1001,1110; any exact candidate must also pass the original frozen reflection-prefix/factorization conditions, not an unsupported all-17 Wall-orthogonality assumption.

For `G=U F4 U.T` define `K_ij=G_i3 G_j3-G33 G_ij` for 0<=i,j<3. The exact half-discriminant of the integer d quadratic is `Delta=(a,b,c).T K (a,b,c)-2*G33`. A norm-minus-two integer root requires Delta a nonnegative integer square, plus integral d and exact norm verification.

## GMA search architecture
The user-selected structure `{{9x9}}^9` has 81 cells around a singlet per generation and nine generations, with axis-pair pattern (a,b), (b,c), (c,a) repeated three times. A completed address has 18 balanced base-nine digits, six in each of a,b,c. The complete address cube has `81^9=150094635296999121` possible full nodes.

**At generation three**, each coordinate has its two lowest balanced base-nine digits fixed; every future coordinate update is a multiple of `9²=81`. Thus all descendants have the *same exact discriminant modulo 81*. The 81 quadratic residues include exactly 31 distinct classes. If the current Delta residue is absent from those 31 classes, every descendant fails the integer-square prerequisite and the whole subtree can be deleted **with no risk of discarding an exact root**.

## Exhaustive exact generation-three certificate
Enumerate every possible triple `a,b,c∈[-40,40]` (exactly 81³=531441 generation-three ancestor nodes), each in bijection with an address of the first 3 generations.

| Result | Nodes |
|---|---:|
| Total ancestor states | 531441 |
| Proven impossible by Delta mod81 | **124659** |
| Surviving ancestor states | **406782** |

All 81 first-generation families are represented and have exactly 6561 ancestor states each; their survivor counts range from 4374 to 6075.

This is exhaustive **only at generation three**. It excludes all complete nine-generation descendants of each pruned ancestor. It does not imply a root fails in any of the surviving ancestor families.

## Full-depth stratified sample
One deterministic generation-4-through-9 continuation was tested for each of 150000 round-robin selected surviving generation-three ancestors. Thus each first-generation family receives 1851 or 1852 exact full-depth checks. Each completed triple is checked against a 12-modulus quadratic-residue sieve; all passing triples receive exact arbitrary-precision discriminants and, if any square, integer d, original-F4 norm, and parity checks.

| Full-depth sample outcome | Count |
|---|---:|
| Exact modular-square rejection | 149869 |
| Nonnegative exact discrimiminant fails (negative) | 125 |
| Nonnegative but nonsquare exact discriminant | 6 |
| Integral norm-minus-two vectors | **0** |
| Full addresses sampled | **150000** |

The sample does not exhaust `81^9`, and one sample per ancestor cannot prove the entire surviving ancestor subtree has no root.

## Verification and next target
The executable `research/rqt368-gma-certified-generation-pruning.py` reconstructs authentic F4, G and K, proves the descendant-mod81 property on 1000 deterministic samples, performs complete 81³ ancestor census and the 150000-address full-depth sample, and asserts the reported counts. The local executed program `/mnt/data/rqt368_generational_prune.py` produced `/mnt/data/rqt368_generational_results.json`.

**RQT-369 next:** deepen certified pruning at generation six modulo `9^4=6561` only for selected surviving generation-three ancestors; use an evidence-carrying scheduler with exact tested-parent identity, ancestor-residue witness and no duplicate counting. Prioritize a truly constructive norm-minus-two solver as soon as practical. Do not mistake finite modular evidence or sampled leaves for original root18. The nested cubit, singlet, Josophene/Juliet and time-angle labels are indexing, not proof.
