# RQT-442 — Valuation Kernel

For nonzero E=p^v u with unit u, E is a square in Z_p iff v is even and u is a square unit. For p=2 the unit criterion is u=1 mod 8; for p=3 it is u=1 mod 3; for p=5 it is u=1 or 4 mod 5. Zero passes. These criteria cover all prime-power depths, but simultaneous local square status at finitely many primes does not prove an integer square.

Executed exhaustive finite residue regression: 12458 cases. Actual RQT-401 fingerprint 5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809, original F4 backmap verified. Old tile: 773376 feasible x, 1262 finite survivors, then 1254,1231,1230. New disjoint tile y=513..640, odd d=1..767: 435456 feasible x, 793 finite survivors, then 791,779,778. Zero exact squares in both tiles. Combined coverage y=1..640, odd d=1..767, all x,z. Sign symmetry covers negative y. No global nonexistence claim. Original F4 witness must have norm -2d². Root19 OPEN; root18 prefix unverified.

```
{{ g0 g1 g2 }}
   2 | 3 | 5
       |
 even valuations + unit tests
       |
 2055 -> 2045 -> 2010 -> 2008
       |
 0 exact squares
 ROOT19 OPEN
```

Next: classify denominator-compatible residues using the original quadratic congruence, not square status alone.