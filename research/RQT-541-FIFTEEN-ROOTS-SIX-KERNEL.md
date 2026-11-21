# RQT-541 — Fifteen Roots, Six-Dimensional Kernel

**Executed: exact original 22D source replay.** Reproduced the **historical RQT-198 index-64 basis B in original column order** using the algorithm in `research/rqt/rqt198_wall_integral_lattice.py` and original Stoicheion G/X text files. B has det 64; BᵀWB has determinant 1. This resolves the prior RQT-540 ambiguity about alternative index-64 bases.

Recovered the published fifteen 21-coordinate root vectors from Stoicheion RQT-201, RQT-203, RQT-204, RQT-205, RQT-207 through RQT-215. The fifteen columns T satisfy, **in exact integer arithmetic**:

- `rank(T)=15`.
- `J15=Tᵀ H T` is upper-unitriangular: all diagonal entries 1 and every strictly lower entry zero.
- `Tᵀ Q T=−J15−J15ᵀ`; all fifteen roots have Gram norm −2.
- All fifteen original 22D ambient vectors `K B T` are orthogonal to h and have norm −2.
- Original ambient root15 matches the RQT-215 published 22D vector exactly.

Constructed the **saturated** 21×6 integer kernel `N` of the fifteen lower-Wall equations using iterative unimodular extended-GCD column elimination, not rational nullspace rounding. Hence `Tᵀ Hᵀ N=0`, `rank N=6`, and `F6=Nᵀ Q N` has exact determinant:

`−313982794406122741723132503868`.

This independently reproduces the Stoicheion RQT-216 restricted Gram determinant from original 22D sources and full fifteen-root ancestry.

**Important boundary:** Our saturated N is a valid 6D integer basis, but the published Branch-2 root16 coordinates `(-232,-246,223,729,-473,-242)` are expressed in historical RQT-216's *different reduced basis*. We have NOT certified a change-of-basis to that convention; do not multiply those coefficients by N. Authentic Branch-2 ambient root16 and its one-sided Wall pairing with root17 remain PENDING. No new root19 witness/exclusion. Root18 first-stage PASS, root19 OPEN, full21-word OPEN. Historical conditional sample remains 647 excluded / 73 unresolved of 720.

**Reproducible conversation artifacts:** `rqt541.py`, `historical_index64_basis.json`, `historical_root15_coordinates.json`, `ambient_root15.json`, `saturated_rank6_basis.json`, `rank6_gram.json`, `results.json`, original new WAKAKU JPEG, and JPEG-embedded HTML. This GitHub version is the research-text edition; GitHub Pages and binary image publication unverified.

**Next RQT-542:** identify historical 6D basis change and transport correct Branch-2 root16; alternatively derive one using complete ambient Wall constraints, but do not conflate it with the historical coordinate witness. Canonical geometry: `{inf brace [ inf contain ( inf construct \\mix/\\match/ ) ] }^{n}`; seven-level base-60 frame retained, not sampled this turn.

Sources: [Stoicheion RQT-198](https://github.com/DavidWise01/stoicheion/blob/main/research/rqt/rqt198_wall_integral_lattice.py), [RQT-201](https://github.com/DavidWise01/stoicheion/blob/main/research/rqt/RQT-201-integral-root-chain.md), [RQT-216](https://github.com/DavidWise01/stoicheion/blob/main/research/rqt/RQT-216-rank-six-Wall-boundary.md), [RQT-224](https://github.com/DavidWise01/stoicheion/blob/main/research/rqt/RQT-224-sixteenth-integral-wall-root.md).