# RQT-620 — Second-Level Singular 2-Adic Geometry

## Exact result
Reopened RQT-619's 27-orbit normal form certificate (SHA-256 `97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021`). Exactly **13** of its 27 canonical orbits have a singular root of the reduced polynomial `R=Q/2` modulo 2.

For every such singular root `(u0,t0)`, the source integer coefficients establish `R(u0,t0) ≡ 0 (mod 4)` and both gradient components are even. Thus substitution gives the **exact integral identity**
```
R(u0+2x,t0+2y) = 4S(x,y),
Q(u0+2x,t0+2y) = 8S(x,y).
```
The 13 reduced S forms each have at least one regular root modulo 2:
- **7 cases** have **one** regular root.
- **6 cases** have **two** regular roots.
- The latter **6** also retain a singular S-root, requiring further classification.

Each regular root of S lifts compatibly through all 2-adic powers by the derivative form of Hensel's lemma. Their contributions are distinct from those of the original regular R classes. If `r_R=2` is the count of R-regular roots mod 2 and `r_S∈{1,2}` the count of S-regular roots, the number `C_Q(k)` of coordinate pairs modulo 2^k satisfying `Q≡0` obeys for **every k>=4**:
```
C_Q(k) >= (r_R + r_S) * 2^k.
```
Thus 7 cases have the certified lower bound `3·2^k` and 6 cases `4·2^k`. These are **lower bounds**, not exact counts; deeper singular branches can contribute additional solutions.

## Reproducibility
All 13 translated identities were checked with signed integer substitutions. Every one of the 20 S-regular roots was lifted to `S=0 (mod 2^13)` and independently verified in the original `R` congruence. The inequalities were checked against archived RQT-619 exact enumeration through `2^10`.

- Executable local verifier: `rqt620.py`
- Complete JSON certificate: `RQT-620-results.json`
- Complete JSON SHA-256: `c23027155b581a22983649642141ba95d0a00c081ece6c8b1215443a2f97b7b3`

## Limits
This is an all-exponent **local 2-adic** theorem, not an ordinary integer norm−2 root and not a global all-scale exclusion. Selected-family ledger stays **82/135 excluded (60.74%), 53 unresolved**, compressed into 27 canonical cases. Original 22D Wall replay not performed. Root 19 **OPEN**.

## Next natural bound — RQT-621
Classify the 6 remaining singular S branches with another exact translated normal form and account for their all-exponent contributions. Stop when the branches become regular or are proved obstructed; preserve their individual ancestry without implying independent witnesses.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
