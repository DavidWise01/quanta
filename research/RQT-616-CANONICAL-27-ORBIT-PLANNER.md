# RQT-616 — Canonical 27-Orbit Test Planner and Exact Inverse Maps

## Executive summary
Reopened RQT-615 canonical mirror-orbit results and the exact RQT-583 Pell coefficient archive. The archived RQT-583 source SHA-256 was checked before execution. Created **27 deterministic research jobs** for **53 unresolved original family IDs**, consisting of **26 paired orbits** and **one self-mirror singleton (family 67)**. Every unresolved family ID belongs to exactly one job; zero duplicate assignments.

The assigned canonical representative is the smallest ID in each orbit. For the canonical family `i` and its partner `j`, exact integer maps `(u,t) -> (-u,-t)` and the inverse are recorded. The correspondence was independently rechecked against ray/offset data and the (A,B,C,D) Pell coefficient identities at signed parameter values, not merely trusted from the RQT-615 source.

Each job stores:
- canonical ID, partner ID(s), ray and offset;
- exact signed coordinate maps and their inverse;
- original exact Pell coefficients (A,B,C,D);
- quadratic-residue preflight sets for primes 7, 11 and 13 (necessary local screens, not roots);
- exact evidence ancestry;
- previous SHA-256 chain hash and own canonical-JSON record hash;
- task status UNRESOLVED.

## Reproducibility
Executable: `research/rqt616-canonical-planner.py`, using only the Python standard library.
Machine-readable full certificate: `RQT-616-results.json`, generated locally with SHA-256
`1c44716a8ac52154804276859b9b6fac3617b0d8697f2c4eba1f7d80228f1f1e`.

The 27-job append-sequence final hash is
```
6b365ada55f5e44881707b73b764814afbf6dc00e1d05affda4103ea2b229cd7
```

Hash chaining detects alteration and establishes within-file order; it does not establish independent evidence or external immutability.

## Mathematical scope
No new whole-family exclusion or exact integer norm−2 seed was found, since this is a planner and verification turn. The 55 selected families excluded before RQT-583 have not been symmetry-classified by this archive. The 135 selected corridors do not exhaust the full rank-four lattice.

Global selected-family ledger remains **82/135 all-scale excluded (60.74%), 53 unresolved** (represented by 27 archived canonical orbits). The original 22D Wall replay remains unperformed. Root 19 **OPEN**.

## Next natural bound — RQT-617
Execute a structurally new exact test on the 27 canonical representatives, prioritizing integer-coordinate congruences or generalized Pell orbit constraints. Use the recorded inverse maps to propagate a genuine theorem or candidate to the 26 mirrored partners. Record every source and test as append-only data, but never inflate evidence by counting mirror partners independently.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
