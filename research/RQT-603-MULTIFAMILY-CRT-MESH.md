# RQT-603 — Multi-Family CRT Mesh & Exact Search Ledger

## Executed result

Reopened the exact archived RQT-583, RQT-584 and RQT-586 JSON files and the RQT-591 rederived reduced 4×4 Gram. SHA-256 fingerprints were checked before the run:

- RQT-583: `5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92`
- RQT-584: `29f0eb2b4ef29d3194185ee45d72c58a793b41bd44993b0b6ad33bf3435cbe5f`
- RQT-586: `45d129e80c7d6b19af2ba7a7e8e541f865e37646a2709efebbba87bb584a4859`
- RQT-591 rederived Gram: `f842ede2ac064c20a18760381a8d411361e864caf1c8cdea4598dd7d7879b228`

The 27 previously excluded archived Pell families (12 RQT-584, 14 RQT-586, and RQT-592 family 13) were removed from 80 archived Pell equations. **53 families remain**. This does not alter the other 55 exclusions already established before RQT-583.

For each family, exact Gram-derived discriminants were checked at signed scales `t∈{-19,-1,0,1,23}`. Then all **200,001** integer t values in **[-100000,100000]** were screened using a selected, effectiveness-ranked sequence from 50 odd primes (5 through 251). Exact quadratic-residue sets were calculated independently for each prime and family. A t was discarded only when `A*t*t+B*t+C` was a nonresidue modulo a tested prime. **All 53 family windows were completely eliminated**, with zero surviving parameters and zero perfect-square discriminants.

- Family-parameter combinations covered: **10,600,053**.
- Total prime-filter stages applied across families: **989** (14–22 per family).
- Family windows certified empty: **53/53**.
- New **all-scale** family exclusions: **0**.
- No 22D Wall replay performed.

The generated `RQT-603-results.json` contains each family index, ray, offset, chronological applied gates, admissible residues per prime, and surviving counts. The Python script `research/rqt603-multifamily-crt.py` deterministically replays the complete experiment from exact JSON inputs, with no random numbers or floating point operations.

## Mathematical scope
The result certifies a *finite* absence of integer square discriminants in the chosen 53 windows; it does **not** prove the 53 families have no solutions at larger integer t, nor that the selected 135 corridors exhaust the full rank-four lattice.

The selected-family all-scale classification remains **82/135 excluded (60.74%), 53 unresolved**. Root19 **OPEN**.

## Next bound — RQT-604
Construct a chunked append-only search ledger with checksum fingerprints and dynamic prime ranking. Prefer testing qualitatively new constraints (e.g. direct integer-coordinate congruences, generalized Pell orbits) over indefinitely expanding finite intervals. Checkpoint every chunk and keep the all-scale count separate from finite-window coverage.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`