# RQT-412 — The Determinant Gate

Date: 2026-11-15. Actual candidate-successor lattice Q reconstructed in RQT-401. The integer vector used as provisional position 18 has not been checked against the frozen 17-reflection predecessor.

## Exact result

Q is even; put A=Q/2, so norm -2 is v^T A v=-1. The determinant of A is a nonzero 3512-bit integer with exact valuations v_3(det A)=4 and v_1129(det A)=1.

For odd prime p not dividing det(A), A mod p is nondegenerate of dimension 3. A nondegenerate ternary form over Fp is isotropic and contains a hyperbolic plane, hence represents every nonzero target, including -1, with nonzero gradient. Hensel lifting guarantees a Z_p solution. Odd-prime local obstructions can therefore only occur at prime divisors of det(A).

The confirmed determinant primes 3 and 1129 are not obstructions: seed (0,0,1) modulo 3 lifts through 3^8; seed (1,4,15) modulo 1129 lifts through 1129^4. Each seed is regular, so the lifts continue indefinitely.

The full determinant is not factored. Other prime divisors may require checks; even local solubility at all primes does not itself yield an integer root.

## ASCII
```
          RQT-412 :: DETERMINANT GATE
      +----------------------------------+
      | ORIGINAL F4 / RANK-THREE Q       |
      +----------------+-----------------+
                       |
                    A = Q/2
                       |
                    det(A)
                 /           \
            GOOD PRIMES    BAD PRIMES
                 |           |
          automatic       3  1129  ?
          local lift      |   |    |
                 |        +---+    |
                 |        HENSEL  FACTOR
                 +-----------+-----+
                             |
                         Z_p ROOTS
                             |
                       INTEGRAL ROOT?
                             |
                         ROOT19 OPEN
```

Root19 OPEN, root20 OPEN, root21 conditional. New 3D JPG exists as a conversation artifact; the GitHub page uses ASCII.
