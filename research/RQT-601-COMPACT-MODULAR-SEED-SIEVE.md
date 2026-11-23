# RQT-601 — Compact Modular Seed Sieve (Family 28)

## Verified exact finite certificate

Using the archived RQT-595 family-28 Pell coefficients (SHA-256 `5e68fddb78395b02f5cc4f6cbdd5c4c3cfc341b1ed036d86174175b9e7aee699`), define the exact discriminant
```
Δ(t) = A*t² + B*t + C
A = 89518360633605555683821304281344825
B = -7483520243911231029085168265101895934
C = -64071240985594466694007969119178624871
```
Every integer solution in this selected ray-offset family requires that Δ(t) be a nonnegative perfect square, and hence a quadratic residue modulo every prime. We tested all integer parameters `-1000000 <= t <= 1000000` (2,000,001 integers) using 26 exact prime-residue gates: 31,29,7,17,19,23,5,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113.

The first gate, modulo 31, has exactly one admissible residue: **t ≡ 12 (mod 31)**. It leaves 64,516 integer candidates in the finite window. Successive gates reduce candidates to 31,146, 17,800, 9,423, 4,964, 2,814, 1,697, 915, 494, 259, 132, 68, 39, 17, 7, 2, 1, and **zero by prime 103** (the remaining gates preserve zero). No exact square candidates survive.

The method discards a t **only** if Δ(t) fails to be a quadratic residue for at least one tested prime; therefore it is an exact negative certificate for the complete stated finite interval. It does not require an explicit gigantic fundamental Pell unit.

## Scope / limitations
This is a **finite exact exclusion**, not an all-scale family obstruction. The previous selected-family exclusion ledger remains **82/135 (60.74%), 53 unresolved**. A solution beyond the window remains possible; selected corridors do not exhaust the 4D lattice. No generalized Pell seed or integer norm−2 vector found. No original 22D Wall replay; Root19 OPEN.

RQT-600's independent lower bound of 417,976 decimal digits for the fundamental Pell y-coordinate remains unchanged and is not needed for this sieve.

## RQT-602 natural bound
Turn the residue filter into a compact CRT wheel certificate: calculate its combined modulus, produce an independently replayable surviving-residue progression, then test a much wider window with exact integer arithmetic. Never promote a finite window nonfinding to global exclusion without a complete modular obstruction.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
