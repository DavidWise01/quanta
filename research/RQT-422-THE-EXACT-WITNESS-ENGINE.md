# RQT-422 — The Exact Witness Engine

Date: 2026-11-16. Source ancestry: original RQT-401 reduced candidate-successor Gram, original F4 and B. Candidate root18 position remains unverified.

## Exact constructive algorithm
Set A=Q/2, H=diag(A,1). For integer u,v in Z4, let alpha=v^THv, beta=u^THv, gamma=u^THu. The rational line u+t*v intersects the homogeneous norm-zero quadric when alpha*t²+2*beta*t+gamma=0. If alpha is nonzero, this occurs over Q precisely when Delta=beta²-alpha*gamma is a nonnegative perfect integer square. Then t=(-beta±sqrt(Delta))/alpha is rational. Clear denominators, divide by all-coordinate gcd, check the primitive four-vector (w,d), verify H norm zero and original F4 norm of Bw exactly -2d². The parity theorem requires d odd. The same code validates the complete B^T F4 B = Q identity before searching.

## Actual execution
Choose u=(ux,uy,uz,1), v=(vx,vy,vz,0), each triple coordinate within [-4,4], with v nonzero. There are 729 anchors and 728 nonzero directions. Because A is rationally anisotropic, alpha ≠ 0 for every such v.

- **530,712** exact rational lines examined
- **9,336** nonnegative discriminants
- **0** perfect-square discriminants
- **0** explicit rational witnesses discovered in this finite family

This is **not** global nonexistence: the RQT-414 Hasse–Minkowski theorem still proves rational existence. No original root19 integer vector has been constructed, and frozen predecessor compatibility is unresolved.

## ASCII narrative
```text
           RQT-422 : EXACT WITNESS ENGINE
      +------------------------------------+
      |        H = diag(Q/2,1)           |
      |                 |                 |
      |        u + t*v rational line      |
      |                 |                 |
      |   Delta=beta^2-alpha*gamma       |
      |                 |                 |
      |          INTEGER SQUARE?         |
      |            /         \\          |
      |          NO          YES         |
      |           X           |          |
      |                 rational t       |
      |                      |           |
      |                primitive (w,d)   |
      |                      |           |
      |                  F4 norm check   |
      |                      |           |
      |                  ROOT 19 OPEN    |
      +------------------------------------+
           530712 tested / 9336 D>=0 / 0 squares
```

All three arithmetic representations derive from a single matrix ancestry, not three independent source roots. New JPG and embedded-JPG HTML exist as conversation artifacts; GitHub chapter is ASCII. Root19 OPEN, root20 OPEN, root21 conditional.
