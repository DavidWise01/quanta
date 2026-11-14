# RQT-372 — Generation-five exact witness routing and dead-path repair

**Date:** 2026-11-14. **Executed PASS** on authentic original F4. **Root18 OPEN**; roots19–21 OPEN.

## Genuine RQT-371 continuation, all 27 cores instantiated

The complete cubic geometry is **nine generations of 9×9×9 = 729 microcells**, grouped as 27 spatial macrocores with 27 microcells apiece, around the singlet inside `||||`. Each generation contributes a balanced signed base-nine digit to each of three search coordinates. The fourth coordinate is constrained by the exact original-lattice discriminant.

RQT-371 provided three viable generation-three witnesses per spatial core, 81 in total. Their parent claims were **valid only through generation three**; this turn checked each proposed generation-four continuation before promotion.

**New counterexample discovered:** the selected g3 representative `(-364,-350,-356)` in macrocore `FCL`, descended from g2 parent `(-40,-26,-32)`, has **zero** viable generation-four children. This makes it invalid to promote that witness automatically to generation five. It is not a proof that its g2 parent is dead.

A deterministic exact sibling search found another g3 descendant of that same g2 parent:
```text
FCL: g2=(-40,-26,-32)
 old g3=(-364,-350,-356)   -> no g4 descendants
 new g3=(-364,-350,-275)
 new g4=(-3280,-3266,-3191) -> valid square-residue gate mod 9^4
```
The other 80 routes retain a valid generation-four representative. No original norm-minus-two integer vector is claimed.

## Exact generation-five gate

Let `F4` be the original frozen symmetric even integral Gram from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`, `U` the exact unimodular RQT-363 coordinate chart, `G=U F4 U.T`, and
```text
K_ij=G_i3*G_j3-G33*G_ij
Delta(a,b,c)=(a,b,c).T K (a,b,c)-2*G33.
```

For a selected g4 triple t, every generation-five child t' is t+9^4 (i,j,k) with i,j,k in {-4,...,4}. Its descendants agree on Delta mod 9^5=59049. Thus a nonquadratic residue mod59049 would certify impossible descendants. Every one of 81 selected g4 representatives was tested against all 729 fifth-generation children, **59,049 child states**.

Two exact square tests were separately evaluated on every child:
- independently enumerated squares of integers modulo 59049;
- exact 3-adic valuation and unit-square condition.

Both always agreed; results:
```text
27 cores; three certified g4 routes per core = 81 routes
g5 children enumerated = 81*729 = 59,049
g5 modular-square exclusions = 0
g5 surviving necessary condition = 59,049
dead g3 routes discovered and repaired = 1
exact original F4 norm -2 roots found = 0 (no full-root search this stage)
```

**Important:** the zero g5 exclusions reflects these **selected g4 families only**. It neither means the full generation-five space has no exclusions nor that any of the 59,049 descendants is an actual root. A modular-square survivor is only a surviving necessary condition.

## Independent replay and source ancestry

The executed local program generated 27 append-only hash-linked core packets, one per macrocore:
`/mnt/data/rqt372_g5_packets.jsonl`.
Each entry records g2 ancestry, the accepted g3/g4 vectors, whether the route was repaired, per-route g5 counts, and its predecessor SHA-256. Last hash:
```text
a3947b888e715dc53fc1286a47e1c6c6c899ba1f50d8e3d521ecce07bfe5cb7a
```
The independent local verifier replayed **all 59,049** fifth-generation conditions and the entire 27-entry hash chain, recovering the same hash and counts.

The GitHub executable `research/rqt372-g5-cubic-witness-router.py` is self-contained: it embeds the RQT-371 parent-selection procedure, regenerates all 27 original parent packets, repairs the dead FCL route, audits the generation-five children, and emits its own complete hash-linked packet JSON. GitHub packet hashes may differ from the separately executed local JSONL because the upstream packet field schemas differ; the local hash above specifically identifies the locally replayed archive. Arithmetic counts and route ancestry are the same.

**Source-correlation invariant:** both modular tests, the exact norm check, and the 27 GMA cores all derive from **one frozen original F4 source**. They are distinct computations but are not independent primary-source witness ancestries.

## Mathematical status and next target RQT-373

RQT-372 *does not* construct a root. The saturated selected g5 residue gate indicates the next meaningful direction is to diversify exact arithmetic checks (other primes and a constructive global representation algorithm) rather than claim that simply advancing the cube depth is progress toward a global integral solution.

A genuine root18 still requires an explicit integer r with `r.T F4 r=-2`, permitted parity, and frozen 17-reflection factorization/order compatibility. There is no universal all-17 H-orthogonality gate (corrected in RQT-363); six pairings are internal to the proposed four-root completion.

**Root18 OPEN. Roots19–21 OPEN.**
