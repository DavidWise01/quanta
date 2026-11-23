# RQT-602 — Compressed CRT Wheel and 200-Million-Parameter Pell Sieve

## Exact result
Source: archived `RQT-595-results.json` (SHA256 `5e68fddb78395b02f5cc4f6cbdd5c4c3cfc341b1ed036d86174175b9e7aee699`) and `RQT-601-results.json` (SHA256 `c1105a199d980f713aa28983ae9d4e75ee77b719bb848e729da62658b777c76e`).

The original RQT-601 26-prime residue sets were recomputed independently from exact `Δ(t)=At²+Bt+C`. The first four primes `31,29,7,17` yield a compressed Chinese-remainder wheel of modulus

```
M = 31*29*7*17 = 106981
admissible residues = 1*14*4*9 = 504
SHA256(comma-separated decimal residues in increasing order)
  dafdc839f5493ca45468404f876b063b4c823b675903352495941eca685be7bf
```

The wheel selects just `504/106981 ≈ 0.4711%` of integer parameter residues. An arithmetic-progression enumerator finds all of them without stepping through every integer.

## Independent regression
- Replayed the interval `-1,000,000 ≤ t ≤ 1,000,000`.
- Exactly **9423** wheel candidates after four primes, matching RQT-601.
- Later gates reduced the candidates to **0 at prime 103**, matching RQT-601.

## Extended interval
- `-100,000,000 ≤ t ≤ 100,000,000` — **200,000,001 integer parameter values**.
- **942,225** initial wheel candidates.
- Sequential prime filters (19,23,5,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113) left **one** candidate:
  `t = 78,589,011`.
- For this t, `Δ(t)=552885633593481542107431486419241210758602953467680` is not an integer square. More compactly, `Δ(t) ≡ 66 (mod 137)`, which is a quadratic nonresidue. Adding the **27th prime gate, 137**, eliminates this final t.
- **Zero candidates survive 27 modular gates** in the extended exact finite interval. No integer square-root checks or coordinate-recovery candidates are needed for this exclusion.

## Status and limitations
This is a **finite, exact exclusion certificate for a single selected family**, not a global theorem. Solutions can occur outside the interval, and the selected corridors do not exhaust the rank-four lattice.

The selected-family ledger is unchanged: **82/135 all-scale excluded (60.74%), 53 unresolved**. No integral norm−2 root found, no original 22D Wall replay, Root19 OPEN.

## Next natural bound — RQT-603
Lift the CRT wheel into a bidirectional expanding search with a rolling immutable certificate and independently recomputed residue-sets. Avoid equating huge finite bounds with a global proof. Consider targeting the remaining 53 families and seeking genuinely global local obstructions or generalized Pell seeds rather than simply increasing the finite window indefinitely.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
