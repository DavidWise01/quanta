# RQT-423 — The Unimodular Search Gate

Date: 2026-11-16. Actual full RQT-401 candidate-successor lattice.

## Exact basis-aware rational-line search

Let A=Q/2. RQT-419 supplied T=[[-9,-25,0],[-5,-14,0],[0,0,1]] with determinant +1. Set C=T^TAT. The map w=T w' is a bijection on both integral and rational numerator coordinates and preserves the equation w^TAw=-d².

Search u=(a,1), v=(b,0), a,b in [-6,6]^3, b!=0, for rational zeros of H'=diag(C,1). Set alpha=b^TCb, beta=a^TCb, gamma=a^TCa+1. A rational zero on the line occurs iff D=beta²-alpha*gamma is a nonnegative integer square. The script accepts a vector only after primitive normalization and direct substitution against H and the original F4 backmap.

## Executed full lattice computation

- 2197 anchors; 2196 nonzero directions
- 4,824,612 exact rational lines
- 1,657,832 nonnegative discriminants
- 0 square discriminants; 0 explicit rational witnesses

The search is finite but implies a stronger bounded-height statement: **there is no primitive rational witness whose transformed numerator coordinates are all between -6 and 6, regardless of the denominator.** If one existed, the search would include u=(0,0,0,1), v=(w',0), with alpha=q(w')=-d², beta=0, gamma=1 and D=d², necessarily a square.

This is a bound on the numerator, NOT a global nonexistence result. Rational existence remains established abstractly in RQT-414; an explicit rational coordinate vector still has not been constructed. The underlying conditional candidate root18 has not been verified against the frozen 17-reflection prefix.

## ASCII

```
        RQT-423 : UNIMODULAR SEARCH
       +--------------------------------+
       |  A=Q/2 , T in GL3(Z)          |
       |       det(T)=+1               |
       |        C=T^T A T              |
       |             |                 |
       |    2,197 x 2,196 lines        |
       |             |                 |
       |    4,824,612 tested           |
       |    1,657,832 nonnegative      |
       |         0 squares             |
       |             X                 |
       |   numerator box [-6,6]^3     |
       |    excluded for any d         |
       |             |                 |
       |       ROOT19 OPEN             |
       +--------------------------------+
```

The new 3D JPG is a conversation artifact, not an independent proof or integer witness. Root19 OPEN, root20 OPEN, root21 conditional.
