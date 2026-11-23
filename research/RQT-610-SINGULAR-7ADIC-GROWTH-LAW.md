# RQT-610 — Exact Singular 7-Adic Branch-Growth Law

## Executive result

For both selected families **2** and **24**, the number of ordered coordinate pairs `(u,t) mod 7^k` satisfying the exact rederived rank-four norm equation `q_F(u,ray*t+offset)+2 ≡ 0 (mod 7^k)` obeys the **all-exponent theorem**:

```
C(1) = 1
C(2) = 49
C(k) = 8 * 7^(k-1)   for every integer k >= 3.
```

The first six levels from archived RQT-609 are `[1,49,392,2744,19208,134456]` for each family, independently matched by the RQT-610 verifier. The formula covers all later levels, not merely a bounded computation.

## Exact reduction

Let `Q(u,t) = q_F(u,ray*t+offset)+2`. Its only root modulo 7 is:
- Family 2: `(u0,t0) = (1,6)`.
- Family 24: `(u0,t0) = (6,1)`.

At these roots, `Q(u0,t0) ≡ 0 (mod 49)` and both partial derivatives of Q are divisible by 7. Thus the substitution `u=u0+7x, t=t0+7y` yields **exactly**:

```
Q(u0+7x,t0+7y) = 49 P(x,y),  P ∈ Z[x,y].
```

The reduced `P mod 7`, with its monomials ordered `x²,xy,y²,x,y,1`, has coefficients:
- Family 2: `[4,1,6,0,4,4]`.
- Family 24: `[4,1,6,2,2,4]`.

**Each reduced polynomial has exactly eight zero pairs modulo 7, and its gradient is nonzero at all eight.** Thus each solution mod `7^n` has exactly seven lifts to mod `7^(n+1)` (two coordinates, one regular congruence). The number of solutions for P mod `7^n` is therefore `8·7^(n-1)`.

For k >= 3, solutions Q mod `7^k` correspond to solutions P mod `7^(k-2)` with an extra 49 choices of the final two coordinate digits. The total is:

```
49 * [8 * 7^(k-3)] = 8 * 7^(k-1).
```

At k=1 there is one root; at k=2 all 49 pairs reducing to that root solve the equation. This proves the complete piecewise law for **every** k >= 1.

## Reproduction and limitations

The executable `research/rqt610-singular-growth.py` reads archived RQT-583 equations, RQT-591 reconstructed Gram, and RQT-609 exact counts; checks exact source identities, the reduced coefficients, eight nonsingular roots for both families, and the six archived levels, then emits `RQT-610-results.json`.

This theorem **does not** produce a global integer norm−2 vector. It does not exclude families 2 or 24; it demonstrates solvability modulo all powers of 7. The 135 selected corridors do not exhaust the full rank-four lattice.

**Selected-family ledger unchanged:** 82/135 excluded (60.74%), 53 unresolved. Original 22-dimensional Wall replay not performed; nineteenth root **OPEN**.

## Next natural bound — RQT-611

Study the **7-adic solution geometry** associated with the eight regular reduced branches, including whether any full p-adic root has additional arithmetic constraints preventing a compatible integral Pell seed. Do not mistake p-adic existence for an integral solution.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
