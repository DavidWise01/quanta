# RQT-614 — Exact Pell Sign-Involution and Mirror-Orbit Compression

## Executive result
Independent reconstruction from the original RQT-583 exact archive (80 Pell equations, SHA256 `5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92`) proves that the archive contains **39 sign-mirror pairs plus two self-mirror families**, indices **13 and 67**. Thus the 80 equations comprise **41 equivalence classes** under an exact integer involution.

For a fixed ray `r`, an offset `o` and its negative `-o`, use integer coordinates `v_i(t)=rt+o`, `v_j(t)=rt-o`. Their relation is `v_j(-t)=-v_i(t)`. Because the homogeneous quadratic Gram norm is even under global negation,
```text
Q_j(-u,-t) = Q_i(u,t)
Δ_j(-t) = Δ_i(t)
A_j = A_i, B_j = -B_i, C_j = C_i, D_j = D_i.
```
This identity holds **at all integer scales**, not just a bounded search. Consequently any exact norm−2 vector on one selected corridor maps to a norm−2 vector in its sign-mirror partner. Likewise a universal family exclusion transfers to the partner. The equivalence does **not** construct a root.

## Archived family counts
- 80 exact archived equations: **39 mirror pairs, two fixed points** (13 and 67).
- Mirrors verified by exact ray/offset comparison, coefficient identities and signed-t discriminant checks.
- This is a classification of the 80 RQT-583 retained equations, **not the entire original 135 selected families** or the complete rank-four lattice.

## RQT-613 wheel mirror regression
Families 2 and 24 are mirrors: same ray `[35,-10,14]`, opposite offsets. Their necessary t residues are negatives mod49:
```text
family 2:  {13,20,27,34}
family 24: {15,22,29,36} = -{13,20,27,34} (mod49).
```
The exact archived RQT-613 wheel residues obey
`Wheel_24 = {-r mod 44051 : r in Wheel_2}`.
Their finite ±20-million search windows are therefore reflections of the same exact arithmetic problem. **Do not double-count them as independent corroboration**. They are still two distinct entries in the original selected-family ledger.

## Certificates
- `research/rqt614-mirror-involution.py` is the independently executable verifier.
- Full JSON results `RQT-614-results.json` SHA256:
`672e66d4dc8db63d6e47aa461e10bd067adfd724201e29c8f1249753a3915f42`.
- Records all 39 paired indices, two self-mirrors and both source digests.

## Honest scope
No new all-scale exclusions: the selected-family ledger remains **82/135 excluded (60.74%) and 53 unresolved**. The two mirrored searches in RQT-613 were not independent evidence. A mirror symmetry does not establish the existence of an integer norm−2 vector, an integral Pell seed, or the original 22D Wall conditions.

## RQT-615 natural bound
Normalize **all 53 unresolved selected families into canonical sign-orbits**, check whether the archived exclusion ledger is mirror-closed, then allocate one search per orbit while preserving individual-family IDs and immutable ancestry. Only claim newly excluded families when a valid all-scale mathematical obstruction exists. Avoid confusing compression of equivalent cases with progress toward Root 19.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
