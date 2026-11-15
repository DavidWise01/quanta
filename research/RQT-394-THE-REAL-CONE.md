# RQT-394 — The Real Cone: a global archimedean corridor for root19

**2026-11-15 | Exact original frozen F4/H4 arithmetic PASS | Authentic root19 still OPEN.**

## Continuing the original problem

RQT-386 constructed an exact original-F4 norm-minus-two reflection, RQT-387 proved it meets the first residual rank/order reduction, and RQT-388 constructed its saturated rank-three Wall successor kernel. RQT-389–390 excluded all three reduced coordinate hyperplanes; RQT-391 searched 400 million pairs with the third coefficient unrestricted; RQT-392–393 constructed and sharpened necessary modular CRT gates (to 1/9000 of coefficient residues modulo 43200). No exact root19 has yet been found.

RQT-394 moves beyond congruences to an **unbounded real-geometric necessary condition** on every exact integral root19 in the **fixed RQT-388 reduced basis**.

## Original exact equation

Let `B∈Z^(4×3)` be the verified saturated integer root19 kernel basis and `Q=B.T F4 B`. Every potential root19 is `r19=B*(x,y,z)` and must satisfy:

```text
r19.T H4 r18 = 0
r19.T F4 r19 = -2
(x,y,z).T Q (x,y,z)=-2.
```

Write `a=Q00, b=Q01, c=Q02, d=Q11, e=Q12, f=Q22`. Solving exactly for *unbounded* integer third coordinate `z` requires

```text
f*z² + 2*(c*x+e*y)*z + a*x²+2*b*x*y+d*y²+2 = 0.
```

Its integer half-discriminant is

```text
D(x,y) = (c*x+e*y)² - f*(a*x²+2*b*x*y+d*y²+2)
       = A*x² + 2*K*x*y + C*y² + T,

A=c²-f*a, K=c*e-f*b, C=e²-f*d, T=-2f.
```

The exact original Q yields `A<0, K>0, C<0, T>0`, plus `A+T<0`. Every genuine root19 must have a nonnegative **perfect-square** D and an integral quotient `z=(-cx-ey±sqrt(D))/f`. A real discriminant D≥0 alone is weaker than a root.

## Unbounded theorem — exact rational corridor

For any nonzero integer y, set `s=x/y`. Since y²≥1,

```text
D(x,y)/y² = A*s²+2*K*s+C+T/y².
```

This expression is a **strictly concave quadratic** in s, with vertex `s=K/(-A)`.

Choose the two exact rational boundary slopes

```text
L = 177065/100000 = 1.77065
U = 178600/100000 = 1.78600.
```

The executable verifies, using exact integers and no floating-point rounding:

```text
L < K/(-A) < U.

Let n be 177065 or 178600, d=100000.

P(n) = A*n²+2*K*n*d+C*d².
P(n)<0, and P(n)+T*d²<0.
```

Since `T/y²≤T` and the concave quadratic decreases as one moves away from its vertex, **D(x,y)<0** for every nonzero integer y whenever `s≤L` or `s≥U`. For y=0, `D(x,0)=A*x²+T<0` for any nonzero integer x, separately verified.

Thus EVERY valid root19 in this fixed integral basis must obey the globally valid necessary condition:

```text
y != 0
177065/100000 < x/y < 178600/100000.
```

This is not confined to ±10000 or any finite radius. It is a narrow conic wedge in the (x,y) projection of the 3D successor lattice. A change of lattice basis would change the numerical slope interval, but not the truth of the certified restriction in these recorded coordinates.

The exact integer negative-margin certificates at the endpoints have bit lengths **2451** and **2450**, respectively, for `-(P(n)+T*d²)`; both are strictly positive integers. Reproducible code computes these large integers from the frozen F4 rather than trusting rounded displayed values.

## Real isn't integral: independent example

The pair `(x,y)=(16,9)` lies inside the certified real wedge. Its exact discriminant is **positive** but **not a perfect square**. It therefore has real solutions for the third coordinate but **no integer root19** at those x,y. This is an exact original-lattice example of the essential distinction between archimedean feasibility and integral representation.

## Reproduce

```bash
python research/rqt388-exact-second-key.py --bound 30 --out /tmp/rqt388.json
python research/rqt394-real-cone.py /tmp/rqt388.json --out /tmp/rqt394.json
```

The RQT-394 executable verifies original F4/H4, the exact saturated reduced Gram identity `Q=B.T F4 B`, both exact rational boundary inequalities, the y=0 obstruction, and the inside-cone non-square example.

The locally executed original analysis is `/mnt/data/rqt394_real_cone.py`; its run emitted `/mnt/data/RQT-394-results.json`.

## 3D illustration and persistent story

The cinematic **RQT-394-The-Real-Cone-3D.jpg** is an original explanatory picture of a slender golden conic corridor cut through the user's nine nested 9×9×9 GMA generations (27 spatial cores, center `||||`) toward root19. The picture is **not** a plot of exact high-bit integer coordinates. The accompanying local `RQT-394-Embedded-3D-Story.html` contains the JPG bytes embedded directly as a data URI and opens offline. The GitHub `rqt394.html` is an independent 3D CSS visualization of the same verified result. The JPG binary itself has **not been committed as a GitHub asset**.

## Next natural target — RQT-395

Exploit the rational wedge to construct a **continued-fraction / lattice rational approximation search in the (x,y) plane**. Filter only exact-integer (x,y) pairs inside the archimedean cone, impose the already proved CRT constraints and test exact discriminant squares and inverse third-coordinate divisibility. Prefer a certified constructive integer norm solver to merely increasing radii.

**Root18: first-stage accepted. Root19: OPEN. Root20: OPEN. Root21: conditional on a valid first three-root Wall flag. Full 21-reflection word: OPEN.**
