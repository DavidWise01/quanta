# RQT-597 — Exact squarefree Pell reduction

## Reproducible result
RQT-595 family **28** has `N=4A=358073442534422222735285217125379300`. Exact factorization:
```
N=100*d
d=3580734425344222227352852171253793
d=3*13*1693*54231366340197528698151546659
```
The largest factor was checked with a recursively verified Pratt/Lucas primality certificate (prime factors of p−1: 2, 603467, 19884661, 2259689841828967; top-level witness a=2). All factors are distinct primes, hence `d` is squarefree. The local downloadable JSON certificate and standard-library verifier reproduce the proof.

## Reduction and necessary coordinate gates
RQT-595: `X²−N Y²=K`, `X=2At+B`, with `K=B²−4AC`. Define `Z=10Y` to obtain
```
X² − d Z² = K
Z ≡ 0 (mod 10)
X ≡ B (mod 2A)
```
These last congruences are necessary to restore integer `Y` and `t`. A candidate must also make `Delta(t)=Y²` and `u=(-b(v) ± Y)/a` integral and satisfy `q_F(u,v)=-2`.

For an integral unit `x+z sqrt(d)` with `x²−d z²=1`, the multiplication action `(X,Z)→(xX+d zZ,zX+xZ)` preserves the generalized Pell norm, but preserving `Z ≡ 0 mod 10`, `X ≡ B mod 2A`, and `u` integrality must be checked.

## Status
- Exact squarefree factorization **PASS**, recursive primality certificate **PASS**, exact substitution **PASS**.
- Explicit nontrivial integral Pell unit **NOT FOUND**; generalized Pell seed **NOT FOUND**. No new selected-family exclusion.
- Selected corridor ledger stays **82/135 excluded (60.74%), 53 unresolved**; corridors do not exhaust the rank-four lattice.
- Original 22D Wall replay **NOT RUN**; Root19 **OPEN**.
- The reduced 4×4 Gram is rederived, not byte-identical to the missing RQT-575 archived file.

## RQT-598 — Integer unit and orbit stabilizer
Find a genuinely integral norm-one unit for the squarefree d (or prove a suitable exponent/congruence stabilizer), then certify integer `Z`, `t`, `u` through explicit modular and norm checks. Separate finite failures from all-scale proofs.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
