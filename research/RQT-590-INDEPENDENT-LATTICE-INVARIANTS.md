# RQT-590 — Independent Rank-Four Gram/Wall Invariants

## Recovery
Recovered Library archive `rank4_gram.json` (4×4) with SHA-256 `e93f43e85f6b70c76d5eb8c043644cf7862ed08593ed0549e814a4a774d3c58c`, and `rank4_wall.json` (4×4) with SHA-256 `5893d5c8b6b7b8048d68d115c8e935ae509f5d4e11c828e7439dae924a64d031`. Both fingerprints exactly match the RQT-575 source ledger.

The independent RQT-589 exact Schur/discriminant matrix `M` and coefficient `a` establish:
```text
det(G) = -det(M) / a²
       = -8281492574115056973770683990411769007319047636247715225543944839911172
```
This exactly agrees with the determinant of the independently recovered 4×4 rank-four Gram. The Gram is symmetric, and the Wall relation `Wall + Wall.T = -Gram` holds on the archived rank-four matrices.

## What this does and does not prove
**Verified:** two source file fingerprints, exact matrix dimensions, Gram symmetry, Wall symmetrization, exact Schur determinant equality across independent source paths.

**Not verified:** the canonical RQT-575 *reduced* 4×4 Gram with expected SHA-256 `aa8607e3582dd979ee35a07782bb56eafc6c247a7edf6584531bb7cc9844473d`; the unimodular HNF/LLL basis transformation to this matrix; a candidate integer `u`; any replay in the original 22D lattice; a nineteenth root. The recovered rank-four original Gram is not interchangeable with the reduced Gram for coefficient recovery.

**Selected-family ledger:** 81 excluded, 54 unresolved among 135 chosen corridors; unchanged.

## Next natural bound — RQT-591
Reconstruct the exact unimodular reduced-basis transformation using the archived rank-four Gram/Wall, the RQT-575 basis-reduction script, and associated original ambient basis. Demand `U.T * G * U == F_reduced`, `det(U)=±1`, the expected SHA fingerprint where byte format agrees, and Wall symmetrization before attempting any integer-coordinate recovery.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
