# RQT-369 — Cubed-nine GMA, corrected from planar to volumetric addressing

**Status:** exact original-F4 verification PASS; Root 18 OPEN.

The earlier RQT-366–368 implementations interpreted the requested nine-generation geometry as a series of 9×9 planar boards. The intended design is **9×9×9 around the central singlet / box ||||**.

## Geometry

Every generation is one 9³ cube: **729 cells** indexed by balanced signed coordinates (x,y,z) in {-4,-3,...,4}³. The central singlet is (0,0,0), identified with `||||`. For spatial semantics, partition each axis into 3 adjacent regions of 3 cells: low (-4,-3,-2), center (-1,0,1), high (2,3,4). The resulting **27 named 3×3×3 anchor regions** each contain 27 actual lattice addresses. For the depth axis, three 9-cell 3×3 anchor slabs are Rear / Center / Front, matching RUL, RC, RLL; CT, center, CB; FUR, FC, FLL and their neighbors. The 27 macro anchors are not a claim that the 729 microscopic addresses reduce to only 27 points.

Each of nine successive generations contributes one independent signed base-nine digit to **each of the three search coordinates**. Therefore all 9 generations encode 27 base-nine digits and `729^9 = 9^27 = 58149737003040059690390169` distinct full addresses. The mapping is bijective onto each coordinate range `[-(9^9-1)/2,(9^9-1)/2]`. Singlet per-generation digit is zero; it is not removed.

## Exact frozen mathematics

Original frozen authentic F4, from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`. The exact unimodular RQT-363 chart U gives `r=U.T*t`; the fourth coordinate of `t=(a,b,c,d)` is solved by integer quadratic discriminant.

Define `G=U F4 U.T`, `K_ij=G_i3 G_j3-G33 G_ij`. The exact necessary perfect-square test is `Delta(a,b,c)=(a,b,c).T K (a,b,c)-2G33`. For an exact norm -2 root, Delta must be a nonnegative perfect square, and `d=(-B +/- sqrt(Delta))/G33` must be integral; the original norm and parity must then be verified directly.

After **two** cubed-nine generations, the lower two base-nine digits of *all three* search coordinates have been assigned; every descendant preserves `Delta mod81`. The complete 729² = 531441 ancestor audit therefore correctly assigns
- 124659 globally impossible ancestor branches (nonsquare residue mod81)
- 406782 surviving ancestor branches (not yet roots).

These numbers coincide with RQT-368's 81³ census because both parameterize the same 81×81×81 low-digit cube; however **the correct generation structure is two volumetric generations, not three planar generations**.

## Executed cubic search

Run `python research/rqt369-cubed-nine-gma.py`. It verifies exact balanced indexing 0..728, the 729^9 address count, two-generation pruning counts, and runs 10000 deterministic nonduplicating full-depth probes. The local executed copy `/mnt/data/rqt369_cubic_gma.py` produced `/mnt/data/rqt369_cubic_results.json`:

```json
{"status":"PASS","two_generation_nodes":531441,
 "pruned":124659,"surviving_nodes":406782,
 "full_depth_sample":10000,"first_generation_coverage":729,
 "sample_counts":{"modular":9990,"negative":10},
 "candidates":[],"root18":"OPEN"}
```

The sample is **not exhaustive** over 729^9. Previous RQT-366–368 root-negative scans were also incomplete and should not be misinterpreted as a global exclusion. The new spatial indexing changes the scheduler, not the quadratic proof.

## Next RQT-370

Use the 27 macro-region spatial semantics for hierarchical witness routing, with 729 microcells per generation. Deepen safe modular pruning at later volumetric generations: after four generations, all descendants agree mod9^4 = 6561 on three free coordinates. Preserve ancestry and exact tested-address ranges. A true root 18 needs the original F4 norm -2, accepted parity, and the frozen factorization/order constraints; original roots 18–21 remain OPEN.

The central `||||` is the singlet box; cubic GMA is a search-addressing discipline, not itself a proof of root existence.
