# RQT-607 — Alternate CRT Representatives & Liftability

## Exact verification — PASS

Input ancestry: RQT-604 family JSON records, RQT-605 simultaneous CRT witnesses, RQT-606 one-step lift outcomes, and the RQT-591 rederived 4×4 Gram. Verified source SHA-256 identities and independently recomputed the entire 53-link RQT-604 canonical record hash chain (tip `e2bd1c5818a294ecd578af40791c81b3b96c432ee9276f0f404b7e4b054994a2`).

In RQT-606, **26 stored CRT representatives could not lift to 2M**, and **two stored representatives (families 2 and 24) could not lift to 7M**. A single nonliftable representative does not exclude its family.

For each of the 53 families, the new verifier rechecked the prior representative modulo `M=121298984430624000`, then:

1. If its local 2-adic class lifted, retained that class; otherwise exhaustively found a different valid pair `(u,t) mod 256` admitting a lift modulo **512**.
2. Performed the corresponding repair modulo **49**, lifting to **343**, for nonliftable 7-adic classes.
3. Preserved valid pairs for the nine remaining pairwise coprime moduli `81,125,11,13,17,19,23,29,31`.
4. Reconstructed a simultaneous coordinate pair with CRT and directly evaluated the rederived integer Gram norm.

The new modulus is
```
M' = 512 × 81 × 125 × 343 × 11 × 13 × 17 × 19 × 23 × 29 × 31
   = 14M
   = 1698185782028736000
```
All **53/53 families** have explicit modular coordinates satisfying `q_F(u, ray*t+offset)+2 ≡ 0 (mod M')`. All **26/26 failed 2M classes** and **2/2 failed 7M classes** were repaired by selecting alternative local residue classes.

## What is (and is not) excluded

The RQT-606 failures concerned *particular stored residue representatives*. All 28 stored-class failures were resolved. This is a witness-selection result, **not** an exact integer norm−2 solution, not a global Pell seed, and not a new all-scale exclusion. The CRT coordinates generally represent huge integers with `q_F+2` divisible by M' but not necessarily zero.

All-scale selected-family ledger stays **82/135 excluded (60.74%)**, **53 unresolved**. Selected ray-offset corridors do not exhaust the rank-four lattice. Original 22-dimensional Wall replay **not performed**. Root 19 **OPEN**.

Reproducible local artifacts: `rqt607.py` and `RQT-607-results.json` (result SHA256 `f92b68e0bb3a6ae71a44f380ff1c8d40b7fae383d7c234a8050c0e35103464cf`). The file contains for each family: prior RQT-604 certificate hash, old nonliftability flags, replacement residues and 14M coordinates.

## Next natural bound — RQT-608: Compatible Higher-Order Lift Mesh

Extend the same *coordinate-pair* classes to higher 2-adic and 7-adic powers with deterministic replay. Distinguish a failure of a particular branch from total loss of solutions at a modulus. Preserve the 82/53 all-scale count until a genuinely all-scale obstruction is certified.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
