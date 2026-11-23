# RQT-629 — Pell Period Bounds and Norm−1 Obstructions

## Certified arithmetic

Input: RQT-628 exact five-group certificate, SHA-256 `f83082dd9e106a9e1bad0c43eac2d8a4608650b1a658c98fa69cd8e2c4f49b83`.

For each of the five nonsquare leading coefficients D, the integer continued-fraction recurrence for sqrt(D) was evaluated for **1,000,000 period states**. None reached its canonical period-ending state `(m,d,a_n)=(floor(sqrt D),1,2floor(sqrt D))`. Therefore all five continued-fraction periods have length **greater than 1,000,000**. This is a rigorous finite period lower bound, not a completed period, regulator, or fundamental-unit calculation. Unlike RQT-628's convergent test, these five million iterations test *period states*, not huge convergent numerator/denominator pairs.

## Four global norm−1 unit obstructions

A hypothetical integer solution to `x²−D y²=−1` is impossible when D is divisible by 3, because it would require `x²≡2 (mod 3)`. It is also impossible when D is divisible by 4, because it would require `x²≡3 (mod 4)`.

- Group 1, D=`89518360633605555683821304281344825`: impossible modulo 3.
- Group 2, D=`149561530769640628300862186866588569`: impossible modulo 3.
- Group 3, D=`158134758925461363207454619257200752`: impossible modulo 4.
- Group 4, D=`865181362726903603566834179921037649`: no obstruction from these tests; remains open.
- Group 5, D=`1957113882671124377864756294075131977`: impossible modulo 3.

The norm−1 obstruction is **all-scale** for those four equations. It does not exclude norm+1 units, the distinct 27 generalized Pell norm targets N, or integer norm−2 roots.

## Evidence and status

Exact verifier: `research/rqt629-period-obstructions.py`.
Full local certificate: `RQT-629-results.json`, SHA256 `541ef9b84851ff1fe87d746369e4dd05a269ce7b6c8382be707aa190218989ec`.

No actual norm+1 fundamental unit, generalized Pell seed, or original integer norm−2 root constructed. Selected-family classification remains **82/135 excluded (60.74%), 53 unresolved**, represented by 27 canonical sign-orbits; the selected corridors do not exhaust the full lattice. Original 22D Wall replay **NOT PERFORMED**. **Root 19 OPEN.**

## RQT-630

Investigate square-factor reductions and congruence-preserving unit construction without mistaking period-search bounds or negative unit obstructions for generalized Pell family exclusions.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
