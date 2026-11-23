# RQT-618 — Singular Prime-31 Geometry and 2-Adic Branch Retention

## Executed, exact result
Reopened RQT-617 source certificate, RQT-591 rederived 4×4 integer Gram, and the RQT-583 original 80-family Pell archive. Python 3 integer-only verifier `research/rqt618-singular-geometry.py` independently derived every binary norm coefficient from Gram and ray/offset inputs.

### Prime-31 exact theorem: canonical family 28
The family-28 quadratic `Q(u,t)=q_F(u,ray·t+offset)+2` has **exactly one root (u,t)=(6,12) mod 31**, singular in both coordinate derivatives. Its value at that representative is divisible by 31² and both derivatives are divisible by 31. Substituting
```
u = 6 + 31x
t = 12 + 31y
Q(6+31x,12+31y) = 31² P(x,y),   P ∈ Z[x,y]
P(x,y) mod 31 =
  3x² + 10xy + 24y² + 13x + 15y + 9
```
yields a reduced equation with **32 distinct roots modulo 31; all are regular** (nonzero gradient). By ordinary two-coordinate Hensel lifting, each reduced regular root has exactly 31 continuations per next exponent. Accounting for the 31² free final coordinate digits in the transformation gives the exact count of original norm congruence pairs modulo 31^k:
```
C(1) = 1
C(2) = 31² = 961
C(k) = 32 × 31^(k-1)  for every k >= 3.
```
This is an **all-exponent theorem**, not an inference from finite counts. Additionally, all 32 reduced branches were explicitly continued by deterministic derivative-based lifts to P=0 modulo 31^8, yielding 32 independently verified original-norm congruences modulo 31^10.

### All 27 canonical 2-adic cases
All 27 RQT-617 canonical unresolved orbits have only **singular** roots modulo 2. Unlike a greedy single-witness test, this verifier retains *all* valid coordinate branches through moduli 2,4,...,1024, and proves by complete enumeration that **all 27 still have valid pairs modulo 1024**. At 1024, branch counts range from **1,024 to 6,144**. This is finite verified modular survival; it does not by itself establish an all-exponent 2-adic law.

### Exact provenance
- Original RQT-583 SHA-256 `5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92`.
- Original RQT-617 and RQT-591 sources checked against RQT-617 recorded ancestry.
- Local complete `RQT-618-results.json` SHA-256: `33503798dbec82617dee32cca7a5f76cbb51f11090a8736c09c9e55b57ef423c`.
- Local complete verifier: `rqt618.py`; GitHub reproducible verifier: `research/rqt618-singular-geometry.py`.

## Interpretation
Prime-31 singularity for family 28 resolves into **32 regular reduced branches**, so it is not a local obstruction. All 27 canonical orbits survive the tested 2-adic powers. **No new full-family exclusion**, no exact integer norm−2 vector, and no original 22D Wall replay. Ledger remains **82/135 excluded (60.74%), 53 unresolved**, represented by 27 canonical orbits. Selected corridors are not the full lattice. Root 19 **OPEN**.

## Next natural bound — RQT-619
Seek an exact *all-exponent* explanation of the universal mod-2 singularity (e.g. coordinate translations and 2-adic normal forms), with explicit complete branch retention, before moving back to global Pell seed or original 22D Wall replay. Preserve the local/global distinction.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
