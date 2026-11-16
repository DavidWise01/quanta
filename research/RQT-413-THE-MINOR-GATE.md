# RQT-413 — The Minor Gate: all finite primes

Date: 2026-11-15. Full source: RQT-401 candidate-successor Gram.

## A single finite exact certificate replaces the 3512-bit determinant factorization

Set A=Q/2, an integral symmetric ternary Gram. The gcd of all **nine** 2x2 minors of A is exactly **9**; the gcd of its entries is 1. These values were computed directly from the full integer Gram, without floating-point arithmetic.

For any odd prime p other than 3, not all 2x2 minors vanish modulo p. Thus rank(A mod p) is at least 2. Over a field Fp of odd characteristic, a symmetric form of rank at least 2 contains a nondegenerate binary subform. Every nondegenerate binary quadratic form represents every nonzero scalar over Fp, by either the split hyperbolic model or surjectivity of the quadratic finite-field norm. Its representation of -1 has nonzero gradient, and so lifts to a Z_p solution by the ordinary Hensel lemma.

At the exceptional p=3, A mod3 is
 [2 0 2]
 [0 0 0]
 [2 0 2]
and the seed v=(0,0,1) represents -1, with gradient (1,0,1) mod3, so that branch also lifts to all powers of 3. A constructive chain through 3^8 is verified.

For p=2, fix y=0,z=1, put a=A00, b=A02, c=A22+1. The discriminant b²-ac is 1 mod8 and a is odd, giving a Z_2 solution. Explicit check through 2^16 passed.

Therefore the inhomogeneous ternary norm equation v^T A v=-1 is locally soluble at **every finite prime**, including infinitely many determinant primes without factoring the determinant.

## Scope
This is a genuine unbounded local theorem but NOT a root19 integral witness or an integral local-global theorem. The RQT-386 root vector has not been verified as the eighteenth reflection of the original frozen 17-reflection prefix, so the root19 identification remains conditional. Root19 OPEN, root20 OPEN, root21 conditional.

## ASCII
```
           RQT-413 : THE MINOR GATE
      +-----------------------------------+
      | A = Q/2   target A(v) = -1       |
      |                                   |
      | gcd(all nine 2 x 2 minors) = 9  |
      |                 |                 |
      |           +-----+-----+           |
      |           |           |           |
      |         p != 3       p = 3        |
      |        rank >= 2    (0,0,1)       |
      |           |          |            |
      |      binary form   regular        |
      |           +-----+----+            |
      |                 |                 |
      |             HENSEL              |
      |                 |                 |
      |      +----------+----------+      |
      |      |   p = 2: D = 1 mod 8 |      |
      +------+---------------------+------+
                     |
          LOCAL ROOT AT EVERY PRIME
                     |
             INTEGER ROOT 19?
                     |
                    OPEN
```

The generated high-definition JPG and embedded-JPG HTML are separately available as conversation artifacts. This GitHub record preserves the ASCII diagram and the exact verifier.
