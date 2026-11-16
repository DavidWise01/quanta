# RQT-429 — Certified Rational Solver

2026-11-16 | DavidWise01/quanta | original RQT-401 candidate-successor lattice

A strict exact search was executed using RQT-428's unimodular basis T*V and the full RQT-401 Gram, kernel basis B, and original F4. The script checks B^T F4 B = Q before enumerating primitive spatial vectors with max coordinate in [121,124]. For each vector it calculates N=-w'^T (TV)^T A (TV) w', applies exact square-residue filters modulo 64,63,65,11,17,19,23,31, and tests isqrt. Any prospective witness is checked against both A and original F4. The frozen predecessor reflection ordering remains unverified.

**Executed results:** 1,215,360 primitive triples; 820 nonpositive N; 1,214,540 positive N; 1,026 passing all modular-square filters; zero exact square values and zero rational witnesses.

**Careful scope:** This is a shell in T*V coordinates. RQT-426 searched radius 0..120 using T coordinates, not T*V. They are not a contiguous radius 0..124 exclusion in the same basis. No global nonexistence claim follows.

The solver includes a known elementary synthetic norm identity as a sanity check, not independent evidence for this lattice. RQT-414's nonconstructive rational-existence theorem remains in force; an explicit rational witness is open.

## ASCII

```
          RQT-429 : CERTIFIED RATIONAL SOLVER
        +-----------------------------------+
        |       ORIGINAL F4                |
        |            |                      |
        |          Q = 2A                   |
        |            |                      |
        |        T * V BASIS                |
        |            |                      |
        |     121 <= max|w'| <= 124        |
        |            |                      |
        |        1,215,360                 |
        |            |                      |
        |     MODULAR SQUARE FILTER        |
        |            |                      |
        |          1,026                   |
        |            |                      |
        |        0 EXACT ROOTS             |
        |            X                      |
        |       ROOT19 OPEN                |
        +-----------------------------------+
```

JPG generated as conceptual art; standalone embedded-image HTML is available as a conversation artifact. GitHub chapter is ASCII.

Root19 OPEN | Root20 OPEN | Root21 conditional.
