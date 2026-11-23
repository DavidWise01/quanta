# RQT-609 — Regular/Singular Hensel Classification and Exact Next-Level Lifts

## Exact verified experiment
Inputs: RQT-608 53-family results (SHA256 `0a86b00b80c7add37edba135971ed0018cae1170685e5feadad8ef0914a15844`), RQT-591 reconstructed 4×4 Gram and RQT-583 archived equations.

For family ray r and offset o, form the exact binary norm polynomial:
`f(u,t) = q_F((u,r*t+o))+2`.
Its coordinate gradients are
`f_u=2a*u+b*t+e` and `f_t=b*u+2c*t+d` when `f=a*u²+b*u*t+c*t²+e*u+d*t+g`.

A mod-p root is **regular** if at least one gradient coordinate is nonzero mod p; otherwise it is **singular**.

## Base-prime classification (all root pairs, not just one witness)
- **p=2:** all **53 families** have **4 mod-2 roots, all 4 singular**, and 0 regular roots. Ordinary nonsingular Hensel assumptions do not apply.
- **p=7:** 29 families have 6 roots (all regular); 12 have 8 (all regular); 6 have 7 (all regular); 4 have 13 (12 regular, 1 singular); and **families 2 and 24** each have **1 root, singular-only**.
- Hence **51/53 families possess a regular mod-7 root**; **2/53** require exhaustive singular-branch retention.

## Next-power lift result
Using exact first-order lift congruence `f(u+i*m,t+j*m)/m ≡ f(u,t)/m + i*f_u + j*f_t (mod p)`, full branch retention was performed for all 53 families modulo `2^14=16384`. For each family, previous RQT-608 counts through 2^13 were independently matched. At 2^14, each family retains between **16,384 and 98,304** valid coordinate pairs.

For regular mod-7 families a valid regular seed was lifted deterministically to **7^6=117649**. For singular-only families 2 and 24, every branch was retained to that level; their exact counts across 7,49,343,2401,16807,117649 were **1,49,392,2744,19208,134456** each.

The 11 CRT component moduli are:
```
16384,81,125,117649,11,13,17,19,23,29,31
Combined M''' = 18639287143547406336000
```
All **53** combined CRT coordinate pairs were directly checked with the exact Gram norm `f(u,t)≡0 (mod M''')`.

The complete local machine-readable file `RQT-609-results.json` has SHA256 `c8ee91be96e29955d8505634deb26057c6506b8915dd1938d530fbe1e989a7b0`.

## Scope
- No *family-wide* obstruction at the tested prime powers.
- **82/135 selected families excluded (60.74%), 53 unresolved**. No change to this all-scale ledger.
- A modular root is not an exact integer norm−2 vector.
- Original 22D Wall replay **not performed**.
- Root 19 **OPEN**.

## Next natural bound — RQT-610
Study the singular-only p=7 families 2 and 24 with an exact branch-growth law and possible p-adic factorization; seek a structural invariant or demonstrate continued p-adic solvability. Preserve the full branch set and avoid promoting a finite level to a global existence theorem.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
