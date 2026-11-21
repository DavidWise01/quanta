# RQT-554 — Six Discriminant Gates

**Exact executed local norm audit at six odd primes dividing the reciprocal fixed-field discriminant:** 7, 29, 89, 1063, 18149, 27179. Exact coefficients and characteristic polynomial taken from canonical RQT-550 output SHA256 `3af3b6e48f8006e529e6136ec74dc5e3f8f5e07c1e44e515d58ef1902778d5d0`.

For each p: `v_p(Δ)=1`, so the unique F-place is ramified over Q_p, and `K=A/2 mod p`. Direct exact rational modular evaluation gives nonzero `δ=K²−4` and `C=a+bK`. The relative L/F algebra is split when δ is square and unramified quadratic when δ is nonsquare. In both cases unit C⁻¹ is a norm at every p-adic order.

| p | K mod p | δ mod p | C mod p | relative L/F | norm |
|---:|---:|---:|---:|---|---|
| 7 | 6 | 4 | 1 | split | PASS |
| 29 | 4 | 12 | 1 | unramified quadratic | PASS |
| 89 | 74 | 43 | 77 | unramified quadratic | PASS |
| 1063 | 872 | 335 | 35 | unramified quadratic | PASS |
| 18149 | 113 | 12765 | 5146 | split | PASS |
| 27179 | 16216 | 1827 | 4329 | split | PASS |

For split places, a simple square root of δ lifts by Hensel, and the norm is surjective; for unramified quadratic places, the local norm map is surjective on units. All tests derived from exact integers/rationals, with Legendre and square-root assertions and no numerical rounding. Thus **six all-order local relative norm certificates**, but **no global rational norm solution**. The unfactored discriminant and target numerator/denominator cofactors remain outside the audit.

Rational Wall isometry OPEN; integral GL4 bridge OPEN; root19 OPEN and full21 OPEN. No root19 exclusion. Historical selected 720-corridor ledger unchanged at 647 conditionally excluded / 73 unresolved. Seven-level base-60 WAKAKU geometry is a navigation frame, not an exhaustive search.

RQT-554 local Python script, full JSON certificates, new ice-crystal neon JPEG and standalone HTML with embedded JPEG exist as conversation artifacts. This committed GitHub page is a text viewer; GitHub Pages and binary upload remain unverified.

**Next RQT-555:** investigate remaining cofactor places and global cyclic-relative-norm obstructions, then construct a rational isometry if representable.
