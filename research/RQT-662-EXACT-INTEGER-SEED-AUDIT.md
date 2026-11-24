# RQT-662 — Bounded Exact Integer-Coordinate Recovery

## Executive result

Reopened the original RQT-619 exact six-coefficient quadratic records (SHA-256 `97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021`) for all 27 canonical unresolved sign-orbits, representing 53 original selected family IDs. Evaluated every integer parameter `t` from **−20,000 through 20,000 inclusive** for each orbit: **1,080,027 orbit–parameter combinations**.

For each `G(u,t)=r0*u²+r1*u*t+r2*t²+r3*u+r4*t+r5`, calculate

```
F(t)=(r1²−4*r0*r2)*t² + 2*(r1*r3−2*r0*r4)*t + (r3²−4*r0*r5).
```

An integer solution requires a nonnegative perfect-square `F(t)=y²` and an integral `u=(-r1*t-r3 ± y)/(2*r0)`. Both signs are tested, followed by **direct exact substitution into the original G** for any candidate. Necessary square-residue sieves `mod 64, 63, 65, 17, 19` accelerate rejection; no modular condition alone is treated as proof of integrality.

## Actual counts

- Parameter–orbit checks: **1,080,027**.
- Nonnegative discriminants: **1,078,223**.
- Passed all modular square-residue tests: **62,032**.
- Exact integer-square discriminants: **0**.
- Reconstructed integral-coordinate solutions: **0**.

A separate unfiltered integer-square scan for the smaller window `|t|<=100` reproduced zero squares, without using the modular filters.

**No all-scale exclusion follows**. This experiment only establishes nonexistence of integer seeds in the specified parameter window of the 27 selected charts. It does not bound solutions with `|t|>20,000`, the full rank-four lattice outside the selected corridors, or all algebraically possible transformations.

The archived global selected-family ledger remains **82/135 excluded at all scales (60.74%)**, **53 unresolved across 27 canonical orbits**, original 22D Wall **not replayed**, **Root 19 OPEN**. No new integer norm−2 root, family exclusion, or generalized Pell seed.

## Reproduction

`python research/rqt662.py RQT-619-results.json RQT-662-results.json 20000`

- Original RQT-619 exact input SHA256: `97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021`
- RQT-662 complete local JSON SHA256: `7b9b0b160819f061920a055c84e44785fe2ee21796747124c8dc387e25c1f21b`
- Python 3 standard library only, exact arbitrary-precision integer arithmetic.

## Next natural bound — RQT-663

Replace another brute-force expansion with a **residue-progressions and Diophantine approximation planner**: determine which parameter residue classes survive, derive exact bounds where possible, and prioritize a route to an actual global integer seed or a rigorous all-scale obstruction. Preserve the distinction between finite experiment and proof.

`{brace{n}[box[n](torroid(n))]} · {{i}} · .dlw`