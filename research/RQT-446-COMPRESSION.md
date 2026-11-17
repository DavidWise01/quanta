# RQT-446 — Sign-independent compression
2026-11-17. Set m=|f|>0. For E>=0, floor(sqrt(E)/m)=isqrt(floor(E/m²)). Thus if E=t² for t>=0 and a signed root satisfies s=L mod m, then t must be jm+r for r in {L mod m,-L mod m}. Test both squares, then retain the signed roots satisfying the original congruence. This is exact and requires no factorization of m. For E<0 reject. E=0 is handled automatically.

Executed 328820 exhaustive controls with f=1..40, L=0..f-1, E=0..400. The frozen Gram SHA matched 5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809. New disjoint tile y=769..800, positive odd d=1..767: 12288 pairs, 148608 feasible x, 447 modular survivors, 290 coupled survivors, no exact squares or witnesses. The maximum discriminant bit length among the 290 is 2444; E//f²=0 for every one. The full isqrt was also evaluated in the regression to validate compression, so no runtime speedup is claimed.

Cumulative coverage y=1..800, odd d=1..767, all x,z, conditional on previously archived coverage; negative y by simultaneous negation. Original F4 norm -2d². Root18 positional compatibility unverified. Root19 OPEN. The separately generated JPEG is conceptual, not proof.

```
RQT-446 :: COMPRESSION
          E >= 0
             |
       j = isqrt(E // m²)
             |
      +------+------+
      |             |
   jm + r       jm + (-r mod m)
      |             |
      +------+------+
             |
       exact squares
             |
       signed congruence
             |
          F4 / Wall
             |
        ROOT19 OPEN
```
Next: compress at the interval level to derive z candidates directly and test the denominator-one branch at larger heights.