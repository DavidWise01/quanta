# RQT-437 — Zero-Plane Closure and Extreme-Denominator Cone

Date: 2026-11-16. Canonical RQT-401 candidate successor Gram, SHA256 `5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809`, with exact `B^T F4 B=Q`.

## New unbounded theorem: zero plane excluded

Let A=Q/2, a=A00, c=A02, f=A22. For y=0 the norm equation for rational witnesses is `a*x²+2*c*x*z+f*z²+d²=0`. Exact coefficients satisfy a≡c≡0, f≡3 (mod 11), and a≡88 (mod 121).

Modulo 11 this becomes `3z²+d²=0`; since -3≡8 is a nonsquare mod11, it requires 11|z and 11|d. Modulo 121, the z- and d-dependent terms vanish, leaving `88x²≡0`, which forces 11|x. Consequently **every solution with y=0 is divisible by 11 in all four coordinates (x,0,z,d)**. Such a solution cannot be primitive; dividing by 11 repeatedly would eventually force the zero vector. Hence no nonzero rational isotropic witness exists on the plane y=0. This argument holds without any coordinate bound.

## Exact expanding-cone inequality

Put `alpha=c²-fa<0`, `K=ce-fb`, `gamma=e²-fg`, and `delta=-f>0`. The exact discriminant for a rational witness is `E_d=alpha*x²+2*Kxy+gamma*y²+delta*d²`. Completing the square gives

`alpha*E_d=(alpha*x+K*y)² - ((K²-alpha*gamma)*y²-alpha*delta*d²)`.

Since alpha is negative, the real-feasibility condition E_d>=0 is exactly

`(alpha*x+K*y)² <= (K²-alpha*gamma)*y²-alpha*delta*d²`.

This is valid for *all* nonzero denominators, including the region `|d|>2^531|y|`. It is only a real-feasibility condition; E_d must also be an exact square and the z integrality congruence must hold. Sample `(x,y,d)=(0,1,2^600)` is real-feasible outside the fixed cone, but its discriminant is nonsquare.

## ASCII

```
        RQT-437 : ZERO-PLANE + EXTREME CONE
          q(x,y,z) = -d²
                 |
        +--------+---------+
        |                  |
       y=0               y!=0
        |                  |
      mod 11         EXPANDING CONE
      11|z,d        discriminant >=0
        |                  |
      mod 121        exact square?
      11|x                |
        |              integral z?
   NOT PRIMITIVE          |
        X            ORIGINAL F4
                             |
                         ROOT19 OPEN
```

Full matrix and SHA verified; original rational witness OPEN; integer root19 OPEN; root18 frozen-prefix ordering UNVERIFIED; root20 OPEN; root21 conditional. The JPG is conceptual illustration, not a mathematical witness. One original matrix ancestry underlies all versions.

Next RQT-438: exploit the zero-plane exclusion and expanding cone to design a direct exact rational seed algorithm for y≠0.
