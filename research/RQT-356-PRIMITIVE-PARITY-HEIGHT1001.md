# RQT-356 — Exact primitive-height parity and reduced null search through 1001

**Status:** Certified finite exclusion and parity restriction on the original frozen F4. **No explicit integer isotropic vector or original root18–21 constructed.**

## Authentic ancestry

F4 comes from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`. RQT-351 proved rational isotropy exists in the ternary planes of slopes `194/195`, `201/202`. RQT-353A proved any primitive integer null vector there has pairing divisibility one. RQT-355 supplied unimodular ternary transformations V and excluded reduced heights `1<=|z1|<=250`. The present script recomputes the authentic F4 determinant and the exact transformed Gram `A=V^T T^T F4 T V` directly, without a synthetic bridge.

## New primitive parity theorem

For each plane, enumerate all `4^3=64` ternary residues `z=(z0,z1,z2)` mod4, retain primitive residues (at least one odd coordinate) and `q_A(z)=z^T A z/2 = 0 mod4`. Exactly **16 primitive null residues survive per plane**, and every one has **z1 odd**. An exact null vector must satisfy the same congruence, so any **primitive integer isotropic vector has z1 odd**.

A nonprimitive integer null vector, if present, divides by its coordinate gcd to give a primitive integer null vector (V is unimodular). Its primitive height is no larger than the original absolute height. This justifies using only odd primitive heights to exclude *all* nonzero integer null vectors within a finite height bound.

## Exact extended finite search

For a fixed positive odd `h=z1`, the `(z0,z2)` block `P=-A[[0,2],[0,2]]` is positive definite. Define `v=P^-1 A[[0,2],1]` and `beta=A11+A[1,[0,2]] P^-1 A[[0,2],1]`. Completing the square gives
```text
(z_perp-h*v)^T P (z_perp-h*v) = beta*h².
```
The exact projected inequality `(z0-h*v0)^2 <= beta*h²*(P^-1)00` yields a finite outward rational range on z0. Every integer z0 in it is checked. For each, solve for z2 using the exact integer quadratic discriminant and perfect-square test; there is **no arbitrary bound on z2**.

The script exhaustively checks every odd positive h in `251,253,...,1001`; negative h follows by central symmetry. Even h cannot belong to a primitive isotropic vector by the new mod4 gate.

| Plane | New (h,z0) pairs | Nonnegative discriminants | Perfect-square discriminants |
|---|---:|---:|---:|
| 194/195 | 1,711,654 | 1,709,013 | 0 |
| 201/202 | 1,383,028 | 1,380,396 | 0 |
| **Total** | **3,094,682** | **3,089,409** | **0** |

Combining with RQT-355's separately executed height 1..250 exclusion and the mod4 primitive parity result gives the new necessary height
```text
|z1| >= 1003
```
for every primitive integer null vector in either plane. Because every nonzero integer null vector has a primitive integer divisor with no larger height, there is also no nonzero integer null vector with `|z1|<=1002` in either plane.

## Reproduce and limits

GitHub: `research/rqt356-primitive-parity-height1001.py`. Local executed source: `/mnt/data/rqt356_parity_scan.py`, local execution transcript: `/mnt/data/rqt356_execution.txt`. All calculations exact (SymPy matrices, Python Fraction, integer isqrt), and explicit matching counts asserted.

The earlier RQT-351 rational-existence theorem is not contradicted; its first primitive integral witness may be at much larger height. No rational-point coordinates, Bézout root18 or full Wall completion appears in RQT-356. Original integral roots18–21 remain **OPEN**.

## Next RQT-357

Prefer a certified constructive ternary isotropy algorithm or algebraic norm-equation solver on the now-reduced Gram. Use this mod4 parity gate to exclude impossible branches in any future search. If explicit primitive coordinates emerge, check the exact original norm, RQT-353A pairing divisibility, permitted root18 parity, successor rank/order, and six RQT-257 Wall equations.

The nested 3x3x3 cubit, brace-box-toroid, Josophene/Juliet and time-angle fields are search lineage metadata, not mathematical witness substitutes.
