# RQT-628 — Actual Pell Unit Search and Exact Denominator Bounds

## Verified computation
The exact RQT-627 27-orbit Pell-unit certificate was reopened and its SHA-256 independently checked:
`cd65fb37c79d8c4f7ef25763b4fa3e78e216498c816e621a56e67b8a17a06ae8`.

There are five distinct positive nonsquare leading coefficients `a`, with 27 distinct generalized Pell targets `N`. For **each a**, the first **10,000 simple continued-fraction convergents** of `sqrt(a)` were constructed from exact integer recurrences:
```
m_(n+1) = d_n a_n - m_n
d_(n+1) = (a-m_(n+1)^2)/d_n
a_(n+1) = floor((floor(sqrt(a))+m_(n+1))/d_(n+1))
p_n=a_n p_(n-1)+p_(n-2)
q_n=a_n q_(n-1)+q_(n-2)
```
All 50,000 convergent pairs were directly checked against `p_n²-a q_n²`. **None equals +1 or −1**. The first 10,000 convergents per group are therefore excluded as Pell units.

Because a nontrivial integer solution to `x²-a y²=1`, with `y>0`, must be a continued-fraction convergent of `sqrt(a)`, every such unit has **y greater than the denominator of convergent index 9,999**. This is a certified lower bound, *not* a proof that the fundamental unit does not exist. The full integer denominators have approximately 17,000 bits; rather than truncating their decimal digits, the certificate records exact bit lengths and SHA-256 digests of unsigned big-endian byte representations.

| Coefficient a (exact) | Canonical orbits | q_9999 bits |
|---|---:|---:|
| 89518360633605555683821304281344825 | 9 | 17017 |
| 149561530769640628300862186866588569 | 3 | 17202 |
| 158134758925461363207454619257200752 | 4 | 17050 |
| 865181362726903603566834179921037649 | 8 | 17220 |
| 1957113882671124377864756294075131977 | 3 | 16962 |

## Generalized Pell diagnostic
For each of the 27 distinct targets `N`, the explicit parameter-seed line `z=a t+h` was checked for **−1000 ≤ t ≤ 1000**, using the exact necessary square condition `y²=a t²+2ht+c`. **No square hits** were found. This is a finite diagnostic only and does not exclude seeds outside this parameter interval or in other Pell residue classes.

## Reproducibility
- Standalone Python 3 script: `research/rqt628-unit-search.py` (inputs: RQT-627 JSON, RQT-626 JSON, output JSON).
- Local exact result: `RQT-628-results.json`, SHA-256 `f83082dd9e106a9e1bad0c43eac2d8a4608650b1a658c98fa69cd8e2c4f49b83`.
- Source artifacts and all five coefficient groups remain tied to their original orbit IDs.
- **Zero fundamental units found, zero generalized Pell seeds found, zero original integer norm−2 roots recovered.**

## Mathematical scope
This computation offers five rigorous denominator lower bounds and bounded nonfindings, but **not a fundamental-unit certificate or global Pell obstruction**. An integer solution still requires the parameter congruence `z≡h (mod a)` and exact recovery of the original integer coordinate u from Q(u,t)=0.

Selected-family ledger remains **82/135 excluded at all scales (60.74%), 53 unresolved**, represented by 27 canonical orbits. The selected corridors do not exhaust the entire rank-four lattice. Original 22D Wall NOT REPLAYED. **Root 19 OPEN**.

## Next natural bound — RQT-629
Rather than indefinitely scanning continued fractions, derive rigorous period or regulator bounds, or seek a compact verified unit via subfield/factorization structure. Separate the proof of unit existence from the more difficult search for generalized Pell norm targets and integral norm−2 coordinates.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`