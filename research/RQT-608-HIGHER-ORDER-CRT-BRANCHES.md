# RQT-608 — Compatible Higher-Order CRT Lifts

## Source and exact execution

The RQT-607 53-family certificate, the RQT-591 rederived reduced 4×4 Gram, and the original RQT-583 Pell-equation JSON were loaded and verified against the recorded SHA-256 fingerprints:

- RQT-607: `f92b68e0bb3a6ae71a44f380ff1c8d40b7fae383d7c234a8050c0e35103464cf`
- Reconstructed Gram: `f842ede2ac064c20a18760381a8d411361e864caf1c8cdea4598dd7d7879b228`
- RQT-583 equations: `5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92`

The original RQT-607 simultaneous modulus was
`M'=1698185782028736000`, with local factors `512,81,125,343,11,13,17,19,23,29,31`.

The upgraded modulus is

```
M'' = 8192 × 81 × 125 × 16807 × 11 × 13 × 17 × 19 × 23 × 29 × 31
    = 784 × M'
    = 1331377653110529024000
```

Every local solution is computed by direct exact evaluation of the integer quadratic norm from the Gram and family ray-offset data. CRT coordinates are recombined independently, and `q_F(u, ray*t+offset)+2` is asserted to be divisible by M''.

## Preservation versus failure of individual branches

For **each of the 53 stored RQT-607 representatives**, the extension of its original `(u,t) mod 512` class through `2^13=8192`, and of its `(u,t) mod 343` class through `7^5=16807`, was checked by **retaining every valid pair at each refinement**.

- **29/53** particular stored 512-classes do **not** reach 8192; the others extend.
- **2/53** stored 343-classes do **not** reach 16807: families **2 and 24**.
- Despite those stored-class failures, *alternative* admissible branches exist for **all 53 families**.

To avoid classifying a greedy selection failure as a mathematical obstruction:

1. The 2-adic verifier starts with all pairs modulo 2 and retains **all valid lifts** at every power up to `2^13=8192`. At the last level it retains **8,192–49,152** pairs per family.
2. The 7-adic verifier first selects a nonsingular mod-7 solution when one exists and verifies successive Hensel lifts to `7^5=16807`.
3. Families **2 and 24** have only singular mod-7 solutions. For these, the verifier retains **all** mod-7 branches to the final level; their branch counts at `7,49,343,2401,16807` are **1,49,392,2744,19208**, respectively.

All 53 combined CRT representatives were checked against the exact Gram norm modulo M''.

## Interpretation

A class that does not lift at a higher prime power is excluded **as that fixed residue class only**, not as an entire Pell ray-offset family. The alternative-branch results show that the 53 families remain soluble at the tested moduli.

- New all-scale selected-family exclusions: **0**.
- Selected-family ledger unchanged: **82/135 excluded (60.74%), 53 unresolved**.
- These 135 corridors do not exhaust the entire rank-four lattice.
- Exact integer norm−2 vector: **not constructed**.
- Original 22D Wall replay: **not performed**.
- Root 19: **OPEN**.

## Next natural bound — RQT-609

Use exact branch statistics to classify regular and singular Hensel behavior and identify families with constrained lift growth. Analyze whether stronger odd-prime-power coordinate gates add any **family-wide** obstruction; require that **all** branches disappear at a modulus before calling a full-family exclusion. Avoid extrapolating finite modular survival to a global integer solution.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
