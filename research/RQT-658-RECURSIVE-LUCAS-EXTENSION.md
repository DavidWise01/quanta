# RQT-658 — Recursive Lucas Certificate Extension

## Executive result
The complete RQT-657 Lucas n−1 proof bundle has been extended to **cofactor index 24**:

`432877412205274760633664264474592820317371476039` — 48 decimal digits, now **rigorously proved prime**.

A fresh Python-standard-library verifier checked the complete recursive factorization of n−1 and modular Lucas witnesses for **126 distinct certified prime nodes**. Six of eight original probable-prime candidates are now proven: indexes **0, 1, 4, 12, 24, 26**.

For every certified node n>2, the proof supplies a complete factorization `n−1=∏q^e` into recursively proved primes, and for each q a modular witness a with `a^(n−1)=1 mod n` and `gcd(a^((n−1)/q)−1,n)=1`. The independent verifier uses only integer arithmetic and no probable-prime oracle.

## Open predecessor chains
- Index **23**: incomplete recursive chain; an intermediate predecessor contains composite factor `200151590961514908188303218776769`, not yet factored and certified.
- Index **28**: unresolved composite n−1 cofactor `327047490468309319818419637014226667936389137`; the known certified factor portion does not exceed sqrt(n), so the simple partial Pocklington threshold is not met.

Neither target is declared prime or composite.

## Reproduction
- Full certificate `RQT-658-results.json` available in this conversation, SHA-256: `f902bb282f26e3b9b254ffcab0231564008f6c9091baa6a53215f5bd98ca6cfb`.
- `research/rqt658-build.py` constructs the certificate (SymPy proposes factors).
- `research/rqt658-verify.py` independently verifies proof nodes using only Python standard-library arithmetic.
- GitHub includes the verifier, builder, report and fingerprint; the **full 55 KB certificate is a separate conversation download**, not yet stored in this repository.

## Classification and next
No new full-family exclusion, generalized Pell seed, ordinary norm−2 integer root, or original 22D Wall replay. Selected ledger **82/135 excluded all-scale (60.74%); 53 unresolved across 27 canonical sign-orbits; Root 19 OPEN**.

**RQT-659:** factor and certify the blocking predecessor components for indexes 23 and 28 or find a provably sufficient partial Pocklington factorization.

`{{i}} · .dlw`