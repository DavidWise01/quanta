# RQT-623 — Exact Global Integer-Coordinate Projection Gates

## Result
Reopened RQT-619's exact 27-canonical-orbit coefficient certificate, RQT-591's rederived Gram, and the original 80-family RQT-583 archive. For every canonical family, constructed the exact binary polynomial
`Q(u,t)=q_F(u,ray*t+offset)+2` from the Gram and ray/offset.

Exhaustively evaluated every pair `(u,t)∈(Z/256Z)^2`, retaining the parameter residue `t` precisely when **some** coordinate residue `u` makes `Q(u,t)≡0 (mod 256)`. This is a **necessary condition on every true integer root, at every scale**: if an integer pair solves Q=0, its t residue must be in the supplied set. It is not a sufficient condition and creates no new entire-family exclusion.

## Exact numbers
- Canonical unresolved orbits: **27**, representing **53** original family IDs.
- Modulus: **256**, with **65,536** possible ordered coordinate pairs per orbit, or **1,769,472** residue-pair tests total.
- Allowed t-residue distribution (number of orbits):
  - 128: 10 orbits.
  - 196: 1 orbit.
  - 200: 6 orbits.
  - 224: 4 orbits.
  - 228: 1 orbit.
  - 240: 1 orbit.
  - 256: 4 orbits.
- Each of the 27 families retains at least one coordinate-compatible class.
- Mirror partners inherit the allowed set by negation `t↦−t (mod 256)` using the exact sign involution. Those transfers are **not independent evidence**.

## Independent arithmetic replay
Because every coefficient of Q is even, the archived RQT-619 normal form has `Q=2R` with integral R. The verifier reconstructs and checks all six coefficients of R independently from Gram. It then projects `R(u,t)≡0 (mod 128)` and verifies that the resulting 256-residue t-set is **identical** to the direct projection from Q modulo 256, for every orbit. The latter equality avoids conflating parameter-filter precision with a global solution.

Full local certificate: `RQT-623-results.json`, SHA-256:
`640343c28a6d18aedc0c7dc503d15c3fcdcafd334aa672d034165db23d52efd5`.
Source reproducer: `research/rqt623-coordinate-projection.py`.
Each record contains the canonical/partner IDs, all allowed residues, exact modular coordinate-pair counts, examples, and mirror mapping.

## Scope and next experiment
No full-family exclusion, no integer norm−2 vector, and no original 22D Wall replay. Selected family ledger **82/135 excluded (60.74%), 53 unresolved** represented by 27 canonical orbits. The selected corridors do not exhaust the entire rank-four lattice. Root 19 remains **OPEN**.

**RQT-624 natural bound:** combine these exact parameter residue gates with an odd-prime coordinate congruence (e.g. the exceptional family 28 modulo 31 and family 2 modulo 7) in a CRT-wheel certified test. Prioritize nonredundant arithmetic information and independent source ancestry; avoid equating CRT compatible residues with integer Pell seeds.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
