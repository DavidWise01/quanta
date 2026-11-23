# RQT-624 — Combined 2-Adic / Odd-Prime Exact Integer Seed Gates

## Verified experiment

Independently reopened exact RQT-623 mod-256 projection results, RQT-591 integer Gram and original RQT-583 Pell equations, verifying recorded SHA-256 ancestry. Reconstructed the full binary integer norm polynomial Q(u,t) for each of **27 unresolved canonical orbits**, covering **53 original selected family IDs**.

For every orbit:
1. Independently reproduce every admissible t mod 256 from a complete search over all u mod 256.
2. Enumerate all valid coordinate pairs modulo **7** and **31**, preserving their projected t sets.
3. For the two singular-only exceptional cases, use their exact translated reduced quadratic forms:
   - Family **2** at p=7: lift the coordinate norm gate to p³=343, and retain **4 t-classes modulo 49**, namely {13,20,27,34}.
   - Family **28** at p=31: lift the coordinate norm gate to p³=29791, and retain **16 t-classes modulo 961**, namely {105,136,167,198,322,384,415,446,477,570,694,787,818,849,880,942}.
4. Use integer CRT separately on u and t to form a concrete simultaneous representative. Verify **Q(u,t)=0 modulo the full combined coordinate modulus**.

## Exact highlights

**All 27/27 canonical orbits have explicit combined coordinate witnesses**. No new whole-family exclusion is found.

- Ordinary family coordinate modulus: 256×7×31 = **55,552**.
- Exceptional family 2 coordinate modulus: 256×343×31 = **2,722,048**. Necessary t wheel: **17,408 / 388,864** classes, using 256×49×31.
- Exceptional family 28 coordinate modulus: 256×7×29791 = **53,385,472**. Necessary t wheel: **8,192 / 1,722,112** classes, using 256×7×961. This retains ≈0.476% of parameter residues.
- Across the 27 projected t wheels, minimum and maximum densities are approximately **0.00475695** and **0.42842742**.

Do not confuse the *parameter wheel modulus* with the larger *full coordinate congruence modulus* in the exceptional cases. The t restriction is projected from a norm congruence at p³, not merely from testing modulo p².

## Artifacts and mathematical scope

- Full reproducible Python source: conversation artifact `rqt624.py` and repository path `research/rqt624-combined-crt.py`.
- Full exact 27-family JSON certificate: `RQT-624-results.json`, SHA256 `3af5fb6ec8a63b67babc42a4692a688c5a302ddf29bfaf15e56dc3a820cf3397`.
- Sources: RQT-623, RQT-591, RQT-583.

**No exact ordinary integer norm−2 seed has been constructed.** CRT-compatible residue classes are necessary conditions, not sufficient conditions for an integer solution. This is not a new all-scale family exclusion and no original 22D Wall replay has been performed.

Selected-family ledger remains **82/135 excluded at all scales (60.74%), 53 unresolved**, represented by 27 canonical sign-orbits; selected corridors are not the entire integer lattice. **Root 19 OPEN.**

## Next natural bound — RQT-625

Use the exact combined coordinate wheels to prioritize a bounded *global integer seed* search with independently checked discriminant squares and genuine norm Q=0 recovery. Store scope, rejected residues, inverse mirror maps and candidate coordinates; never promote a bounded nonfinding to global exclusion.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
