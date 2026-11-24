# RQT-650 — Singular Prime Lifting: Two Exceptional Cases Resolved

## Executive result

RQT-649 found 349 nonsingular prime–orbit cases and two singular-only cases among 351 tests (27 canonical orbits × 13 odd primes). This iteration resolves the two singular exceptions **over their respective p-adic integers**.

For an integer quadratic (G(u,t)=a u^2+b ut+c t^2+d u+e t+f), both singular cases have a unique root ((u_0,t_0)mod p), with
(p^2mid G(u_0,t_0)), (pmid G_u(u_0,t_0)), and (pmid G_t(u_0,t_0)). The exact substitution
[
u=u_0+pU,quad t=t_0+pT,quad
G(u_0+pU,t_0+pT)=p^2 H(U,T)
]
defines an integer quadratic (H). Every equation below is exact over integers, not merely a congruence.

| Canonical orbit | p | Unique singular root (u₀,t₀) mod p | Coefficients of H (mod p), in order (U²,UT,T²,U,T,1) | Nonsingular H roots mod p |
|---|---:|---|---|---:|
| 2 | 7 | (1,6) | (2,4,3,0,2,2) | **8** |
| 28 | 31 | (6,12) | (17,5,12,22,23,20) | **32** |

All 8/32 roots of H are nonsingular. Fix one, hold the other variable constant, and apply ordinary Hensel lifting: this constructs (U,Tinmathbb Z_p) with (H(U,T)=0), hence (G(u_0+pU,t_0+pT)=0) over (mathbb Z_p) **at all powers of p**.

The standalone Python 3 verifier checks the identity for multiple integer substitutions, exhaustively counts all H roots modulo p, and produces exact explicit witness lifts through (p^{14}) for the original G. It verifies 49 solutions modulo (7^2) and 961 modulo (31^2) over the singular base residue, plus counts (8cdot7^2=392) and (32cdot31^2=30,752) corresponding solutions modulo (p^3). Those finite counts corroborate, but do not substitute for, the nonsingular-H Hensel proof.

## Scope

Together with RQT-649, all **351 tested prime–orbit combinations** are now proven locally solvable in their respective (mathbb Z_p). This covers only the stated 13 odd primes, not every prime. RQT-648 separately established local 2-adic solvability for all 27 orbits.

**No ordinary integer norm−2 root** follows from a collection of local solutions. Nothing here proves a single integer pair satisfies the original equation globally; the original 22D Wall has not been replayed.

Exact source: RQT-619 JSON SHA-256 `97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021`. Exact local RQT-650 results SHA-256 `45714e90f7e7a8aee714976c33657df302145401e4fc138ed03b3a6a879803cd`. The source ancestry is one owned corpus, not independent witnesses.

Selected ledger unchanged: **82/135 excluded all scale (60.74%), 53 unresolved**, represented by 27 canonical sign-orbits; Root 19 **OPEN**.

## RQT-651 — Next natural bound

Audit additional bad primes from coefficient discriminants and determinants, rather than extending solved local lifts. Seek an actual global integral seed or a genuine obstruction; keep local and global proof statuses separate.

`{brace{n}[box[n](torroid(n))]} · {{i}} · .dlw`
