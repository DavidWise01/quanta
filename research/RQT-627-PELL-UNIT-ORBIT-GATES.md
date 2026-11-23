# RQT-627 — Congruence-Preserving Generalized Pell Orbits

Source: exact RQT-626 27-orbit certificate, SHA-256 `1d901288a9a6007f79496615ef421bd0c6aa147aab1ecc33355e5ef71d4c1052`.

For each equation `z²−a y²=N` with required seed congruence `z≡h (mod a)`, a norm-one Pell unit `x²−a w²=1` acts by
```
(z,y) -> (xz+a w y, wz+x y).
```
The action preserves the norm identically. Its z-coordinate satisfies `z'≡xh (mod a)`. As every unit has `x²≡1 (mod a)`, **all even powers preserve the original z≡h (mod a) requirement**. Odd powers preserve it **if and only if**
```
a | (x-1)h
equivalently x ≡ 1 (mod a/gcd(a,h)).
```
This is a global, exact, conditional orbit theorem, not a finite-search extrapolation. It applies to any actual integer norm-one unit and any valid starting Pell solution; neither is asserted to have been constructed here.

Exact archived classification: **27 canonical orbits, 5 leading coefficient groups, 10 distinct stabilizer moduli**. Canonical family **67** satisfies `a|h`, so every odd and even unit step preserves its parameter gate. The other 26 cases have a nontrivial odd-step stabilizer modulus. All 27 target norms N remain distinct.

Reproducer: [rqt627-pell-unit-gates.py](rqt627-pell-unit-gates.py). Full local JSON certificate `RQT-627-results.json` SHA-256 `cd65fb37c79d8c4f7ef25763b4fa3e78e216498c816e621a56e67b8a17a06ae8`. It records all 27 coefficient triples, gcd stabilizers, original member IDs and evidence provenance. The algebraic theorem does not rely on numeric sampling.

Limitations: **0 fundamental units computed; 0 generalized Pell seeds computed; 0 new whole-family exclusions**. A Pell solution still requires `t=(z-h)/a` and the original integer `u` to satisfy the exact quadratic norm equation. This archive represents selected corridors, not the complete rank-four lattice. **82/135 selected families excluded all-scale (60.74%); 53 unresolved**, represented by 27 canonical orbits. Original 22D Wall NOT REPLAYED; **Root 19 OPEN**.

Next RQT-628: seek actual norm-one units and generalized Pell seeds, retain exact parity stabilizers and the original coordinate-recovery gate.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
