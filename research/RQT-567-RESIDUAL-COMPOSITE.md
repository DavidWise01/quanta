# RQT-567 — Residual Composite Gate

**Exact new result:** the RQT-566 259-bit fixed-discriminant cofactor
`555654409826629710119829271213958080091261217263858828861644919996120497288591`
is **proven composite**. The base-2 strong probable-prime test fails: `n−1=2·d` (`s=1`) and `pow(2,d,n)` is neither 1 nor n−1. Bases 3,5,7,11,13,17,19 also fail. These are rigorous compositeness witnesses, not factors.

**Completed bounded exact ECM work (all negative):**
| batch | B1 | B2 | configured curves | seed | factor |
|---|---:|---:|---:|---:|---|
| A | 7000 | 70000 | 16 | 56701 | none |
| B | 16000 | 160000 | 16 | 56702 | none |
| C | 35000 | 350000 | 16 | 56703 | none |
| D | 80000 | 800000 | 32 | 56704 | none |

Total **80 curves completed**, no divisor found. A search nonfinding cannot prove primality or minimum factor size. Exact prior 293-bit source multiplication rechecked. The 259-bit number remains unfactored, so its unknown prime factors and associated local relative-norm conditions remain unresolved.

**Global rational norm OPEN; rational Wall isometry OPEN; integral GL4 bridge OPEN; root19 OPEN; full21 OPEN.** Historical selected 720-corridor conditional ledger unchanged: 647 excluded, 73 unresolved; zero new exclusions.

Downloadable local artifacts: exact Python engine, JSON base-2 residues and work ledger, warm parchment crystal-observatory JPEG, and standalone HTML with its embedded JPEG. The GitHub HTML viewer is text only, and GitHub Pages/JPEG repository upload are unverified.

**Next RQT-568:** targeted factor recovery or exact number-field obstruction without complete discriminant factorization.
