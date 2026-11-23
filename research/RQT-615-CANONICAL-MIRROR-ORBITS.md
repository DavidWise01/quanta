# RQT-615 — Canonical Mirror-Orbit Compression and Exclusion Reconciliation

## Executive result
Reopened exact RQT-583 / RQT-584 / RQT-586 JSON archives and the RQT-614 sign-involution certificate. The SHA-256 fingerprints of the three original archived JSON inputs matched the recorded source hashes. Rebuilt each orbit **from the ray and offset data**, then checked exact (A,B,C,D) mirror identities and exclusion statuses. No floating-point arithmetic.

**The 80 archived RQT-583 families form 41 mirror orbits**:
- 39 two-element mirror pairs.
- 2 self-mirrors (families 13 and 67).
- **14 excluded orbits**: 13 pairs and the self-mirror 13, representing 27 family IDs.
- **27 unresolved orbits**: 26 pairs and the self-mirror 67, representing 53 family IDs.
- **0 mirror-status conflicts**. Every previously excluded archived pair has both members excluded; no pair mixes excluded and unresolved statuses.

The canonical representative of an orbit is its smallest family index. This gives **27 canonical unresolved research cases instead of 53 family-address searches**, without erasing the partner's identity or double-counting mirror evidence. Under sign inversion, the exact integer quadratic norm and discriminant relations are
```
Q_partner(-u,-t)=Q_canonical(u,t)
Delta_partner(-t)=Delta_canonical(t).
```
Results transfer along these exact equalities.

## Scope and provenance
RQT-583 starts after **55 previously excluded selected families**; those 55 are not present in the 80-equation archive, so their mirror structure cannot be reconstructed from this archive alone. Do not advertise the 41 orbits or 27 remaining orbits as the complete symmetry quotient of all 135 selected corridors or the original rank-four lattice.

Global **family-ID** ledger remains **82/135 selected excluded all-scale (60.74%), 53 unresolved**. Compression is computational deduplication, **not** a new all-scale family exclusion. No integral norm−2 root or original 22D Wall replay was performed. **Root19 OPEN**.

## Executed local certificate
The standalone exact verifier `research/rqt615-canonical-orbits.py` reconstructs the 41-orbit table, tests status closure, checks all sign-reflected discriminants, and emits every canonical ID, both original IDs, ray, canonical offset and evidence ancestry. Local full certificate `RQT-615-results.json` SHA-256:
`f2c7a414a4139b271cfa60ddb65d135a372e648061dc10ea14a7e7bfc1564f06`.

The archived source SHA-256:
- RQT-583: `5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92`
- RQT-584: `29f0eb2b4ef29d3194185ee45d72c58a793b41bd44993b0b6ad33bf3435cbe5f`
- RQT-586: `45d129e80c7d6b19af2ba7a7e8e541f865e37646a2709efebbba87bb584a4859`

## Next bound — RQT-616
Construct a canonical **27-orbit test planner** preserving the original 53 family IDs and exact inverse maps. Rank by genuinely new arithmetic tests (primitive direct norm/Pell compatibility) instead of multiplying finite search windows, and leave the original 55 selected families unclassified under sign-symmetry until their source data is reopened.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`