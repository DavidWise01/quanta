# RQT-619 — Universal 2-Adic Normal Form and All-Exponent Solvability

## Executive result
Independently replayed the RQT-618 local branch certificate, reconstructed the exact quadratic norm from the rederived RQT-591 4×4 Gram, and reopened the original RQT-583 80-family Pell equations.

For all **27 unresolved canonical sign-orbits**, the integer quadratic form of the target norm equation, `Q(u,t)=q_F(u,ray*t+offset)+2`, has **every coefficient even**. Therefore
```text
Q(u,t) = 2 R(u,t),    R ∈ Z[u,t].
```
Direct enumeration of the four points (u,t) modulo 2 shows **each R has at least one regular zero** modulo 2 (a root where at least one partial derivative is odd).

Precisely:
- **17** canonical orbits have **two** regular roots of R mod 2.
- **10** canonical orbits have **one** regular root of R mod 2.
- **13** orbits additionally have a singular R-root mod 2; **14** do not. Singular branches need not be classified for the existence theorem.

## Exact all-exponent theorem
Let r be the number of regular roots of R mod 2, hence r=1 or r=2. Every regular root lifts by two-variable Hensel's lemma to compatible roots modulo every power 2^n, with **exactly two extensions per exponent** (one free coordinate digit). Therefore, for n>=1, the number of roots of R modulo 2^n arising from regular starting classes is `r · 2^(n-1)`.

For k>=2, the equation Q=0 modulo 2^k is equivalent to R=0 modulo 2^(k-1). Every solution (u,t) modulo 2^(k-1) has **four** coordinate lifts modulo 2^k, so the total satisfies
```
C_Q(k) >= r * 2^k   for all k >= 2.
C_Q(1) = 4.
```
This proves nonempty compatible **2-adic roots for every k>=1**, for all 27 canonical orbits, and hence their 53 original family IDs under the exact sign mirror map. The lower bound is not generally an exact count, because additional singular-root branches can contribute.

## Reproducible finite checks
Every regular mod-2 root was deterministically lifted to R=0 modulo **2^15**, with exact integer checks at each level. The original Q thus vanishes modulo **2^16** along each constructed jet. All 27 archived RQT-618 complete branch counts through 2^10 exceed the theorem's exact lower bound; no archived count contradicted the theorem.

A verified Python 3 standard-library source file and full JSON record preserve every reduced coefficient, regular and singular mod-2 root, Hensel jet, old counts and SHA-256 source fingerprint. Local output SHA-256:
`97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021`.

## Honesty gates
A 2-adic root is **not** an ordinary integer norm−2 solution. This theorem proves local 2-adic solvability, not the existence of any generalized Pell seed or an eighteenth/nineteenth root, and it gives **zero new full-family exclusions**.

Historical selected-family ledger: **82/135 excluded at all scales (60.74%), 53 unresolved** (organized as 27 archived canonical orbits). The 135 selected corridors do not exhaust the rank-four integer lattice. Original 22-dimensional Wall verification has not been performed. Root 19 **OPEN**.

## Next natural bound — RQT-620
Classify the singular roots of R modulo 2 for the 13 canonical orbits that retain them. Derive **exact additional branch-count contributions**, distinguishing eventual stable recurrences from transient growth. Do not infer a global integer solution from a p-adic theorem.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
