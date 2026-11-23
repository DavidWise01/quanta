# RQT-630 — Known Square-Factor Extraction and Pell Unit Recovery Gate

## Executive finding

Reopened RQT-626 and RQT-629 research records. Exact integer divisibility establishes **three nontrivial square-factor extractions** among the five original generalized Pell leading coefficients:

| Group | Original coefficient D | Extracted s | Reduced d = D/s² | Canonical orbits |
|---|---:|---:|---:|---:|
| 1 | 89518360633605555683821304281344825 | 5 | 3580734425344222227352852171253793 | 9 |
| 2 | 149561530769640628300862186866588569 | 7 | 3052276138155931189813514017685481 | 3 |
| 3 | 158134758925461363207454619257200752 | 4 | 9883422432841335200465913703575047 | 4 |
| 4 | 865181362726903603566834179921037649 | 1 | unchanged | 8 |
| 5 | 1957113882671124377864756294075131977 | 1 | unchanged | 3 |

These are **known exact square divisors**, not complete squarefree decompositions. Absence of an extracted factor in groups 4 or 5 does not prove their coefficients squarefree.

## Exact theorem and integrality

For D=s²d, the original norm-one equation is

`x²-Dy²=1`.

Substitute Y=sy. Then it becomes

`x²-dY²=1`.

Conversely, a solution of the reduced equation gives an **original integer unit if and only if** `Y≡0 mod s`. Replacing a coefficient without preserving this gate would introduce spurious original solutions.

If `U=x+Y sqrt(d)` is any reduced norm-one unit, then its image modulo s belongs to a finite multiplicative group, since its conjugate is an inverse. Thus some positive power `U^k` is congruent to 1 modulo s, and the square-root coefficient of that power is divisible by s. This is an **existence transfer conditional on having a reduced unit**, not an explicit construction of any numerical unit, nor a small regulator bound.

For generalized Pell targets `z²-Dy²=N`, the same substitution gives `z²-dY²=N`, with the necessary `Y≡0 mod s` recovery restriction; the pre-existing parameter congruence `z≡h (mod D)` and original integer coordinate check remain mandatory.

## Reproduction and scope

- Exact standalone verifier: `research/rqt630-square-factor-reduction.py`.
- Full machine-readable certificate: `RQT-630-results.json` SHA-256 `25d228f0176e366deca4fa3401b66789650ad2ef2c0dcb68d054c95a1de83ea6`.
- No complete factorization claim; no fundamental norm-one unit, generalized Pell seed, or integer norm−2 root constructed.

Selected-family ledger **82/135 excluded all-scale (60.74%), 53 unresolved**, organized as 27 canonical orbits. The original 22D Wall was not replayed. Root 19 **OPEN**.

## Next natural bound — RQT-631

Test the reduced coefficients' exact continued-fraction periods or seek certified norm-one units, while maintaining the `Y≡0 mod s` gate and all original parameter/integrality conditions. Only report a genuine unit when its full norm is directly checked.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`