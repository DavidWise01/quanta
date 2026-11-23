# RQT-631 — Sharp Universal Recovery Exponents for Reduced Pell Units

Reopened the exact RQT-630 certificate, SHA256 `25d228f0176e366deca4fa3401b66789650ad2ef2c0dcb68d054c95a1de83ea6`. For the three known square-factor decompositions `D=s²d`, enumerate the full finite norm-one residue groups `G_s(d)={(x,Y) mod s : x²−dY²≡1 (mod s)}`. Multiplication is `(x,Y)(v,w)=(xv+dYw,xw+Yv)` modulo s. Every element is invertible by conjugation.

| Original group | s | d mod s | Group size | Element orders | **Minimal universal exponent E** | Order-E residue witness |
|---|---:|---:|---:|---|---:|---|
| 1 (9 orbits) | 5 | 3 | 6 | 1,2,3,6 | **6** | (3,1) |
| 2 (3 orbits) | 7 | 1 | 6 | 1,2,3,6 | **6** | (4,1) |
| 3 (4 orbits) | 4 | 3 | 8 | 1,2,4 | **4** | (0,1) |

**Theorem:** For any *actual reduced integer* norm-one unit `U=x+Y√d`, its E-th power satisfies `U^E=X+Y_E√d` with `X≡1, Y_E≡0 (mod s)`. Thus `y=Y_E/s` is integral and `X²−Dy²=1` exactly. The E values are **sharp for all residue elements**, because the table exhibits order-E elements. An actual unit may have smaller individual order. This is a *conditional algebraic transfer theorem*, not discovery of a nontrivial numerical unit. The remaining two groups have s=1, requiring no conversion.

The result preserves all 27 canonical orbit IDs. For any generalized Pell target `z²−Dy²=N`, the original parameter condition `z≡h (mod D)` and original quadratic coordinate u remain separate mandatory gates.

**Evidence:** exact Python-stdlib replay `research/rqt631-recovery-exponents.py`. Local complete machine-readable `RQT-631-results.json` SHA256 `a99d1aa8f6d44c148c8684cfe952794077c0f5d5ee6307c19d4aa16141c2ee7a`; includes all norm-one residue elements, their orders, and sharp witnesses. Source ancestry is the same owned corpus, not independent corroboration.

**Status:** no numerical nontrivial norm-one unit constructed, no generalized Pell seed, no integer norm−2 root, no new family exclusion. Selected ledger **82/135 excluded all-scale (60.74%), 53 unresolved** across 27 sign orbits. Original 22D Wall **NOT REPLAYED**. Root19 **OPEN**.

**RQT-632:** seek an actual verified nontrivial reduced norm-one unit, apply the certified exponent, check the original norm directly, and preserve the independent target and integer-coordinate gates.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
