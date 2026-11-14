# RQT-370 — All 27 GMA spatial cores instantiated, next certified cubic generation

**2026-11-14 — Executed exact arithmetic and committed executable cores. Root 18 is still OPEN.**

## 27 spatial cores, 729 microcells, 9 generations

Correct the earlier flattened interpretation: each generation is a volumetric `9×9×9` cube with 729 microcells, centered on singlet `{{i}}` inside the central box `||||`. Three depth slabs are **Rear, Center, Front**; each slab has a 3×3 matrix of named macrocores, and each macrocore has 3×3×3=27 microcells. Thus 3 depth slabs × 9 macrocores/slab = **27 cores**, exactly covering 729 microcells. Nine nested cubic generations have address capacity `729^9 = 58149737003040059690390169` without preallocating any such giant array.

Coordinates are balanced signed base nine `x,y,z ∈ {-4,...,4}`. Three 3-wide groups on each axis are low `{-4,-3,-2}`, center `{-1,0,1}`, high `{2,3,4}`. The central singlet at (0,0,0) has core **CCC**, and the rear upper-left anchor (-4,+4,-4) belongs to **RUL**. Spatial names are routing/index metadata rather than arithmetic constraints.

## Every core instantiated

```text
REAR (R)              CENTER (C)            FRONT (F)
RUL  RUC  RUR          CUL  CUC  CUR         FUL  FUC  FUR
RCL  RCC  RCR          CCL  CCC  CCR         FCL  FCC  FCR
RDL  RDC  RDR          CDL  CDC  CDR         FDL  FDC  FDR

CCC contains the spatial singlet {{i}} and ||||.
```

Each of these 27 cores has a concrete microcell enumerator, individual generation-2 survivor count, three exact parent witnesses, generation-3 pruning counts, and 400 separately sampled depth-nine continuations.

## Authentic original lattice, not a surrogate model

This project uses the original frozen RQT-242 F4 coefficients and the exact unimodular RQT-363 chart U. For `r=U.T*(a,b,c,d)`, the root condition is `r.T*F4*r=-2`. Eliminate d with the exact quadratic discriminant

```text
Delta(a,b,c) = (a,b,c).T * K * (a,b,c) - 2*G33,
K_ij=G_i3*G_j3-G33*G_ij,
G=U*F4*U.T.
```

A genuine integer root requires Delta≥0, Delta a perfect integer square, exact integral d, exact original-F4 norm, and accepted root parity (0111, 1001 or 1110). A norm -2 vector alone still needs authentic predecessor factorization/rank/order checks before being named root18.

## Certified hereditary pruning

After generation k, the first k base-nine digits on each of (a,b,c) are fixed. Every descendant agrees with the parent modulo 9^k, so their quadratic discriminants agree modulo 9^k. An integer square modulo 9^k, with 9^k=3^(2k), must have either zero residue or even 3-adic valuation with unit ≡1 modulo3. The executable implements precisely this exact test; it never rejects a possible perfect-square discriminant.

Generation two (all 729²=531441 parent addresses) was audited exhaustively:

- 124659 exact impossible parent subtrees.
- 406782 surviving parent subtrees.

Generation three selected **three distinct surviving generation-2 parents in each of 27 cores**, preferentially including valuation-zero/valuation-positive/zero-discriminant-mod81 representatives, then checked **all 729 children per selected parent**:

- 81 certified parent witnesses
- 59049 third-generation children tested (27×3×729)
- **8019 third-generation child subtrees proved impossible**
- 51030 third-generation child subtrees survived the necessary square-residue gate.

This is an exhaustive g3 child audit **only for the 81 selected g2 parents**; it is not an exhaustive audit of all g3 nodes.

A separate deterministic, seeded full-depth sample tested **400 paths per spatial core**, total **10800 paths** across the nine generations, with the full modular-square sieve, exact discriminant and exact original-F4 verification on survivors. It returned **zero exact norm-minus-two candidates**. The sampled leaf set is not exhaustive, and no global nonexistence result is claimed.

## Reproduction and exact source witness

Run `python research/rqt370-instantiate-27-cubic-cores.py` from the quanta repository. The executable emits a complete JSON per-core evidence ledger. The full locally executed source and output are `/mnt/data/rqt370_all_cores.py` and `/mnt/data/rqt370_all_cores_results.json`. The repository executable independently reconstructs original F4 and calculates the same modular results.

## Next natural boundary — RQT-371

Use the per-core ledger to implement an append-only, diodic witness-packet scheduler with three independent verification operations (exact discriminant, original norm and prefix-factorization verification) without counting derived checks as independent original-source ancestries. Consider constructive indefinite norm representation as a parallel algorithm rather than indefinitely scaling a sampled search. **Original root 18 and roots 19–21 remain OPEN.**
