# RQT-663 — Residue-Guided Diophantine Integer Seed Search

## Executive summary

Reopened the exact original RQT-619 six-coefficient quadratic certificate (SHA-256 `97de34faf9b0163357ec3c0c81d4d1d768ffe040dc5fd5faf707ea3e8ae19021`) and tested all **27 canonical orbits** across **−100,000 ≤ t ≤ 100,000**. This is **5,400,027** possible original-parameter/orbit pairs.

The exact discriminant is `F(t)=(r1²−4r0r2)t² + 2(r1r3−2r0r4)t + r3²−4r0r5`. Necessary square classes modulo **64 and 63** form a **4,032-position residue wheel**. Enumerating only allowed arithmetic progressions passes **1,732,949** of the original parameter/orbit pairs to exact large-integer evaluation. Follow-up necessary square tests modulo **65, 17 and 19** leave **310,407** nonnegative candidates; exact integer square roots show **zero squares**. Therefore zero integer coordinates u were recoverable in the finite interval.

| Measure | Exact count |
|---|---:|
| Parameter/orbit pairs | 5,400,027 |
| Nonnegative discriminants across full interval | 5,398,223 |
| Wheel-selected parameter/orbit pairs | 1,732,949 |
| Remaining modular-square candidates | 310,407 |
| Exact square discriminants | **0** |
| Original integer `(u,t)` seeds | **0** |

**Independent consistency:** A fresh direct scan across `|t|≤20,000` exactly reproduces RQT-662's **1,078,223** nonnegative discriminants, **62,032** modular-square survivors, and zero exact squares. The new wheel enumerator uses integer arithmetic and preserves a formally exhaustive enumeration of the allowed t residue classes.

## What is and isn't proved

This is a finite negative-search certificate on the **27 original charts**. It is **not** a global Diophantine approximation theorem, an all-scale exclusion, a proof about all parameter t, or an original 22D Wall replay. The underlying source is one owned corpus; the independent scan checks computation, not independent physical ancestry.

The selected-family ledger remains **82/135 excluded at all scales (60.74%), 53 unresolved across 27 canonical orbits**. No new all-scale exclusion. **Root 19 OPEN**.

## Reproduction

- Exact Python 3 standard library: `research/rqt663.py`.
- Full per-orbit JSON results: `RQT-663-results.json` (conversation attachment).
- Results SHA256: `ca7b6909fa1821fa05f57897c4413d9f9f45a48cf367ba8fc84c9f2e4be1411e`.
- Input: original `RQT-619-results.json`; no floating point.
- New JPEG: psychedelic risograph math poster.

## RQT-664 next natural bound

Before repeating a larger brute-force range, analyze **continued-fraction and inhomogeneous Pell approximations** targeting `y²=F(t)`; measure errors to the nearest integer y without mistaking near misses for solutions. Test the complete original coordinate congruence and `G(u,t)=0` for every actual candidate.

`{{i}} · .dlw`