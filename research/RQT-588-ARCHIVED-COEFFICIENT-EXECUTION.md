# RQT-588 — Archived-Coefficient Execution

## Exact run and baseline
- Source archives: RQT-583 equation JSON (SHA256 `5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92`); RQT-584 certificate JSON (SHA256 `29f0eb2b4ef29d3194185ee45d72c58a793b41bd44993b0b6ad33bf3435cbe5f`), and RQT-586 results JSON.
- Both source fingerprints matched RQT-586's recorded reference hashes.
- Previous all-scale exclusions: 81 of 135 selected corridors (60%).
- Remaining 54 indices derived from the 80 archived RQT-583 equations after removing 12 RQT-584 and 14 RQT-586 exclusions.
- Tested exact quadratic-square residues for prime powers <= 4096 of primes 2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97.
- Bounded discriminant-square search: -2000 <= t <= 2000 for each of 54 corridors.

## Results
- **0 newly excluded families** from these prime-power gates.
- **0 integer square discriminants** in the finite t-window.
- **81 excluded, 54 unresolved** unchanged.
- Failure to find a square in the bounded window is not proof of all-scale exclusion.

## Reconstruction blocked by source mismatch
A Library file called `reduced_gram.json` was inspected, but contains a **5×5** matrix and SHA256 `e2de9ccd078db582a8e9...`; RQT-583 records a different **4×4** reduced Gram SHA256 `aa8607e3582dd979ee35a07782bb56eafc6c247a7edf6584531bb7cc9844473d`. Therefore:
- Recovered integer u: **not attempted**.
- Original 22D Wall replay: **not attempted**.
- Root 19: **OPEN**.

## Next natural bound — RQT-589
Recover the hash-matching RQT-575 4×4 reduced Gram and 22D embedding. If recovery succeeds, validate discriminant identity and exact coordinate reconstruction before any new search. Otherwise, derive and certify an equivalent Gram from archived data and identify the derivation as reconstruction, not an original archive.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
