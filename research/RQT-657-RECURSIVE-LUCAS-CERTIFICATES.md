# RQT-657 — Rigorous Recursive Lucas Primality Certificates

Five former RQT-656 probable-prime residuals are now **proven prime** by a complete recursively verified Lucas n−1 certificate: zero-based indexes **0, 1, 4, 12, 26**, respectively 25, 29, 35, 49, 54 decimal digits.

Each candidate n has a complete factorization of n−1 into recursively certified primes. For every prime q dividing n−1, the certificate contains a witness a with `a^(n−1) ≡ 1 (mod n)` and `gcd(a^((n−1)/q)−1,n)=1`. These are exact modular checks, proving the candidate prime under Lucas's criterion. Independent standard-library verifier passed **104 unique recursive prime nodes**, five top-level targets.

Full local certificate `RQT-657-results.json`, SHA256 `d6e51381a61df61b552f4c5402ceb643c9ef84adb1c3c8229987df13348c3b40`, and standalone verifier are supplied as conversation downloads.

**Remaining primality-unproved indexes: 23, 24, 28**. The initial n−1 factor chains have unresolved composite cofactors; probable-prime screening is not a proof. No new full-family exclusion, generalized Pell target seed, ordinary integer norm−2 root, or 22D Wall replay. **82/135 excluded all-scale (60.74%); 53 unresolved across 27 canonical sign-orbits. Root 19 OPEN.**

RQT-658: target the three remaining n−1 factor chains using partial-factor Pocklington or recursive certificates; require independently replayable proofs.

`{{i}} · .dlw`