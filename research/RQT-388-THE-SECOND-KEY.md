# RQT-388 — The Second Key: exact rank-three integral search preparation

**2026-11-15 | New exact unimodular reduction PASS | Root 19 not found.**

## Why the second key is different

RQT-386 recovered an explicit original frozen-F4 integer norm-(-2) reflection, and RQT-387 proved it satisfies the prescribed first-stage rank/order reduction of the authentic residual `D4=I+H4^{-1}F4`. This does **not** yet finish the 21-reflection word; the remaining three roots must be built in the correct one-sided Wall order.

RQT-388 takes the first genuine successor problem:

```text
r19.T F4 r19 = -2
r19.T H4 r18 = 0.
```

The saturated integer solution space of the linear equation is rank three. Write its basis as the columns of `B∈Z^(4×3)`; then every possible integral successor is **exactly** `r19=B*z`, `z∈Z³`, with the ternary quadratic condition `z.T (B.T F4 B) z=-2`.

The prior RQT-386 conditional-kernel archive `RQT-386-Root19-Conditional-Kernel.json` was used as the original data witness. It had maximum basis-coordinate bit length **3340**; the original restricted Gram had huge coefficients.

## Exact, rational-free LLL basis reduction

A new completely exact LLL implementation works with Python `fractions.Fraction` and uses an *integer-only nearest-integer operation*, avoiding SymPy's machine-floating conversion failures on thousands-of-bit Gram-Schmidt fractions. It maintains the integral transformation `U∈GL(3,Z)` through every size-reduction and swap:

```text
L = U * B.T
Bnew = L.T = B * U.T
Qnew = Bnew.T F4 Bnew = U * Qold * U.T
det(U) = -1
```

Thus the new basis spans **exactly the same saturated integer Wall kernel**; no coordinates are rounded, no candidate vectors are lost or gained. All identities and the original one-sided Wall constraint are asserted directly against original F4/H4.

### Executed structural certificate

| Verification | Exact outcome |
|---|---:|
| Saturated kernel rank | 3 |
| LLL iterations | **855** |
| Unimodular basis transform determinant | **−1** |
| Largest old basis coordinate | **3340 bits** |
| Largest new basis coordinate | **644 bits** |
| Reduced ternary Gram determinant bit length | **3515 bits** |
| Reduced ternary signature | **(1 positive, 2 negative)** |
| Original F4/H4 and Wall equation | **PASS** |

The restricted ternary quadratic is still indefinite, so reduction does not turn the next root problem into a trivial shortest-vector calculation. This is a large and exact basis simplification, not the discovery of root 19.

## Exact modular and finite coefficient checks

The published reproducer enumerates root candidates in the *new reduced basis*, testing all nonzero integer triples in `[-30,30]^3` (the user-chosen GMA generational cube remains a separate 9×9×9 visual/search addressing structure). It applies the **complete norm equation modulo** `8,9,5,7,11,13,17,19,23,29,31` before exact integer norm verification. This rejects a triple only when its reduced Gram cannot possibly have norm −2.

```text
Total nonzero coefficient triples : 226,980
Rejected by exact modular norm:   226,980
Surviving all listed moduli:               0
Exact norm-minus-two successors:           0
```

This is a finite coefficient-box exclusion in the newly reduced basis. It **does not** exclude root 19 outside the box and does not establish global nonexistence. Small modular admissibility classes exist:

```text
Modulus 8:   192 / 512 root-compatible triples
Modulus 9:   162 / 729
Modulus 5:    20 / 125
Modulus 7:    42 / 343
```

The last figures are residue-class counts for separate moduli, not simultaneously realizable exact integer roots. The conjunction of many moduli can reject all small triples even when every modulus individually admits solutions.

## Self-contained Git reproduction

Primary executable:
```bash
python research/rqt388-exact-second-key.py --bound 30 --out RQT-388-kernel.json
```

It automatically:
1. Executes the committed RQT-386 exact null-to-root constructor and parses its authentic full integer certificate;
2. Loads the committed RQT-377 saturated integral kernel constructor;
3. Reconstructs the original 4×3 rank-three basis;
4. Performs the exact rational-free LLL with a tracked determinant-±1 transformation;
5. Checks original Wall annihilation, Gram identities, signature, residue classes and all finite search tests;
6. Saves the complete large integer reduced basis, transformation and Gram in machine-readable JSON.

The independently executed local algorithm `/mnt/data/rqt388_exact_kernel_reducer.py`, seeded with the archived RQT-386 conditional kernel JSON, produced `/mnt/data/RQT-388-root19-kernel-results.json` with the structural and search results above. These are the actual verified counts; the GitHub version reconstructs its input directly from its RQT-386/RQT-377 code dependencies instead of requiring an unattached conversation JSON file.

## Image and provenance

The new chapter image, **RQT-388-The-Second-Key.jpg**, illustrates the 27 cubic 3×3×3 spatial macrocores in the `{{9×9×9}}^9` GMA around central `||||`, with root18's first-stage gate open and root19's much smaller integral kernel now under construction. It depicts exact structural milestones but is conceptual scientific art, not a literal coordinate plot. The JPG is delivered as a conversation artifact; this executable and ledger are committed to GitHub.

This calculation remains within the same frozen stoicheion F4 source ancestry. Separate code paths are separate computational checks, not independent primary-source lineages.

## RQT-389 natural target

Now that the exact rank-three successor search basis has shrunk from 3340 to 644 bits, attempt an **unbounded constructive ternary norm−2 representation** rather than merely widening the coefficient box. Use exact local-global arithmetic (p-adic constraints, ternary conic norm representations or a certified indefinite ternary solver). Promote a vector only after checking `r19.T F4 r19=-2` and `r19.T H4 r18=0` in original coordinates. Then descend to rank two for root20, and use RQT-379's forced fourth root21 construction.

**Root18: first-stage accepted; root19: OPEN; root20: OPEN; root21: conditional. Full 21-word: OPEN.**
