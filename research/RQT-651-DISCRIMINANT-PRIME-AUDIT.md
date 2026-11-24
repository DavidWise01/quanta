# RQT-651 — Discriminant Prime Audit & Integer Seed Constraints

## Exact result
The 27 canonical original integer quadratics were reopened from the RQT-619 JSON certificate (SHA-256 `97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021`).

For `G(u,t)=a*u²+b*u*t+c*t²+d*u+e*t+f`, potential bad-reduction primes were identified by exact divisibility into either:

- Binary quadratic discriminant `Δ=b²−4ac`;
- Homogenized symmetric `2G` matrix determinant `det([[2a,b,d],[b,2c,e],[d,e,2f]])`.

Testing **all odd primes strictly below 2,000**, this produces **84 prime–orbit risk cases across 20 distinct primes**. **55** were already part of the thirteen-prime RQT-649/650 audit; **29** are new cases spanning twelve distinct additional primes:

`53,59,71,113,131,271,293,449,491,769,929,1693`.

Every one of the 29 newly identified prime–orbit cases has an exact nonsingular modular root, verified by exhaustive finite-field search, and therefore has a solution over `Z_p` by Hensel's lemma. No singular exceptions were found among the 29.

### Scope
This is **a bounded prime-factor/divisibility screen**, NOT complete factorization of the coefficients or the determinant, and not a statement about primes `p≥2000`. It proves 29 additional local cases but **does not** prove local solvability at every prime or existence of one global integer norm−2 root. Existing RQT-650 resolved the two singular cases among the earlier 55.

The complete JSON certificate records all 27 coefficients' discriminants and determinants, all bad-prime divisibility flags below 2000, and every new root count, nonsingular count and exact modular witness. Reproduce with `research/rqt651-discriminant-primes.py` using RQT-619 data. Exact local result SHA-256: `bdbf19b65aff510708ba8ef0818a9d57981ea1d857f23d49948114a6431459b1`.

**Selected-family ledger:** 82/135 excluded all-scale (60.74%), 53 unresolved across 27 canonical sign-orbits. No additional whole-family exclusions; original 22D Wall NOT REPLAYED. **Root 19 OPEN**.

## Next — RQT-652
Seek *complete* factorization or a certified bound for discriminant/determinant prime supports, then audit any primes at or above 2000 that are genuine risk factors. After the local sieve, prioritize original integer-coordinate recovery and construction over another generic novelty search.

`{brace{n}[box[n](torroid(n))]} · {{i}} · .dlw`
