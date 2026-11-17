# RQT-440 — Generational Residue Engine

Date: 2026-11-16. Canonical RQT-401 Gram SHA256: 5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809.

With E=alpha*x²+2Kxy+gamma*y²+delta*d², square-residue feasibility mod m depends only on (x,y,d) mod m. For m=16,9,25, build a compact bitset indexed by (y mod m,d mod m), with bit (x mod m) set exactly when E mod m is a quadratic residue. These tables are lossless necessary gates.

The checker replays all three already-covered RQT-438/439 tiles from the exact RQT-401 Gram and verifies the original F4 backmap. It verifies that historical counts remain unchanged under the old eight-modulus filter before applying an extra mod25 filter:

| Tile | Earlier survivors | With mod25 | Exact squares |
|---|---:|---:|---:|
| Old | 223 | 154 | 0 |
| A | 213 | 143 | 0 |
| B | 1335 | 954 | 0 |
| Total | 1771 | 1251 | 0 |

515,584 real-feasible integer x values were covered for 131,072 positive (y,d) pairs. The extra modulus25 removes 520 prior candidates, or 29.36% of survivors. Mod9 did not reduce the candidates further after mod16 within this frontier. Results do not show global nonexistence.

```
RQT-440 :: GENERATIONAL RESIDUE ENGINE
         RQT-401 Gram
              |
        g0 [16 mask]
              |
        g1 [ 9 mask]
              |
        g2 [25 mask]
              |
     legacy eight moduli
              |
        integer isqrt
              |
        original F4
              |
       ROOT19 : OPEN
 old 1771 -> new 1251 -> 0 squares
```

Root19 OPEN; root20 OPEN; root21 conditional. Frozen position18 compatibility UNVERIFIED. The JPG is conceptual art, not a root witness. Next step: recursive residue-mask expansion to new disjoint frontier tiles, or a constructive isotropic vector solver.
