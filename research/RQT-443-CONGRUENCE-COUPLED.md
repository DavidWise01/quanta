# RQT-443 — Congruence-Coupled Kernel

For p=13,23 the frozen Gram has v_p(f)=1. Write C=M+d². If p does not divide L, the reduced linear equation has a simple root and Hensel lifts. If p divides L but not C, no Z_p root exists. Otherwise divide by p: the leading coefficient f/p is a unit, so completing the square gives an equivalent local test for E′=(L/p)²−(f/p)(C/p). This is a necessary and sufficient Z_p criterion for the fixed triple x,y,d, not a global integer witness.

Executed full source SHA and F4 backmap checks. Previous rectangle: 2008 valuation survivors, 1997 after p13 and p23. New tile y=641..704, odd d=1..767: 24576 pairs, 253056 feasible x, 371 valuation and coupled survivors; zero exact squares in both regions. Complete coverage y=1..704, odd d=1..767, all x,z, with negative y by sign symmetry. Root19 OPEN; predecessor18 unverified. Root20 OPEN, root21 conditional.

```
RQT-443 :: CONGRUENCE-COUPLED KERNEL
       f z^2 + 2L z + C = 0
                 |
          p = 13 / 23
       /         |         \
   p ∤ L    p|L,p ∤ C    p|L,p|C
 regular       reject      divide by p
   lift          X         test E'
       \                    /
         exact square check
                 |
       2368 survivors / 0 squares
            ROOT19 OPEN
```

The original F4 norm for a witness is -2d². JPG generated separately as conceptual art, not a proof. Next: general valuations at primes dividing f, or constructive rational isotropy.