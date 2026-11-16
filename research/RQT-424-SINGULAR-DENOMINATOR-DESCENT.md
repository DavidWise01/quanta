# RQT-424 — The Singular Denominator Descent

Date: 2026-11-16. Conditional successor lattice from RQT-401; root18 predecessor compatibility remains unverified.

## Exact theorem

Let A=Q/2, q(w)=wᵀAw. For 3|d and q(w)+d²=0, the full Gram reduces modulo 3 to rank one, forcing x+z≡0 mod3. Set x+z=3t. The actual full matrix satisfies

A mod27 = [[8,3,14],[3,0,21],[14,21,2]].

Substitution yields q(w)/9 ≡ z²+zt+2t²+yz+2ty (mod3). In particular q(w) is divisible by 9 when x+z is divisible by 3.

If v3(d)=1, q(w)/9 must equal 2 mod3. If v3(d)≥2, q(w)/9 must equal 0 mod3. Of 216 primitive numerator classes mod9 with x+z≡0 mod3: 36 satisfy the first, 72 the second, and 108 satisfy neither.

For any surviving parent, coordinate changes by multiples of 9 do not change q modulo27, so all 27 lifts survive. Independent direct enumeration over all primitive triples modulo27 gives 972 for d=3 and 1944 for d=9, exactly 36×27 and 72×27.

## ASCII
```
         RQT-424 : SINGULAR DESCENT
      +-----------------------------+
      | q(w) + d² = 0              |
      | 3 | d, x+z = 0 (mod 3)     |
      +--------------+--------------+
                     |
               216 PARENTS
                     |
                  MOD 27
              /      |      \
             36     72      108
           v3=1    v3>=2   DEAD
             |      |        X
            972    1944
             \      /
              ROOT19 OPEN
```

This is a necessary congruence restriction at every coordinate size, not an integral existence or nonexistence proof. Some singular branches survive. No explicit rational four-vector was constructed. GitHub and any mirror of these results share one original source ancestry; the JPG is a conceptual visualization, not separate evidence.

Root19 OPEN; root20 OPEN; root21 conditional.
Next: RQT-425 — lift the surviving 3-adic branches through modulus81 and beyond.
