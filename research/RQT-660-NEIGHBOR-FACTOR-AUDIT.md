# RQT-660 — Bounded Predecessor Neighbor-Factor Audit

## Executive summary

Replayed the exact RQT-659 partial Pocklington certificate, preserving its two unclassified large primality targets (indexes **23** and **28**) and all 130 previously certified recursive prime nodes. The new audit examined the unresolved predecessor cofactors **R** in `n−1 = F×R`, and certified exact factors of their **neighbors R−1 and R+1**, without promoting these side factors to factors of R itself.

**Result: ten prime-power entries certified by complete integer trial division and exact recomposition. Zero new divisors of R. Zero new target primality certificates.** The bounded direct trial search found no divisor of either R at most 100,000; this is a finite nonfinding, not proof of primality.

| Target | Neighbor | Certified prime powers | Remaining unfactored cofactor |
|---|---|---|---|
| 23 | R−1 | 2² | 76639725079445569518266295353665375160169403 |
| 23 | R+1 | 2 × 3⁵ × 7264393 | 86831705041770541568988559551178693 |
| 28 | R−1 | 2⁴ × 1451 | 14087159306870663327809253834175855786371 |
| 28 | R+1 | 2 × 3 × 3182573 × 402939577 | 42505122329380322301491991463 |

The six distinct primes appearing in these ten prime-power entries are **2, 3, 1451, 3182573, 7264393, 402939577** (six distinct primes; ten entries counting repetitions and exponents). Each listed prime is verified by complete trial division to its square root. The four remaining large neighboring cofactors are **not** certified prime.

## Global proof boundary

- Index 23: target `n=945427648580040545577333019482816067975849758493`, previously certified predecessor portion **F=3084**; `floor(sqrt(n))=972331038576903882216971`.
- Index 28: target `n=724069887353858191628011556527931108147407415720720843`, previously certified portion **F=2213959466**; `floor(sqrt(n))=850922962055824529286174779`.
- Both fail the simple `F>sqrt(n)` Pocklington threshold by a wide margin. Side-factor discoveries do not increase F unless they lead to a certified factor of R.
- Index 28's R has an exact base-2 Fermat compositeness witness. Index 23's R passes the base-2 Fermat test but remains primality-unproved.

The exact standard-library verifier `research/rqt660.py` reads the archived `RQT-659-results.json`, checks every prime by trial division, validates exact factor products, and records its local bounded trial test. Its independently generated full JSON certificate is `RQT-660-results.json`, SHA-256 **`b0719a64145785fabc47ee9bc77e5c57ba162cd45ddd8dbc0a37b1b262e6030a`**.

**Classification unchanged:** 82/135 selected families excluded at all scales (60.74%); 53 unresolved across 27 canonical orbits; no newly proved integer norm−2 root or all-scale exclusion. Original 22D Wall not replayed. **Root 19 OPEN.**

## Next natural bound — RQT-661

Rather than expanding blind factor searches, examine whether a certified **partial n+1 test** (Lucas or BLS) can use the newly factored neighbors, or target the large remaining R by a properly bounded ECM run. Accept a new target prime only after a complete independently checked certificate.

`{{i}} · .dlw`