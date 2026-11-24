# RQT-655 — Exact Fermat Compositeness Certificates

Reopened the RQT-654 complete exact cofactor certificate, SHA-256 `f96f757aeb861f7a0c117639c91c6653fb00b745227cf80eb36b6bb2cbe4eae8`. Evaluated all 31 unresolved odd remainders with **exact integer** `pow(2,n-1,n)`. If odd n>2 were prime, Fermat's little theorem would require the result to equal 1. Hence a result other than 1 is a direct certificate that n is **composite**.

**Results:** 23/31 proven composite. Eight are still **NOT CERTIFIED PRIME**. Passing a base-2 Fermat test does not establish primality. No new prime is certified this turn.

**Proven composite (zero-based cofactor indexes):** `2,3,5,6,7,8,9,10,11,13,14,15,16,17,18,19,20,21,22,25,27,29,30`.

**Primality unresolved:** `0,1,4,12,23,24,26,28`.

The verifier additionally checks exact recomposition of each RQT-654 cofactor from its prior certified factors and remaining n. Full local certificate `RQT-655-results.json` SHA-256 `f8b712bfd62052d9f01590b8061de0bdcb613b769b24ff1c614e3a453f2f9198` contains the original integer n and exact Fermat residue of every candidate.

**Proof boundary:** A compositeness witness is not an explicit factor; no factor is required for the proof. No ordinary integer norm−2 root, generalized Pell seed, full-family exclusion, or original 22D Wall replay. The 31 cofactors derive from the same original owned quadratic corpus and do not provide independent evidence witnesses.

Selected ledger: **82/135 excluded at all scales (60.74%); 53 unresolved**, across 27 canonical sign-orbits. **Root 19 OPEN.**

**RQT-656 next bound:** Attempt bounded explicit factor recovery for the 23 composites, and full primality certificates for any of the eight open integers. Keep original integer coordinate and global norm checks decisive.

`{{i}} · .dlw`