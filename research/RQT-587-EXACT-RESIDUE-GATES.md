# RQT-587 — Exact Residue Gates and Integer Recovery

## Baseline
RQT-586 records 81/135 selected ray-offset families excluded by all-scale odd-prime gates; 54 remain unresolved. This is not a classification of all integral vectors in the original 22-dimensional lattice.

## New verifier
The companion `rqt587.py` conversation artifact implements:
1. Exact residue analysis of quadratic discriminants `A*t*t+B*t+C` modulo prime powers up to 32768.
2. An all-scale exclusion **only if no integer residue t modulo m yields a quadratic residue**.
3. Finite search `-bound <= t <= bound`, testing integer square discriminants via `isqrt`.
4. Exact integer recovery `u=(-b ± sqrt(delta))/a`, with `a=F[0][0]`, `b=sum(F[0][j+1]*v[j])`, `v=ray*t+offset`.
5. Norm check `a*u*u+2*b*u+c == -2`, where `c=v^T F_sub v`.

The local regression tests confirm that a constant 3 fails the square gate modulo 4 and `t²` passes modulo 4. These are illustrative unit tests, not newly certified original-family exclusions.

## Verification status
- Repo baseline: RQT-586 commit `4d0a5b3f0e843cc717ef520ae8a35dc8f05640f2`.
- RQT-587 archive-input execution: **not yet run**; original RQT-583 equation JSON and RQT-575 reduced-Gram JSON are required.
- New exclusion count: **unknown**, preserve 81 excluded / 54 unresolved.
- Original 22D Wall replay: **not performed**.
- Nineteenth root: **OPEN**.

## Natural bound — RQT-588
Load archived exact JSON inputs; record per-family residue-obstruction certificates and bounded candidate list; validate the reduced norm and reconstruct the 22D Wall representative using the archived change-of-basis data.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
