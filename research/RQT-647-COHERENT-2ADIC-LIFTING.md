# RQT-647 — Coherent 2-Adic Lifting Trees

## Exact result

Reopened RQT-619 original integer quadratic norm coefficients, RQT-626 generalized Pell data, and RQT-646 exact recovery projections. Ran an **exact coherent pair-level 2-adic lifting test** on the ten canonical orbits sharpened by integer-coordinate recovery:
`28,31,34,37,55,61,64,67,109,112`.

For each canonical orbit, a complete pair `(t,y) mod m` is admissible when
```
y² ≡ a t²+2ht+c     (mod m)
y ≡ ±(r1*t+r3)      (mod gcd(m, |2r0|)).
```
Each admissible pair mod m has four possible children mod 2m:
`(t+αm,y+βm)`, for `α,β∈{0,1}`. Recheck **both** equations for every child. Merely having some allowable t residue is insufficient to establish a coherent lifted pair.

| m | Coherent (t,y) pairs across 10 orbits | Projected t residues |
|---:|---:|---:|
| 16 | 560 | 160 |
| 32 | 640 | 160 |
| 64 | 1,280 | 320 |
| 128 | 2,560 | 640 |
| 256 | 5,120 | 1,280 |
| 512 | 10,240 | 2,560 |
| 1,024 | **20,480** | **5,120** |

For every transition in this finite tree, each parent pair has either **0 children** or **4 children**. No parent at these precisions has exactly 1, 2, or 3 children.

| Transition | Parent pairs terminated | Parents lifting with four children |
|---|---:|---:|
| 16→32 | 400 | 160 |
| 32→64 | 320 | 320 |
| 64→128 | 640 | 640 |
| 128→256 | 1,280 | 1,280 |
| 256→512 | 2,560 | 2,560 |
| 512→1,024 | 5,120 | 5,120 |

**Cross-check:** for all ten orbits and every overlapping modulus 16–256, the directly enumerated pair count and projected t count exactly match the existing RQT-646 certificate. Every higher pair reduces to its admissible unique lower pair.

## Scope and evidence

- Reproducible Python 3 (standard library): `research/rqt647-paired-lifting.py`.
- Full certificate including every orbit and parent-degree histogram: `research/RQT-647-results.json`.
- Local SHA-256: `3445b6a6376bb59dc7c1135b67b15e75a52b80614f3fc7510ade9b81d115260a`.
- The continuing branches have been checked **only to finite modulus 1,024**. The experiment does **not** prove an infinite 2-adic path, an ordinary integer solution, or a generalized Pell seed.
- These ten orbits are part of the original **27 canonical unresolved sign-orbits**, representing 53 original selected family IDs.

**Ledger unchanged:** 82/135 selected families excluded at all scales (60.74%); 53 unresolved; no new full-family exclusion. Original 22D Wall not replayed. **Root 19 OPEN.**

## Next natural bound — RQT-648

Test whether the repeated 0-or-4 branch pattern can be established algebraically from 2-adic valuations of the exact coefficients; distinguish a verified finite depth from a truly proven indefinite lift. Compare all 27 orbits before making claims about the whole selected corpus.

`{brace{n}[box[n](torroid(n))]} · {{i}} · .dlw`
