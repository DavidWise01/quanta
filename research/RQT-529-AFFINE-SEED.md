# RQT-529 — Affine Seed Navigator

**Exact numerical test completed.** Frozen conditional Gram SHA256 `5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809` checked against RQT-520 coefficients. RQT-523's 73 unresolved fixed-x corridors used.

Original quadratic `Q=a*x²+2bxy+g*y²+2cxz+2eyz+fz²+1`. Exact norm: `9v²+αk²=f(Hx²−α)`, with `v=αy−βx`, `k=cx+ey+fz`, `α=(fg−e²)/9`, `β=(ce−fb)/9`, `H=((ce−fb)²+(fg−e²)(c²−fa))/(9f)`. Defect: `9v²+αk²=f(Hx²−α+αQ)`. Every sampled candidate is an integer (x,y,z) and every identity checked exactly.

**Implemented:** for each of 73 complete discriminant-feasible y intervals, seven levels of 60-cell base-60 adaptive sampling. At each level select the cell with minimum exact |Q| after nearest-square integer z reconstructions. **30,245 distinct integer (x,y) points**, **241,960 exact integer identity checks**, **zero Q=0 witnesses**, **zero additional complete corridor exclusions**, runtime 6.052 s. Some deep cells contain fewer than 60 distinct integer points, correctly deduplicated.

**Important limitation:** adaptive sampling is *not* exhaustive of any of the 73 fixed-x corridors; no global representation or root exists from these results. The ledger remains 647 conditionally excluded of 720 selected corridors and 73 unresolved. Root19 OPEN; root18 predecessor UNVERIFIED.

Canonical recursive geometry: `{inf brace [ inf contain ( inf construct \\mix/\\match/ ) ] }^{n}`; the seven levels use real 60-fold interval subdivisions. The angular address space of size 60^7 was not exhaustively traversed.

**Next RQT-530:** matched-budget comparison of adaptive versus stratified sampling and independent root18 predecessor certificate. Reproducible script, all 73 exact results, high-resolution JPEG, and self-contained JPEG-embedded HTML were created as conversation artifacts, but are not included as binary media in this commit.
