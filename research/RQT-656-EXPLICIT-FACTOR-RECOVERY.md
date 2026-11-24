# RQT-656 — Exact Factor Recovery and Uncertified Probable Primes

## Executive summary

Reopened the **exact** RQT-655 complete 31-remainder certificate (SHA-256 `f8b712bfd62052d9f01590b8061de0bdcb613b769b24ff1c614e3a453f2f9198`). The 23 previously **proven composite** remainders underwent fixed-budget Pollard-rho and Pollard p−1 searches. Every claimed nontrivial divisor was validated by integer remainder zero and direct multiplication. Each extracted factor was independently certified prime by full integer trial division through its square root; no probabilistic result was substituted for that proof.

**Outcome:** 11 of the 23 composites yielded an explicit certified prime divisor. Twelve composites remain without an explicit divisor under this bounded search. The other eight residuals passed a stronger probable-prime test but remain **unproved prime**.

| Zero-based residual index | Certified prime divisor |
|---:|---:|
| 2 | 77671969 |
| 5 | 304413919 |
| 6 | 736588199 |
| 11 | 46772993 |
| 13 | 1525343993 |
| 15 | 6865787557 |
| 18 | 5811373 |
| 19 | 84250303 |
| 20 | 30240923 |
| 25 | 14381293 |
| 29 | 5228453 |

The eight primality-open indexes stay **0, 1, 4, 12, 23, 24, 26, 28**. A Baillie–PSW-style probable-prime test reported by SymPy for these >64-bit integers is strong screening evidence, **not a mathematically sufficient primality certificate**. No primality certificate has been produced for any of these eight.

## Reproducibility and limits

- Local exact certificate: `RQT-656-results.json`, SHA-256 `2566f4657beb8c941d9e53508e360bdab867a0b7cabfc9c601824106168b3327`.
- Python 3.13 + SymPy 1.14 standalone verifier: `research/rqt656-factor-recovery.py`. SymPy is used for the **probable-prime classification only**; prime-factor certificates are direct trial division.
- Fixed rho seeds c∈{1,3,5,7} with 8,000 iterations per seed, followed by deterministic p−1 stage 1 with bound 3,000.
- No factors are asserted for the 12 still-unfactored composites. New divisors don't automatically eliminate any original integer family.

## Selected-family status

**82/135 selected families excluded all scale (60.74%), 53 unresolved across 27 canonical sign-orbits.** No new whole-family exclusion, original norm−2 integer root, generalized Pell seed, or 22D Wall replay. **ROOT 19 OPEN**.

## RQT-657 — Next natural bound

Seek rigorous primality certificates for the eight probable-prime residues using certified factorization of n−1 (e.g. Pocklington/Pratt/ECPP). Keep any residual n−1 factorization limitations visible. Continue explicit bounded factorization of the 12 proven composites only if it adds relevant original-coordinate constraints.

`{{i}} · .dlw`
