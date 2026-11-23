# RQT-625 — CRT-Guided Exact Integer Seed Recovery

## Executive result

Replayed the RQT-619 reconstructed integral binary norm coefficients and the RQT-624 combined integer-coordinate CRT gate certificate. Both input SHA-256 fingerprints were verified:

- RQT-619: `97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021`.
- RQT-624: `3af5fb6ec8a63b67babc42a4692a688c5a302ddf29bfaf15e56dc3a820cf3397`.

Each of the **27 canonical unresolved sign-orbits**, representing 53 original family IDs, was tested over the exact finite parameter window **−1,000,000 ≤ t ≤ +1,000,000**. This covers **54,000,027 distinct canonical-orbit/parameter pairs**. No candidate survives the complete modular gates; hence no integer norm−2 vector occurs in those selected finite windows.

## Method — exact necessary conditions

For each canonical family define

```
Q(u,t) = a u² + (b t + d)u + c t² + e t + f.
```

The six integer coefficients are obtained as twice the six archived RQT-619 `R=Q/2` coefficients. For integer u, the discriminant

```
Δ(t) = (b t + d)² − 4a(c t² + e t + f)
     = A t² + B t + C
```

must be a **nonnegative integer square**. The verifier applies the precise RQT-624 *coordinate projection* sets modulo 256, 7 and 31, with family 2's enhanced t-mod49 and family 28's enhanced t-mod961 restrictions. These are independently necessary conditions on every exact integer seed.

The remaining t values are then filtered by exact quadratic-square residue conditions modulo odd primes chosen in a fixed declared sequence. Each rejection is mathematically valid regardless of the scale of the integer t; the claim that **all tested t** are rejected is only valid over the explicitly scanned interval.

**Every one of the 27 windows becomes empty** by a prime no larger than 139. Across all jobs the certificate records **706 ordered filter stages**, including the original coordinate-projection gates. No discriminant-square candidate, integer u, or exact integer root is recovered.

Final prime stage distribution across the 27 jobs: 71 (1), 97 (6), 101 (2), 103 (7), 107 (5), 109 (3), 113 (1), 127 (1), 139 (1).

## Reproduction

- Executable script: `research/rqt625-integer-seed-search.py`.
- Input: exact RQT-619 and RQT-624 JSON results (SHA-256 above).
- Output: locally generated `RQT-625-results.json`, SHA-256:
`201bbc5dfde380016884c775ff1c390a69196303fce3a8199219de739c6ace69`.
- The full JSON records each of the 27 canonical IDs, original member IDs, discriminant coefficients, every modular filter's surviving candidate count, and the final surviving t/square-discriminant/integer-root sets.
- Arithmetic: Python integer operations, exact modular squares and `math.isqrt`; no floating-point approximations.

The RQT-619 and RQT-624 certificates descend from the same owned archive and are **not independent witness roots**. Mirrored families are transferred by the exact sign involution, not counted as 26 additional independently executed searches.

## Honest scope

This is an exact **finite search certificate**, not an all-integer theorem and not an exclusion of any of the 53 unresolved families at every scale. Selected family ledger remains **82/135 all-scale excluded (60.74%), 53 unresolved**, compressed to 27 canonical sign-orbits. The selected corridors are not a complete enumeration of the rank-four integer lattice. No original 22-dimensional Wall replay has been performed. **Root 19 remains OPEN.**

## RQT-626 natural bound

Rather than repeatedly increasing the finite interval, inspect the exact quadratic discriminant identities, possible factorization, local-to-global phenomena and generalized Pell orbit constraints for the 27 canonical families. Target a genuine all-scale obstruction or an exact integer root. Never infer either from an arbitrarily large bounded no-hit search.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
