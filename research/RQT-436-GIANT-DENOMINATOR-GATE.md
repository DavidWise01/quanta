# RQT-436 — The Giant Denominator Gate

Date: 2026-11-16. Frozen candidate-successor source: RQT-401 reduced Gram, with SHA256 `5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809`. The original F4 backmap `B^T F4 B=Q` is checked.

Let `A=Q/2`, `f=A22<0`, `L=A02*x+A12*y`, `M=A00*x²+2*A01*xy+A11*y²`. Set `alpha=A02²-f*A00<0`, `K=A02*A12-f*A01`, `gamma=A12²-f*A11`, `delta=-f>0`. Then the discriminant for `q(w)=-d²` is

`E_d=alpha*x²+2*K*x*y+gamma*y²+delta*d².`

For `y!=0`, `E_d/y²` is strictly concave in `s=x/y`, with vertex inside `(177065/100000,178600/100000)`. At each endpoint numerator n, the *exact integer*

`alpha*n²+2*K*n*100000+gamma*100000²+delta*100000²*(2^531)²`

is **negative**, with negative-margin bit lengths 2449 (lower) and 2448 (upper). It follows for all integer coordinates that **if `0<|d|<=2^531|y|` and `E_d>=0`, then `177065/100000<x/y<178600/100000`**. This is an unbounded exact theorem and vastly extends RQT-435's restriction `|d|<=|y|`. The extreme region `|d|>2^531|y|` is not covered.

### Bounded formerly denominator-dominated region

Enumerated every odd `3<=d<=1001`, `0<y<d`, with every integer `x` inside the now justified narrow cone. Sign symmetry covers negative y. Applied known prime 13/23 obstructions, square tests modulo 256,63,65,11,17,19,23,31, full integer discriminant and square root, integral z, and original F4 norm checks.

| Gate | Count |
|---|---:|
| Triple cases | 1,284,928 |
| Excluded by primes | 142,743 |
| Prime survivors | 1,142,185 |
| Modular-square survivors | 4,469 |
| Nonnegative discriminants | 4,467 |
| Exact square discriminants | **0** |
| Rational witnesses | **0** |

**Important limitation:** the special `x=y=0` case cannot satisfy a nonzero rational denominator because `-f` is nonsquare. That does *not* exclude `y=0, x!=0`; this coordinate plane and the extreme denominator ratio remain open. No root19 or explicit rational witness has been constructed. Position18 predecessor compatibility remains unverified.

## ASCII
```
         RQT-436 : GIANT DENOMINATOR GATE
     +------------------------------------+
     |          q(w) = -d^2             |
     |               |                  |
     |        0<|d|<=2^531|y|           |
     |               |                  |
     |  1.77065 < x/y < 1.78600        |
     |         /           \\            |
     |       p13/23     ratio >2^531    |
     |         |            |            |
     |  1,284,928 cases    OPEN         |
     |         |                         |
     |  4,469 modular                  |
     |         |                         |
     |  ZERO exact squares             |
     |         |                         |
     |      ROOT19 OPEN                 |
     +------------------------------------+
```

JPG conceptual only. GitHub/HTML are the same evidence ancestry. Root19 OPEN, root20 OPEN, root21 conditional. Next: exact analysis of y=0 with x nonzero, plus denominator ratio exceeding 2^531.
