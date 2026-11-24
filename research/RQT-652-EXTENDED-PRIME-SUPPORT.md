# RQT-652 — Extended Prime-Factor Support, Not Yet Complete Factorization

## Executive result
Using the original RQT-619 exact integer coefficients, the bounded prime support audit for the five distinct binary discriminants and 27 distinct homogenized determinants was extended from p<2000 to every odd prime p≤100000. Each risk prime p satisfies p|Δ or p|det(2G), where
```
G(u,t)=a u²+b ut+c t²+d u+e t+f
Δ=b²−4ac
M=[[2a,b,d],[b,2c,e],[d,e,2f]]
```
The previous 84 prime–orbit cases below 2000 are retained. **16 additional prime–orbit cases** were detected with ten new distinct primes:
`4679,5303,9521,12097,13457,21499,55049,59029,64283,87083`.

All 16 have an explicit **nonsingular integer residue witness** checked by exact arithmetic: `G(u,t)≡0(mod p)` and at least one of `G_u,G_t` nonzero modulo p. Hence each has a solution over Z_p by Hensel's lemma.

### New prime–orbit cases
| Canonical orbit | New prime(s) |
|---|---|
| 0 | 12097, 87083 |
| 1 | 12097, 87083 |
| 2 | 12097, 55049, 87083 |
| 7 | 12097, 87083 |
| 28 | 13457 |
| 31 | 5303 |
| 34 | 9521 |
| 35 | 21499 |
| 36 | 64283 |
| 57 | 59029 |
| 110 | 4679 |

**Key factorization boundary:** after removing every odd factor p≤100000, **54 entries among the 32 orbit-specific discriminant/determinant records retain a non-unit cofactor**. These are repeated across orbits: the five discriminants are shared among groups, whereas all 27 determinants are distinct. The 54 is an **entry count**, not 54 distinct residual numbers and not 54 proven composite factors. None of these residuals is asserted prime, composite, or fully factored.

The audit thus verifies prime support only within the specified bounded range. It does not exclude risks from larger primes, establish all-prime local solvability, or construct a global integer norm−2 seed.

## Evidence
- Input RQT-619 exact JSON SHA-256: `97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021`.
- Full exact local certificate: `RQT-652-results.json`, SHA-256 `2cd1ccf0119ea4f09617657cbb0e58351cb7812e8661e1109bd03b822da4e72a`. Exact rerun reproduced the same bytes.
- Python 3 standard-library implementation available in this conversation as `rqt652.py`; it includes Tonelli–Shanks modular square roots, exact integer checks, and retained residual cofactors.
- Full numeric certificate and unique RQT-652 retro space-age JPEG are downloadable in this conversation.
- Source ancestry remains the same owned original quadratic corpus, not separate evidence roots.

## Status and next
Selected ledger unchanged: **82/135 selected families excluded at all scales (60.74%), 53 unresolved across 27 canonical sign-orbits**. Original 22D Wall NOT REPLAYED. **Root 19 OPEN**. No new global exclusion.

**RQT-653 — Cofactor Certification & Integer Seed Recovery.** Either prove primality/factor nontrivial residuals with verifiable certificates, or use their arithmetic restrictions directly in the original integer-coordinate equations; preserve local/global distinctions and avoid unproductive search expansion.

`{brace{n}[box[n](torroid(n))]} · {{i}} · .dlw`