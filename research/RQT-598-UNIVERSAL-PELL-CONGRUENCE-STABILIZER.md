# RQT-598 — Universal Integral-Pell Congruence Stabilizer

## Exact result (family 28)

For RQT-597's squarefree Pell parameter `d=3580734425344222227352852171253793`, set `M=2A=179036721267211111367642608562689650`. The necessary original-coordinate gates are `X ≡ B (mod M)` and `Z ≡ 0 (mod 10)`. Since `M` is divisible by 10, identity modulo M stabilizes both simultaneously.

The exact factorization, supported by RQT-597's recursive prime certificate, is

```
M = 2 × 3 × 5² × 13 × 1693 × 54231366340197528698151546659
```

For any *integral* norm-one unit `x+z sqrt(d)` with `x²-dz²=1`, multiplication acts by
```
T = [[x,dz],[z,x]] ∈ SL₂(Z).
```

For each prime power `p^k | M`, the finite group has order `|SL₂(Z/p^k Z)|=p^(3k−2)(p²−1)`. By Lagrange's theorem, `T` raised to this local group order is identity modulo `p^k`. By the Chinese remainder theorem, the least common multiple of all local group orders, `E`, satisfies `T^E ≡ I (mod M)` for every possible integral norm-one unit.

**Exact universal exponent (97 digits):**
```
2495428846376980414842976695320325076410511060575086680674879676418181949822869503902337202645000
```

Local group orders for p=2,3,5,13,1693 and the large prime are respectively 6, 24, 15000, 2184, 4852557864, and 159496677051283848789993089073041986534578777267482551001415764409064584666352111922520.

**Verified computational gates:** independently checked recursive Pratt certificate from RQT-597, exact factorization of M, group-order formulas, computed lcm E, and modular exponent checks on standard nontrivial SL₂ generators.

**Limits:** This is a *conditional, all-scale stabilizer theorem*, **not** an explicit nontrivial integral Pell unit, generalized Pell seed, or original norm−2 root. It does not construct the nineteenth root. No original 22D Wall replay. The ledger remains **82/135 selected families excluded (60.74%), 53 unresolved**. The 135 selected corridors do not exhaust the rank-four lattice.

**Next natural bound RQT-599:** Determine a concrete integral norm-one unit (possibly enormous) via exact continued-fraction period or verified infrastructure method; then find a generalized Pell seed and test coordinate recovery. Do not mistake a universal exponent or congruence preservation for the existence of a seed.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
