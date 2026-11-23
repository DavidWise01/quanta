# RQT-604 — Append-Only CRT Certificates & Direct Coordinate Gates

## Executed result

Replayed the exact RQT-603 per-family CRT ledger using the RQT-591 rederived 4×4 Gram matrix. Source RQT-603 SHA-256:
`5b368539719e209e47dacdd6b294546632af66d7c70f88d3cd834002ca4b25c8`.

**All 53** prior unresolved selected ray-offset families passed every replay assertion. The code recomputed each discriminant coefficient from the integer Gram (not copied from the prior ledger), independently recalculated allowed prime residues, and replayed **989 chronological prime-filter stages** over **−100000 ≤ t ≤ 100000**. Every per-stage survivor count matched RQT-603; every interval again ended at zero surviving discriminant-square candidates.

## Append-only certificate chain

A distinct JSON certificate was generated for each family. Each records its family index, ray, offset, exact quadratic discriminant coefficients, each rechecked prime gate and survivor count, direct norm-congruence results, and the SHA-256 hash of the previous family record. Canonical JSON serialization uses `sort_keys=True,separators=(',',':')`, and genesis is 64 zero hex characters.

**53 chained records.** Final hash:
```
e2bd1c5818a294ecd578af40791c81b3b96c432ee9276f0f404b7e4b054994a2
```

This is a **hash-linked append-only serialization convention**, not a claim of independent third-party witnesses, Byzantine agreement, or an immutable external storage service. The certificate content is reproducible from the archived RQT-603 results and Gram.

## Direct integer-coordinate gates

For each family, wrote the full integer norm condition as
`q(u,t)+2=a u²+b ut+c t²+d u+e t+f`. Exhaustively checked every residue pair `(u,t)` modulo:

`2,4,8,16,32,64,128,256,3,9,27,81,5,25,125,7,49,11,13,17,19,23,29,31`.

All 53 families had **at least one** valid pair at every tested modulus. The sum of counts across families and moduli was **95,248 admissible residue pairs** (counts may describe overlapping congruence classes and must not be interpreted as independent witnesses or global solutions).

This establishes **zero new all-scale exclusions**. Finite modular survival does not prove an integer norm−2 vector exists; the earlier finite CRT nonfinding does not prove a family is globally excluded.

## Status
- Exactly verified finite family-parameter coverage: **10,600,053**.
- Previously logged filter stages reproduced: **989/989**.
- Append-only family records: **53**, with deterministic final chain hash.
- Direct modular coordinate gates: **24 moduli × 53 families**, all locally satisfiable.
- Selected all-scale classification: **82/135 excluded (60.74%), 53 unresolved**.
- Original 22D Wall replay: **not performed**.
- Nineteenth root: **OPEN**.

## Next natural bound — RQT-605

Avoid enlarging finite intervals by default. Test **compatibility across combined prime-power coordinate moduli** (CRT lift for (u,t) in the same family) and prioritize exact all-scale obstructions or genuine integral norm−2 candidates. If a family remains locally soluble, document it as unresolved, not excluded.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`