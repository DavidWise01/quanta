# RQT-654 — Certified Small-Prime Extraction from 31 Coprime Cofactors

## Executive finding

Reopened the complete RQT-653 certificate, retaining its 31 **distinct pairwise-coprime odd cofactors** derived from 54 residual entries. Tested every possible prime up to **5,000,000** by a deterministic Eratosthenes sieve. Each reported factor is prime by complete sieve construction, divides its original cofactor exactly, and passes exact multiplicative recomposition.

**Result:** nine distinct certified prime factors occur in eight of the 31 cofactors. One cofactor contains two factors. **All 31 original cofactors still have unresolved remainders** after extraction: none has been completely factored.

| Zero-based cofactor index | Certified factor(s) |
|---:|---|
| 2 | 777871 |
| 5 | 1909651 × 2120863 |
| 9 | 2640767 |
| 17 | 220859 |
| 18 | 402881 |
| 20 | 2479457 |
| 23 | 153437 |
| 24 | 482093 |

The other 23 distinct cofactors yielded no certified prime factor in this bounded test. Larger residuals are **not asserted prime**; a successful bounded small-prime scan does not certify irreducibility, primality, or ordinary integer root existence.

## Reproduction and exact proof scope

The Python 3 standard-library verifier `research/rqt654-certified-cofactors.py` reads `RQT-653-results.json`, creates a complete prime sieve to 5,000,000, divides each of the 31 distinct odd cofactor values, and checks exact recomposition. For any remaining integer n whose square root is within the sieve range, it performs complete deterministic trial division and would certify n as prime if no factor remained. No remaining integer met that full-certification condition.

Full local certificate: `RQT-654-results.json`; SHA-256 `f96f757aeb861f7a0c117639c91c6653fb00b745227cf80eb36b6bb2cbe4eae8`.

The previous pairwise-coprime partition is preserved. These nine prime factors belong to separate original cofactor components, except for the two belonging to one component; they are not nine new all-scale obstructions or nine integer norm−2 solutions.

## Classification

Selected-family ledger **82/135 excluded at all scales (60.74%)**, **53 unresolved across 27 canonical orbits**. No new whole-family exclusion, no ordinary integer norm−2 root, no generalized Pell seed, and no original 22D Wall replay. **Root 19 OPEN.**

## Next natural bound — RQT-655

Apply explicit primality/factor certificates to the largest remaining residues using bounded algorithms and independent exact validation. Prioritize outcomes that can restrict original integer coordinates rather than optimizing factor counts alone.

`{brace{n}[box[n](torroid(n))]} · {{i}} · .dlw`
