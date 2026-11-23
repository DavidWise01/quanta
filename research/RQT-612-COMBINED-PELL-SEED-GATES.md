# RQT-612 — Combined Pell Seed Gates and Exact Integer Recovery

## Verified result

Two unresolved selected ray-offset families, indices **2** and **24**, were subjected to independent exact integer necessary-condition sieves over `−1,000,000 ≤ t ≤ 1,000,000`. This is **2,000,001** parameter values per family, or **4,000,002** family-parameter pairs.

The original RQT-583 Pell equations, rederived RQT-591 4×4 Gram, and RQT-611 16-branch Hensel record were reopened from the archive, and all source hashes recorded in the RQT-612 certificate.

Each family has the following necessary parameter classes, established by **modulo 343** norm solvability and projected to `t mod 49`:

- Family 2: `{13,20,27,34}`.
- Family 24: `{15,22,29,36}`.

**Important precision correction:** A direct norm test merely **modulo 49** allows all seven `t mod 49` classes reducing to the sole mod-7 t root. The sharper four-class condition follows by requiring the norm to vanish **modulo 343**; it is therefore genuinely necessary for an *exact integer zero*. Do not describe the four-class set as the full set of solutions modulo 49.

The resulting direct finite-window mesh started with **163,264** candidates for each family. It then checked exact discriminant-square necessity through a sequence of odd-prime residue gates (31, 29, 17, 19, 23, 5, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97). Each family had **one** parameter left after prime 89, then **zero** after prime 97.

Each discarded t has an explicit necessary modular obstruction; the entire window is therefore certified empty without floating-point approximations. No integer norm−2 seed was found in these two finite windows.

## Certificate

- Exact script: `research/rqt612-combined-seed-sieve.py`.
- Input SHA-256: RQT-611 `f0c2e02fe5e35847574c334de7c56d61a54f3e9d44dbb8cfcae4490145078e32`; RQT-591 `6dadba9f74f9f5625b4a1d87ab4b2d42d293851b54d40cd18c4b6e1aa91ecb67`; RQT-583 `5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92`.
- Full locally generated JSON results SHA-256: `5569e8da309af43c477b8799bc09ffb00c31f948511c540f980f092ebea1525c`.
- New all-scale exclusions: **zero**.

## Scope

The earlier classification remains **82/135 selected families excluded all-scale (60.74%), 53 unresolved**. The 135 selected ray-offset corridors do **not** exhaust the full rank-four lattice. This run supplies no generalized Pell seed, no complete lattice root, and no original 22-dimensional Wall replay. Root19 remains **OPEN**.

## Next natural bound — RQT-613

Derive a compact CRT progression for the two necessary mod-343 parameter gates and selected discriminant primes, including explicit residue-count and fingerprint certificates. Search a larger window without treating a finite nonfinding as a global obstruction. Alternatively, prioritize exact global Pell orbit restrictions rather than unbounded scanning.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
