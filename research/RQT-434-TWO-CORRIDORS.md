# RQT-434 — The Two-Corridor First-Seed Filter
Date: 2026-11-16. Full frozen RQT-401 candidate-successor reduced Gram.

## Important scope correction
Let A=Q/2, f=A22<0, L=A02*x+A12*y and M=A00*x²+2*A01*xy+A11*y². A rational witness (w,d) with w=(x,y,z) solves q(w)=-d² and has discriminant
 E_d=L²-f(M+d²)=E_1+(-f)(d²-1).
Because -f>0, the slope corridor of RQT-394 derived for integer d=1 must NOT be applied as a necessary filter to unrestricted rational denominators. For x=y=0, d=1, the equation even has real z=1/sqrt(-f) (not an integer since -f nonsquare), clarifying the real versus integral distinction.

## New exact bounded integer-root scan
In the original RQT-401 reduced basis enumerate y=1..3000, all integer x strictly satisfying 177065*y<100000*x<178600*y; apply the RQT-433 prime-13 and prime-23 obstructions, E_1 square mod256, nonnegative E_1, exact isqrt and full z-integrality. Exact arbitrary-precision results:
- 69,094 cone pairs
- p13 excluded 4,905; p23 excluded 2,873; union 7,575
- 61,519 prime survivors
- 13,486 E_1 square-residue mod256
- 13,477 E_1 nonnegative
- **0** exact perfect-square E_1 and **0** integral root witnesses

By vector-negation symmetry, this also excludes 1<=|y|<=3000 for d=1, without excluding larger coordinates or any d>1 witness. Original F4 back-map B^T F4 B=Q and canonical Gram SHA256 verified.

## ASCII
```
         RQT-434 : TWO SEARCH CORRIDORS
                    q(w)=-d²
               /                \
          d=1                    d>1 odd
           |                       |
     RQT-394 CONE        E_d=E_1+(-f)(d²-1)
           |                       |
       p=13/23                 p=13/23
           |                       |
       mod256                 PELL SEED
           |                       |
     EXACT SQUARE          INTEGER z CONDITION
           \                       /
              ORIGINAL F4 NORM
                    |
                ROOT19 OPEN
```

The neon JPG is conceptual art, not independent evidence. GitHub and HTML mirrors share the one original source ancestry. Candidate root18 predecessor ordering unverified; root19 OPEN, rational witness OPEN, root20 OPEN and root21 conditional. Next RQT-435: denominator-aware rational first-seed construction without imposing the d=1 real-cone filter.
