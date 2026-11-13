# RQT-339 — Exact joint-wedge search in original frozen F4

**Status:** exhaustive finite negative result on original RQT-242 lattice for positive x2=5001..5010; negative slices by central symmetry. Original eighteenth root and roots 19–21 OPEN.

## Source
Authentic Gram F4 from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`. RQT-338 established unimodular chart and exact necessary wedge:
`z=(x2,y0,x0,-13*x1-10*x3)`, `y0=-24x0-22x1-17x2-17x3`, `det U=1`,
`x2*y0<0`, `2/125<|y0|/|x2|<63/250`, with `|x2|>=5001` after RQT-337/A. RQT-254/332/333 established `|y0|>=1021` for norm -2; **that additional height condition is not assumed for norm zero**.

## Exact exhaustive search

Let `J=U^-T F4 U^-1`; separate the first two coordinates `b=(x2,y0)` from `w=(z2,z3)`. Let `P=-J[2:4,2:4]` positive definite, `V=P^-1 J[2:4,0:2]` and `K=J[0:2,0:2]+J[0:2,2:4] P^-1 J[2:4,0:2]`. Then

```
z^T J z = b^T K b - (w-Vb)^T P(w-Vb).
```

For each positive x2 t=5001..5010, enumerate **every** integer y0 in the exact necessary wedge. For norm -2, additionally impose the earlier |y0|>=1021 bound. For each (t,y0), compute `R=b^T K b-target`. If R<0 no candidate can exist. When R>=0, let δ0=z2-(Vb)0 and δ1=z3-(Vb)1 and complete the square in P:

```
alpha*δ0²+P11*(δ1+(P01/P11)*δ0)²=R,
alpha=P00-P01²/P11>0.
```

The script chooses **outward** exact rational integer ranges for z2 and z3 and validates the enclosure inequalities; for each candidate pair it solves the last coordinate z3 by the exact integer discriminant of the full quadratic form. All arithmetic is integer/Fraction/SymPy, with `math.isqrt` for perfect squares. No coordinates have an arbitrary cutoff.

## Exact counts

| positive x2 | norm 0 pairs | norm -2 pairs |
|---:|---:|---:|
| 5001 | 166,752 | 23,672 |
| 5002 | 166,792 | 23,688 |
| 5003 | 166,840 | 23,712 |
| 5004 | 166,912 | 23,768 |
| 5005 | 166,960 | 23,816 |
| 5006 | 167,048 | 23,848 |
| 5007 | 167,088 | 23,848 |
| 5008 | 167,136 | 23,888 |
| 5009 | 167,184 | 23,920 |
| 5010 | 167,280 | 23,968 |
| **Total** | **1,669,992** | **238,128** |

For both targets all tested discriminants were nonnegative, but **zero** were perfect squares. Thus **no exact integral solution** of norm zero or minus two exists for `5001<=|x2|<=5010`.

## Conditional combined bound

RQT-336/337-A proved no solutions on x2=0; RQT-337 excluded 1<=|x2|<=5000. Taking their previously established results together with RQT-339 yields

```text
Any nonzero integral isotropic vector or integral norm -2 vector
on the authentic F4 must satisfy |x2|>=5011.
```

This is an exclusion through a finite height, not proof of global nonexistence. The original exact root18, continuation roots19–21, and completed 21-reflection word remain OPEN.

## Reproduction and lineage

Run `python research/rqt339-authentic-joint-wedge.py` with SymPy. The 1,908,120 tested coordinate pairs refer to two separate target equations and are not independent source witnesses. Both derive from the same original F4. RQT-338 is an exact necessary test, not sufficient for root existence. The nested 3×3×3 cubit, Josophene, Juliet and time-angle indices remain provenance/search metadata.

## RQT-340 next natural bound

Use a global exact rational-isotropic solver rather than pushing heights ten slices at a time; alternatively use certified simultaneous congruence constraints on the two-coordinate wedge and build a reusable checkpointed exhaustive scanner. Never promote modular approximations to integral witnesses.
