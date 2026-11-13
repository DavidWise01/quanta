# RQT-332 — Exact first unexplored height interval in original F4

**Status:** Exhaustive finite negative result for y0=1001,...,1010 and their negatives. **Root 18 through 21 remain OPEN.**

## Authentic provenance
Original frozen Gram is in `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`. Reduced unimodular coordinates and Gram J are in `DavidWise01/stoicheion/research/rqt/RQT-254-unimodular-second-height.md`. Let x=T^T y, with det(T)=-1 and y0=-24x0-22x1-17x2-17x3.

For any fixed t=y0>0, partition the quadratic form as

```
q(y)=beta*t² - (z-t*v)^T P (z-t*v), z=(y1,y2,y3)
P=-J[1:4,1:4] positive definite,
v=P^-1 J[1:4,0], beta=J00 + v^T P v >0.
```

Thus q=-2 implies (z-tv)^T P(z-tv)=beta*t²+2. Cauchy-Schwarz for the inverse form bounds each of y1,y2 independently:

```
|y_i - t*v_i|² <= (beta*t²+2) * (P^-1)_{ii}.
```

The script constructs **outward integer box bounds** and proves each outward inequality with exact rational arithmetic, so no admissible y1/y2 pair is excluded. For each pair, it sets q(t,y1,y2,y3)=-2, an exact integer quadratic A*y3²+B*y3+C=0, and checks nonnegative discriminant, perfect square by integer isqrt, and the full integer divisibility condition. No artificial bound is placed on y3.

## Executed result (positive slices)

| y0 | candidate y1/y2 pairs | square discriminants | integral roots |
|---:|---:|---:|---:|
| 1001 | 103596 | 0 | 0 |
| 1002 | 103984 | 0 | 0 |
| 1003 | 103984 | 0 | 0 |
| 1004 | 103984 | 0 | 0 |
| 1005 | 103984 | 0 | 0 |
| 1006 | 104372 | 0 | 0 |
| 1007 | 104372 | 0 | 0 |
| 1008 | 104372 | 0 | 0 |
| 1009 | 104372 | 0 | 0 |
| 1010 | 105840 | 0 | 0 |
| **Total** | **1,042,860** | **0** | **0** |

Negative y0 slices follow by central symmetry y → -y. This search excludes **all** integral norm−2 roots in the stated slices, regardless of parity; it therefore excludes admissible root18 there a fortiori.

The previously published RQT-254 bounded exhaustive audit reported no norm−2 root with |y0|<=1000, but **RQT-332 did not rerun that audit**. Combining the two independent result sets gives the necessary height condition |y0|>=1011, conditional on accepting the prior audit.

## Limits
This is not a global nonrepresentation theorem, a proof of absence of norm−2 roots, or an eighteenth-root witness. RQT-247 supplies an existential argument but not explicit frozen coordinates. The current integral roots 18–21 remain unsolved. The bridge orientation obstruction must not be imported into the authentic F4.

## Next RQT-333
Use a strong *conditional two-coordinate Schur bound* to reduce candidate pairs and extend the exact height interval, with a deterministic ledger of completed slices. Search exact norm 0 as a parallel target toward the primitive hyperbolic plane construction. Keep both targets' evidence separate.

## Tensor routing
The 3×3×3 cubit / Josophene / Juliet and time-angle address encode metadata and source ancestry; they do not substitute for exact norm tests.
