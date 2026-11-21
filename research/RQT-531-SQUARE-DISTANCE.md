# RQT-531 — The Square-Distance Trial

Exact frozen Gram SHA256 `5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809`. RQT-529 source JSON SHA256 `2e1850066423ea91827ba736d36b7a78439008e9c3cd91fea58b628e6b696b86`; RQT-530 JSON SHA256 `2accafe5094fac67584dbbec201a336ea13ae53247ec229f038443be9263a364`.

**Critical measurement correction:** RQT-529's `best_square_distance` measures distance only at the best |Q| point, not the global minimum within its sampled path. Replayed every adaptive path from its original algorithm; all 73 corridor counts, level sample counts and best |Q| reproduced. Measured true minimum exact integer discriminant-square distance `min(D-isqrt(D)^2,(isqrt(D)+1)^2-D)` over all sampled y. New control uses deterministic 60-base radical-inverse multiresolution coordinates (centered first seed), nonadaptive and with **the same per-corridor number of unique y values as both prior methods**: 30,245 positions per method.

**Three-way outright wins across 73 corridors:** adaptive **44**, multiresolution **14**, uniform **11**, tie **4**. Paired multires vs adaptive: 14/54/5 (multi/adaptive/tie). Multires vs uniform: 38/31/4. New arm and adaptive replay underwent 483,920 exact affine-identity checks (241,960 each); zero integral Q=0 hits, zero new corridor exclusions. Executed 11.533 s for both new arm and replay. These results correct the objective-specific interpretation: adaptive's 73/73 |Q| advantage from RQT-530 must NOT be reused as a claim about square distance.

Search is bounded and not exhaustive. Selected-sample ledger remains 647/720 conditional fixed-x corridors excluded, 73 unresolved. Root19 OPEN, root18 predecessor UNVERIFIED. Seven-level base-60 seeded cross is the navigation frame, not full 60^7 traversal.

Canonical: `{inf brace [ inf contain ( inf construct \\mix/\\match/ ) ] }^{n}`.

**Next RQT-532**: equal-budget hybrid refinement using explicit |Q| and square-distance objectives and independent root18 predecessor audit.

Reproducible Python, exact 73-corridor JSON, JPEG and embedded JPEG HTML are downloadable conversation artifacts; committed HTML is text only.
