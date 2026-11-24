# RQT-659 — Partial Pocklington Threshold Audit

## Executive result

Replayed the exact RQT-658 126-node recursive Lucas proof bundle and original RQT-656 numerical residues. The exact successor certificate adds **four rigorously certified predecessor primes** (487, 853, 3413, 2273059), for **130 independently validated prime nodes**. Its standard-library verifier passes each recursive Lucas n−1 proof and both target modular-witness families.

Neither target can be certified prime using the presently certified portion of its n−1 factorization. This is an **insufficient-certificate result**, not a proof of compositeness or an impossibility of primality.

| Index | Target n | Certified F dividing n−1 | Unresolved R=(n−1)/F | Pocklington F²>n? |
|---|---|---:|---|---|
| 23 | 945427648580040545577333019482816067975849758493 | 3084 = 2²·3·257 | 306558900317782278073065181414661500640677613 | No |
| 28 | 724069887353858191628011556527931108147407415720720843 | 2213959466 = 2·487·2273059 | 327047490468309319818419637014226667936389137 | No |

For **both targets**, base a=2 satisfies the conditional Lucas witnesses for each *certified* prime divisor q of F:

- a^(n−1) ≡ 1 (mod n)
- gcd(a^((n−1)/q)−1,n)=1

These checks are not sufficient without adequate factorization of n−1. The conventional elementary Pocklington threshold **F>sqrt(n)** fails decisively in both cases. The residual R for index 28 is **provably composite** because 2^(R−1) mod R is not 1; R for index 23 passes that base-two test but has no primality certificate. This does **not** classify target index 28 itself as composite.

## Source and proof reproducibility

- Exact source: `RQT-658-results.json` and `RQT-656-results.json` from the Quanta series.
- `rqt659-build.py` creates the deterministic JSON proof bundle. SymPy may propose factorizations for small predecessor primes, but does not supply final proof validity.
- `rqt659-verify.py` independently checks **every node** and the partial-factor gates using only Python standard-library arithmetic.
- Full exact proof certificate: `RQT-659-results.json` SHA-256 `da410c2fdd7319d6fde2fb247b329e52de3b675147db5c3a04a9076196019f0b`.

## Family status

**82/135 selected families excluded at all scales (60.74%); 53 unresolved across 27 canonical sign-orbits. Root 19 OPEN.** No new whole-family exclusion, generalized Pell seed, ordinary norm−2 integer root, or original 22D Wall replay.

## Next — RQT-660

Prioritize the two unresolved R factors through provably sound factorization or an alternate rigorous primality certificate. Preserve bounded search limits, original source ancestry, and exact global integer norm gates. Avoid confusing partial Lucas witnesses with completed prime proofs.

`{{i}} · .dlw`