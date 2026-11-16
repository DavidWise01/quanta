# RQT-414 — The Rational Bridge

Date: 2026-11-15. Conditional candidate-successor rank-three form from the canonical RQT-401 full Gram.

## Exact rational-existence theorem

Let Q be the symmetric even restricted Gram; A=Q/2, q(v)=v^T A v. The equation q(v)=-1 has a rational solution (not explicitly constructed).

- A is nonsingular and A00 is negative, so q(v)=-1 has a real solution.
- At p=2, fixing y=0,z=1 gives a quadratic in x with odd leading coefficient and discriminant 1 modulo 8: a Z_2 solution.
- At odd primes p≠3, gcd of all 2x2 minors of A is 9, hence rank(A mod p)≥2, and a nondegenerate binary subform regularly represents -1 modulo p. Hensel lifting gives a Q_p solution.
- At p=3 the regular mod-3 seed (0,0,1) has gradient (1,0,1).
- The homogeneous quaternary form F(v,t)=q(v)+t² has nonzero zeros over R and every Q_p. By Hasse–Minkowski it has a nonzero rational zero (v,t).
- Seven primitive parity classes of q modulo 4 all have nonzero q, proving q is anisotropic over Q (RQT-405). Thus t cannot be 0, and q(v/t)=-1 is an ordinary rational solution.

This is an **existence theorem**, not a constructive rational witness and emphatically **not** integral existence. A rational solution may have large denominators. Simply multiplying denominators changes the represented norm.

## Executable witness audit

The accompanying script checks the exact local and anisotropy hypotheses against the full RQT-401 Gram. It passed locally on the preserved full JSON. The Hasse–Minkowski theorem supplies the global implication; the script does not output rational coordinates.

## ASCII

```
          RQT-414 : THE RATIONAL BRIDGE
       +-----------------------------------+
       |        q(v) = v.T A v = -1       |
       +-----------------+-----------------+
                         |
            +------------+-----------+
            |            |           |
           REAL         p=2       ODD PRIMES
           YES          YES          YES
            |            |           |
            +------------+-----------+
                         |
                  HASSE-MINKOWSKI
                         |
                 RATIONAL v EXISTS
                         |
                  DENOMINATORS?
                         |
                   INTEGER v ?
                         |
                     ROOT19 OPEN
```

RQT-386's root candidate has not been verified as position 18 of the frozen 17-reflection prefix. Root 19 OPEN; root 20 OPEN; root 21 conditional. JPG and HTML with embedded JPG are separate conversation artifacts; this GitHub chapter is ASCII-only.
