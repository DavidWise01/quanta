# RQT-634 — Corrected Sharp Pell Unit Recovery Exponents

## Executive result and correction

RQT-631 correctly computed the **full identity exponents** of three reduced Pell norm-one residue groups as **(6, 6, 4)**. Those exponents force every residue unit to equal `(1,0)` when powered. However, original Pell recovery from `D=s²d` only requires the coefficient of `√d` to be divisible by `s`; the first component is allowed to equal `-1` as well as `+1`.

Exhaustive exact enumeration of the same finite norm-one groups gives the smaller, **sharp recovery-only exponents**:

| s | d mod s | Residue group size | Full identity exponent | Minimal universal Y-divisibility exponent | Witness requiring this many steps |
|---:|---:|---:|---:|---:|---|
| 5 | 3 | 6 | 6 | **3** | (2,1) |
| 7 | 1 | 6 | 6 | **3** | (3,1) |
| 4 | 3 | 8 | 4 | **2** | (0,1) |

For each residue norm-one element `(x,Y)`, use exact multiplication
```
(x,Y) * (v,w) = (x v + d Y w, x w + Y v) mod s.
```
The verifier enumerates **all 6+6+8 = 20 group elements**, checks both identity orders and coefficient-divisibility exponents, and proves no smaller positive exponent uniformly gives `Y=0 mod s`. The witness table is sharp **over these finite groups**; not every abstract residue is necessarily realized by an integral norm-one unit of the huge reduced coefficients.

## Exact transfer theorem

For an actual integer reduced norm-one unit `U=x+Y√d` satisfying `x²−dY²=1`, raise it to the corresponding reduced universal exponent `E=3,3,2`. Writing `U^E=X+Y_E√d`, the coefficient satisfies `Y_E≡0 mod s`. Set `y=Y_E/s` and verify
```
X² - (s²d)y² = X²-dY_E² = 1.
```
There is no need to demand `X≡1 mod s`; `X≡-1 mod s` is equally valid.

This refinement reduces the universal transfer work by half compared with the stronger RQT-631 identity return. It **does not produce a numerical reduced unit** or determine fundamental-unit size. No generalized Pell target seed or integral norm−2 root is claimed.

## Replay evidence

The standalone Python 3 verifier `research/rqt634-sharp-recovery.py` reconstructs the three RQT-630 coefficients and all norm-one residue elements, computes all orders directly, and derives the sharp minimal recovery-only exponents. Local machine-readable certificate `RQT-634-results.json` SHA-256:
`5a4a8e7edcdd510a520e2ac50d4ff842cb3cb3d698668aa4939721f53f843e4f`.

The three square-factor reductions cover **16 of the 27 canonical unresolved orbits**. The remaining two coefficient groups have `s=1` and need no square-factor transfer.

## Honest limits and next bound

Selected-family ledger stays **82/135 excluded at all scales (60.74%), 53 unresolved**, represented by 27 sign orbits. The selected corridors do not exhaust the full lattice. No new whole-family exclusion or original 22D Wall replay. Root 19 **OPEN**.

**RQT-635:** exploit the sharpened exponents in a verified local-to-original unit construction if a concrete reduced norm-one unit can be found, while maintaining original generalized Pell target, parameter congruence, and exact integer norm gates. Do not confuse finite residue-group sharpness with the minimal exponent of an as-yet-unknown actual global unit.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
