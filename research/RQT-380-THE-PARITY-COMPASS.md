# RQT-380 — The First Real Key: The Parity Compass

**Date: 2026-11-14. Exact F4 arithmetic verified; 437,200,800 new parity-compatible triples tested; authentic roots18–21 remain OPEN.**

## The story and preserved architecture
The cubic GMA remains nine generations of 9×9×9 voxels (729 cells per generation), 27 spatial cores of 27 cells, centered on the `||||` singlet. RQT-377 built exact Wall-kernel rank descent 4→3→2→1, RQT-378 built the signed-cofactor completion, and RQT-379 proved the fourth root is automatically supplied if a valid three-root Wall flag exists. This chapter returns to the missing root18 and finds a **rigorous parity compass** that reduces its direct original-lattice search.

The JPG chapter `RQT-380-The-Parity-Compass.jpg` was generated and delivered as a conversation artifact, depicting three admissible gates before an unentered root18 portal. It is narrative, not a literal map of individual integer search points. The JPG has not been uploaded to GitHub; the executable research and ledger are committed here.

## Authentic rank-four data

Use frozen F4/H4 from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`, verified determinant `-8281492574115056973770683990411769007319047636247715225543944839911172`, H4 unimodularity, and H4+H4.T=-F4. The RQT-363 **unimodular** integer chart

```
U = [[ 224,  29,-224,-130],
     [-193, -25, 193, 112],
     [  40,   5, -40, -23],
     [-336, -43, 335, 195]]
det(U)=-1,
r=U.T*(a,b,c,d),   G=U F4 U.T.
```

The norm-minus-two condition is exactly `(a,b,c,d).T*G*(a,b,c,d)=-2`. Previous accepted first-root original-coordinate parities were **0111,1001,1110**.

## New exact parity theorem

Enumerate all 16 classes of `(a,b,c,d) mod2` and map them through the exact unimodular U.T. Exactly **three** classes land in the accepted original parities:

```text
chart t mod2 -> original r mod2
     0001    ->     0111
     0100    ->     1110
     0101    ->     1001
```

Therefore EVERY original norm-minus-two vector with one of the accepted first-root parities satisfies

```text
a ≡ 0 (mod2),   c ≡ 0 (mod2).
b even  => d odd,
b odd   => d can be even or odd.
```

This means only one quarter of all possible `(a,b,c)` coordinate triples can support a root18 in these admissible classes. The parity restriction is a consequence of exact original F4/U coordinates, not a learned heuristic. It must NOT be applied to roots19 or20 unless their accepted parity requirements have separately been established. A root satisfying this gate remains a **candidate**, not automatically root18 of the frozen factorization.

## Executed exact search: new shell 501–700

RQT-364 previously proved there are no norm-minus-two original-lattice vectors for **any** `a,b,c∈[-500,500]`, solving fourth coordinate d algebraically **without bounding d**.

RQT-380 uses the necessary parity restriction `a,c even` and exhaustively checks **every** additional triple with
```text
a,c ∈ [-700,700] ∩ 2Z,
b   ∈ [-700,700] ∩ Z,
max(|a|,|b|,|c|)>500.
```
The C++ scanner preserves the proven RQT-364 modular quadratic-residue prefilter. Every survivor is checked via the **exact arbitrary-precision integer half-discriminant**
```text
A=G33,
B=G03*a+G13*b+G23*c,
C=2+sum_{i,j<3}Gij*t_i*t_j,
Delta=B²-A*C.
```
An actual integer d requires Delta to be a nonnegative perfect square and `A | -B±sqrt(Delta)`. There are no false negatives: the modular filter only rejects nonsquare residues, and exact full integer square roots are used for the remaining triples.

Executed `g++ -O3 -std=c++17` scan:
```json
{"shell_inner":500,"radius":700,"tested":437200800,
 "after_modular_square_sieve":565796,
 "nonnegative":25818,"square_discriminants":0,"integer_roots":0}
```

Combining the **previous entire [-500,500] cube exclusion** with this complete necessary-parity shell exclusion gives the new exact finite bound:

> Any authentic root18 in the three accepted original parity classes has `max(|a|,|b|,|c|)>=701` in the fixed RQT-363 unimodular coordinates, irrespective of d.

This does NOT prove there is no root18 at larger integer coordinates, and does NOT prove anything global about other root parity classes. The 437.2M shell points are new relative to the ±500 census. They are not 437.2M newly found roots.

## Reproduction
```bash
g++ -O3 -std=c++17 research/rqt380-parity-compass-shell.cpp -o rqt380
./rqt380 700
python research/rqt380-verify-parity-compass.py
```

The independent SymPy parity verifier reconstructs original F4/H4/U and checks all 16 possible parity classes, the determinant and all three accepted-class mappings. Local executed artifacts include `/mnt/data/rqt380_parity_shell.cpp`, `/mnt/data/rqt380_shell_results.json`, `/mnt/data/rqt380_verify_parity.py`, and `/mnt/data/rqt380_parity_verification.json`.

## Next natural target RQT-381

Use these three exact parity-chart cosets to drive a **constructive** (not endlessly bounded) representation algorithm for `r.T F4 r=-2`, possibly exploiting the previously rationally isotropic planes 194/195 and 201/202 and their primitive isotropic-vector Bézout construction. Once r18 is a true original vector, apply the exact Wall-kernel reduction to r19 and r20, with r21 supplied automatically by the signed-cofactor theorem. Do not assert frozen 17-predecessor compatibility without verifying the actual product/order.

**Authentic roots18–21: OPEN.**
