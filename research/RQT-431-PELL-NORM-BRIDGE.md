# RQT-431 — The Pell Norm Bridge

2026-11-16. Exact source: full RQT-401 candidate successor Gram Q, original F4 and reduced basis B.

## Exact completed-square equivalence

Set A=Q/2 with entries A00=a, A01=b, A02=c, A11=g, A12=e, A22=f. For integral x,y define L=c*x+e*y, M=a*x²+2*b*x*y+g*y². Let s=f*z+L, E0=L²-f*M. The equation

    w^T A w + d² = 0, w=(x,y,z), d != 0

is equivalent to the generalized Pell-type equation

    s² + f*d² = E0(x,y)

plus the integral-coordinate congruence

    s ≡ L (mod |f|), so z=(s-L)/f ∈ Z.

For the actual matrix f<0 and D=-f is a positive 1352-bit nonsquare integer. Thus s²-D*d²=E0(x,y). This is a *family* of generalized Pell equations, since E0 depends on x,y; the reduction alone does not solve them.

## Executed checker and controls

Loaded full original F4, kernel basis B and reduced Gram Q; checked B^T F4 B=Q, all-even Q and SHA256 5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809.

For five original test vectors, verified exactly:

    (f*z+L)² + f*d²-E0 = f*(w^T A w+d²).

None of the five is null. Positive control A0=diag(1,1,-2), w=(1,0,1), d=1 is accepted; perturbing s is rejected.

An actual primitive rational witness is *not constructed*. The additional requirements are gcd(w,d)=1, d odd, the original F4 norm -2d², and the frozen predecessor compatibility check before a true position-19 root can be claimed.

Pell unit transformations preserve the norm equation but may not preserve s≡L mod |f|. A unit-generated candidate must pass that exact congruence.

## ASCII

```text
       RQT-431 : PELL NORM BRIDGE
    +---------------------------------+
    | Q=2A, 4D quadratic null form  |
    | f=A22<0, D=-f nonsquare       |
    |               |                |
    |  s=f*z + L(x,y)               |
    |               |                |
    |  s² - D*d² = E0(x,y)          |
    |               |                |
    |  s = L (mod |f|)              |
    |               |                |
    |  Original F4 norm = -2d²      |
    |               |                |
    |        ROOT19 OPEN            |
    +---------------------------------+
```

Source and GitHub mirror count as one provenance lineage. The conceptual JPG is not an evidence witness.

Root18 position UNVERIFIED. Root19 OPEN, root20 OPEN, root21 conditional. Next: fixed (x,y) generalized Pell equation solving with exact congruence and original lattice verification.
