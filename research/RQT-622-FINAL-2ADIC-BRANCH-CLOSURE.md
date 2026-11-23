# RQT-622 — Fourth-Level Singular Branch Closure and Exact 2-Adic Count

## Executive result
Replayed the RQT-619, RQT-620 and RQT-621 exact JSON archives for canonical family **29** and its sign mirror **51**. The last unclassified singular root of the third-level quadratic `T` is `(u,t)=(1,0) mod 2`.

Let `T(u,t)=a u²+b ut+c t²+d u+e t+f`, with exact integer coefficients from RQT-621. Direct integer substitution establishes:
- `T(1,0) ≡ 2 (mod 4)`;
- both partial derivatives of T are even at `(1,0)`;
- hence **`T(1+2x,2y) ≡ 2 (mod 4)` for every integer x,y**.

This is a *global obstruction to that fixed 2-adic residue branch*, not to family 29 or 51 as a whole.

## Exact all-exponent 2-adic count
The exhaustive nested partition for this family is now complete:
- first reduced level R: **two regular** roots modulo 2 and **one singular** root;
- second reduced level S on the singular R class: **two regular** roots and **one singular** root;
- third reduced level T on the singular S class: **two regular** roots and **one singular** root;
- last singular T class: **blocked modulo 4**.

The three pairs of disjoint regular branches each have compatible Hensel lifts at every higher exponent, and their coordinate-class cardinalities contribute `2·2^k` each. No unexamined singular branch remains once k≥7. Thus for **every integer k≥7**:
```
C_29(k) = C_51(k) = 6·2^k,
```
where C counts coordinate pairs modulo 2^k solving `q_F(u,ray·t+offset)+2 ≡ 0`. This is an **exact count**, not a lower bound.

Archived complete counts for k=1..10 are `[4,12,32,80,192,448,768,1536,3072,6144]`; k=7..10 agree with the formula. Family 51 inherits exactly the same count under `(u,t)↦(-u,-t)`.

## Reproducibility
Standard library verifier: `research/rqt622-final-2adic-closure.py`. It checks exact input SHA-256, polynomial coefficients, gradients, the fixed-class obstruction, nested regular/singular structure and the first ten archived counts.
Source SHA-256:
- RQT-619 `97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021`
- RQT-620 `c23027155b581a22983649642141ba95d0a00c081ece6c8b1215443a2f97b7b3`
- RQT-621 `5d0a88735d0bdb0d7cc9ca3a51381475debb5e580cc8233e85a68711d3c1be92`

Exact locally generated results SHA-256: `7f498c067c1777e2a14c71ced242cb8a0e2c60acb1c074c85f33e6f505919401`.

## Scope
No new whole-family exclusion or integer norm−2 root. The full selected-family ledger remains **82/135 excluded all-scale (60.74%), 53 unresolved** across 27 canonical orbits. The selected corridors do not exhaust the full rank-four lattice; original 22D Wall replay remains unperformed. **Root 19 OPEN.**

## RQT-623 natural bound
Use the now-complete 2-adic branch structure to form a compact, *global integer-coordinate* search gate across the 27 canonical orbits, separate from local Hensel existence. Prioritize an exact integer norm−2 candidate or a valid all-scale obstruction; do not mistake a local branch count for a genuine integer root.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`