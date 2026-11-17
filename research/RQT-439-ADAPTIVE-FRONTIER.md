# RQT-439 — Adaptive Rational-Seed Frontier

2026-11-16. Exact RQT-401 Gram SHA256: 5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809. Verified B^T F4 B=Q. Extend the RQT-438 rectangle using two disjoint tiles, odd positive d only. Tile A: y=1..256, d=257..511. Tile B: y=257..512, d=1..511. The RQT-438 exact integer interval yields every real-feasible integer x for fixed y,d; exact discriminant-square and z-congruence gates leave no untested possible z. Prime 13/23 hypotheses were rechecked on the frozen Gram.

Executed new counts: 98,304 pairs; 451,072 feasible x values; 50,560 prime rejections; 1,548 modular-square survivors; zero perfect squares; zero witnesses.

Together with the prior RQT-438 certificate, this excludes all primitive witnesses for positive y=1..512 and odd d=1..511, without separate bounds on x,z. Sign symmetry covers negative y. No global nonexistence claim. Root19 OPEN. Root18 ordering UNVERIFIED; root20 OPEN; root21 conditional.

```
 RQT-439 : ADAPTIVE FRONTIER
              y 1..256      y 257..512
 d 257..511   [ NEW A ]     [ NEW B ]
 d   1..255   [ RQT438]     [ NEW B ]
              98304 new pairs
              451072 feasible x
              1548 modular survivors
              0 exact squares
              ROOT19 OPEN
```

Reproduce: python research/rqt439-frontier.py RQT401_FULL.json output.json

The separate JPG and embedded-image HTML are conceptual, not independent witnesses. Next: explore a stronger exact construction or disjoint next frontier.
