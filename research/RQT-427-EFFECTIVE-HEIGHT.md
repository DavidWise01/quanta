# RQT-427 — The Effective Height Gate

2026-11-16. Original full RQT-401 conditional candidate-successor Gram.

**New result:** Cassels' 1955 small-zero theorem gives a provable finite stopping bound for the four-dimensional rational-isotropy search. Let H=diag(Q/2,1) and S=sum over all 16 entries |H_ij|. Since RQT-414 proves H isotropic over Q, there exists a nonzero integer H-null vector X with max|X_i| ≤ (3S)^(3/2). Because coordinates are integers, define the exact bound B=isqrt((3S)^3). A primitive zero can be obtained by gcd normalization without increasing B.

**Exact computed result:** On the actual frozen H, B has 611 decimal digits and 2030 bits. Recomputing in the RQT-419 integral unimodularly transformed basis gives a slightly smaller bound, still 611 digits/2030 bits. This is a mathematically finite search endpoint, not a feasible enumeration. The verifier emits the complete 611-digit integer bounds and all source checks.

The RQT-405 anisotropy theorem for A=Q/2 forces the fourth coordinate d of any H-isotropic nonzero vector to be nonzero; RQT-415 forces it to be odd after primitive normalization. This yields an explicit theoretical bound on a primitive rational witness (w,d), but it does NOT imply |d|=1 and therefore does NOT establish integer root19.

Citation: Lenny Fukshansky, *Heights and quadratic forms: Cassels' theorem and its generalizations*, Theorem 1.1, page 2: https://www1.cmc.edu/pages/faculty/lenny/papers/cassels.pdf

## ASCII

```
       RQT-427 : EFFECTIVE HEIGHT GATE
       +------------------------------+
       | H = diag(Q/2,1), isotropic   |
       |              |               |
       |      CASSELS BOUND           |
       | S = sum_ij abs(H_ij)         |
       | B = isqrt((3S)^3)            |
       |              |               |
       | 611 digits / 2030 bits       |
       |              |               |
       | FINITE, NOT PRACTICAL        |
       |              |               |
       | EXPLICIT RATIONAL: OPEN      |
       | INTEGER ROOT19: OPEN         |
       +------------------------------+
```

Root19 OPEN. Frozen predecessor root18 ordering UNVERIFIED. Root20 OPEN; root21 conditional. The new JPG is conceptual artwork, not an integer-root witness; it and the embedded-image HTML are available separately as conversation artifacts.
