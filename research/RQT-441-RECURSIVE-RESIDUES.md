# RQT-441 — Recursive Residue Generations
Exact RQT-401 Gram fingerprint 5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809 and original F4 backmap verified. For each prime p in 2,3,5, the square residues at p^(k+1) project onto those at p^k. The executed checker enumerates the residue sets and verifies this projection identity. It adds mod4096,243,3125 to the RQT-440 baseline gates, then uses exact integer square roots. This is a hierarchy of residue sets, not a claim of a separate independent witness or a complete rational solver.

Regression: 515584 feasible x, 1251 baseline survivors, 1198 after4096, 927 after243, 852 after3125, zero exact squares. New disjoint tile y=1..512 and odd d=513..767: 65536 pairs, 257792 feasible x, 603 baseline survivors, 573 after4096, 442 after243, 410 after3125, zero exact squares. Combined 592 additional removals. Complete rectangle y=1..512, odd d=1..767, all x,z. Sign symmetry covers negative y. No global nonexistence claim.

```
RQT-441 :: {{ g0 g1 g2 }}
  2^8 -> 2^12 | 3^2 -> 3^5 | 5^2 -> 5^5
  1854 -> 1771 -> 1369 -> 1262 -> 0 squares
  ROOT19 OPEN
```

Original F4 backmap norm for a candidate is -2d², while homogeneous norm is zero. Conceptual JPG labels the latter in its F4 panel; the certificate is authoritative. Root19 OPEN; position18 UNVERIFIED; root20 OPEN; root21 conditional. Next: use residue valuation criteria to avoid enumerating larger tables and expand the numerator frontier.