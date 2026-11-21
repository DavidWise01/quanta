# RQT-530 — The Matched Frontier

Frozen Gram SHA256 `5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809` verified. Prior RQT-529 JSON SHA256 `2e1850066423ea91827ba736d36b7a78439008e9c3cd91fea58b628e6b696b86`.

For each of the same 73 unresolved fixed-x corridors, uniform-stratified sampling receives **the identical number of distinct integer y coordinates** as the prior seven-level adaptive search (30,245 across corridors). Compute nearest-square integer z candidates, original polynomial Q and the exact affine identity `9v²+αk²=f(Hx²−α+αQ)` for each, using identical candidate evaluation logic. Each arm has **241,960 exact identity checks**.

**Result**: Adaptive has smaller minimum sampled |Q| in all **73/73** paired corridors; uniform wins **0**. Median best-residual advantage is 10 decimal digit places (range 9–12). **Zero exact integral Q=0 roots** in either method. Uniform runtime 5.978 seconds; adaptive runtime in prior execution 6.052 seconds, not a repeatable controlled timing comparison.

**Critical limit**: Adaptive intentionally optimizes for |Q|. This performance does NOT imply better exact root discovery probability. Neither arm completely covers a corridor. Conditional 720-corridor ledger remains **647 excluded / 73 unresolved**; root19 OPEN; root18 predecessor UNVERIFIED.

Canonical geometry `{inf brace [ inf contain ( inf construct \\mix/\\match/ ) ] }^{n}`. The 7 levels are 60-fold adaptive interval subdivisions; not 60^7 exhaustive traversal.

Reproducible Python engine, full per-corridor JSON, and paper-quilling JPEG are available in conversation artifacts. This GitHub viewer is text only, not the JPEG-embedded standalone edition.

**Next RQT-531**: compare a multiresolution stratified control and optimize exact square distance; audit predecessor root18.
