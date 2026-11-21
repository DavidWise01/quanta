# RQT-533 — The Pareto Seed Frontier

**Executed:** 73 conditional fixed-x corridors; **30,245** distinct integer positions; **241,960** exact affine identity checks; **zero integral roots**, zero new complete exclusions. Frozen Gram SHA256: `5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809`. RQT-532 source JSON SHA256: `54535343cab4d4bd1c2a6f895dec52a0a2c9f1dd24544fcc1b269b038ab1482f`.

Algorithm: seven recursive base-60 interval refinements, sampling at most 60 positions per depth across up to two active subintervals. At each level retain up to two distinct nondominated sampled seeds, extreme on minimized |Q| and exact discriminant square-distance. Deterministic 60-base low-discrepancy fill preserves previous per-corridor exact candidate budgets. Every candidate is an original integer (x,y,z) tested through the exact affine identity. Total time 5.662 s, single execution.

| Comparison | Pareto wins | Other wins | Ties |
|---|---:|---:|---:|
| Square-distance vs adaptive | 39 | 30 | 4 |
| Square-distance vs RQT-532 hybrid | 33 | 38 | 2 |
| Square-distance vs uniform | 55 | 14 | 4 |
| |Q| vs adaptive | 0 | 73 | 0 |
| |Q| vs RQT-532 hybrid | 36 | 37 | 0 |

Conditional 720-corridor ledger unchanged: 647 excluded in prior bounded searches/necessary-condition checks; **73 unresolved**. ROOT19 OPEN. **Root18 predecessor remains UNVERIFIED**; searches for `RQT-401 root 18 certificate` and `RQT-386 18th root integral` in `DavidWise01/quanta` surfaced no matching file results, not a proof of absence.

These are finite, different-footprint sampled comparisons, not complete corridor searches or proof of existence/nonexistence. Seven 60-fold levels do not exhaust all 60^7 addresses. Canonical geometry: `{inf brace [ inf contain (inf construct \\mix/\\match/ ) ] }^n`.

Next: RQT-534 — root-18 provenance and constructive root certificate audit. Full reproducible script, JSON, JPEG and self-contained embedded-JPG HTML are available as conversation artifacts; GitHub page is a text edition. GitHub Pages deployment is not independently confirmed.
