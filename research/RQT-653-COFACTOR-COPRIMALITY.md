# RQT-653 — Cofactor Coprimality & Integer Recovery Boundary

RQT-652's complete exact certificate was independently replayed (input SHA256 `2cd1ccf0119ea4f09617657cbb0e58351cb7812e8661e1109bd03b822da4e72a`).

For each of the **54 residual discriminant/determinant entries**, extract `R=2^v q` with q odd. The exact audit confirms **31 distinct odd cofactors**, a total valuation sum **82** (counting repeated records), and **465/465 pairwise gcd tests equal to 1** among distinct q values. Every original integer was reconstructed by exact multiplication of RQT-652's recorded factors and the residual, and each odd q was checked against every odd prime ≤100,000.

This is a **pairwise-coprime partition**, not primality proof: the 31 odd numbers may themselves be composite. The remaining factorization work is not complete; no new local prime-orbit case or ordinary integer norm−2 root is claimed.

## Evidence

- Reproducer: `research/rqt653-cofactor-coprimality.py`; input `research/RQT-652-results.json` is available as the downloadable RQT-652 certificate in the conversation, and full exact RQT-653 output is downloadable as well.
- Full local result SHA256: `cf3e28b3eacb5214a99f381609ecf5ed21b0a4f56bf7ebd01132ac0be7602627`.
- New all-scale family exclusions: **0**. Existing ledger: **82/135 excluded (60.74%); 53 unresolved across 27 canonical orbits**. Original 22D Wall NOT REPLAYED. **Root 19 OPEN**.

## RQT-654

Prioritize certifications for the 31 pairwise-coprime odd residuals. Admit a new factor only with exact divisibility verification, or a primality claim only with a genuine certificate. Preserve original global norm and integer-coordinate checks.

`{brace{n}[box[n](torroid(n))]} · {{i}} · .dlw`
