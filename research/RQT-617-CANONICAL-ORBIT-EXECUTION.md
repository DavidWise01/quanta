# RQT-617 — Canonical Orbit Execution and Local Gradient Structure

## Exact execution
Reopened RQT-616 27-job ledger, RQT-591 rederived 4×4 Gram, and the original RQT-583 80-equation archive. Checked the RQT-616 chain tip `6b365ada55f5e44881707b73b764814afbf6dc00e1d05affda4103ea2b229cd7` and RQT-583 source SHA256 `5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92`.

Exactly **27 canonical orbits** covering **53 unresolved family IDs** were tested. For each, independently reconstructed the full binary quadratic integer norm in (u,t) from the reduced Gram and verified its discriminant identity at signed t-values. Complete finite scan on `-100000 ≤ t ≤ 100000` yielded **zero square discriminants** across **5,400,027 canonical job–parameter pairs**. This is a finite bound only, with mirror partners inherited by exact sign symmetry, not independent tests.

## New structural classification
For each canonical norm polynomial Q(u,t), enumerated all coordinate pairs modulo primes
`2,3,5,7,11,13,17,19,23,29,31`. Classified each modular root as regular when either partial derivative of Q is nonzero modulo p, singular otherwise.

- At **p=2**, **all 27** canonical orbits have modular roots but **none is regular**.
- At **p=3,5,11,13,17,19,23,29**, **all 27/27** have at least one regular root.
- At **p=7**, **26/27** have a regular root; **canonical family 2**, paired with family 24, has only a singular modular root (one).
- At **p=31**, **26/27** have a regular root; **canonical family 28**, paired with family 52, has only a singular modular root (one).

For every regular root, a deterministic coordinate-derivative Hensel construction was independently checked to **p^5** using exact arithmetic. This proves local compatibility through those moduli, not a global integer vector.

## Provenance and files
Complete reproducible script: `research/rqt617-canonical-local-gates.py`.
Full results certificate: `RQT-617-results.json` (locally generated SHA256 `396ed165bd78fdada25c7737f7dcd637c07d3fa15c92ff051d3bb48f8c462648`).
All 27 records include original family IDs, exact local root counts, regular/singular classes, and finite square hits.

## Honest limits
No new all-scale family exclusion. Ledger **82/135 selected families excluded (60.74%); 53 unresolved represented by 27 canonical orbits**. The 135 selected corridors do not exhaust the rank-four lattice. Original 22D Wall replay has not been performed. Root 19 **OPEN**.

## Next natural bound — RQT-618
Analyze the special **singular-only p=31 family-28 orbit** and universal mod-2 singularity of the 27 canonical quadratic forms, retaining *all* branches rather than assuming regular Hensel lifting at those primes. Seek a genuine all-scale structural obstruction or integer seed; do not infer either from finite tests.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
