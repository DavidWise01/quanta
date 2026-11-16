# RQT-420 — The Hyperbolic Construction Gate

2026-11-16. Full source: RQT-401 exact candidate-successor Gram Q. Candidate root18 compatibility with the frozen 17-reflection predecessor remains UNVERIFIED.

## Exact rational diagonal congruence
Set A=Q/2 and H=diag(A,1). Its exact LDL^T decomposition supplies rational P with P^T H P diagonal. With Delta_k the leading principal minors and Delta_0=1, the diagonal is (Delta1, Delta2/Delta1, Delta3/Delta2, 1). Verified signs (-,+,-,+), signature (2 positive,2 negative), leading-minor signs (-,-,+,+). Numerator bit lengths: (1088,2161,3509,1); denominator bit lengths: (1,1088,2158,1). This rational congruence is NOT a unimodular integer basis change.

## Global Witt-index-one theorem
RQT-414 established that H has a nonzero rational isotropic vector via Hasse–Minkowski and local solvability. RQT-405 established that A is anisotropic over Q, using its seven primitive parity residues mod4 (3,2,3,1,2,3,2) for parity strings 001,010,011,100,101,110,111. If H had a two-dimensional totally isotropic rational plane, that plane would intersect the 3D hyperplane d=0 in a nonzero vector, giving a rational isotropic vector for A. Contradiction. Thus **Witt index of H over Q is exactly one**.

This proves a rational hyperbolic plane exists abstractly. No explicit rational isotropic vector, denominator, or ordinary integer root19 has been found. RQT-419's distinct integral unimodular transformation remains valid.

## ASCII
```text
           RQT-420 | WITT INDEX ONE
      +--------------------------------+
      | H = diag(Q/2, 1)               |
      |               |                |
      |      rational LDL^T            |
      |               |                |
      |          (-,+,-,+)             |
      |               |                |
      |       Witt index = 1           |
      |               |                |
      |      rational null basis?      |
      |             OPEN               |
      |               |                |
      |       integral root 19?        |
      |             OPEN               |
      +--------------------------------+
```

JPG and embedded-JPG HTML are conversation artifacts. The generated visual is conceptual, not a mathematical witness. Root19 OPEN; root20 OPEN; root21 conditional.

Next: RQT-421 constructive rational isotropic-vector algorithm with direct exact substitution.