# RQT-538 — Branch-2 Transport Gate

**Executed original 22D verification:** original Stoicheion 22×22 Gram and operator source pass exact symmetry/isometry and fixed-vector checks. Reconstructed integral 21D Wall form from these sources. The published RQT-224 *initial* root16 and RQT-241 *Branch-2* root17 each have original Gram norm −2, but **their mixed-branch one-sided Wall pairing is nonzero**:

`H(r17, r16_initial) = 307135354231451946557 ≠ 0`.

**Correct lineage:** RQT-241 continues the alternative RQT-224 **Branch-2** rank-six root16:
`c_B2=(-232,-246,223,729,-473,-242)`.
The initial RQT-224 rank-six root is `c_initial=(-183,-198,174,572,-368,-188)`. Only the latter's ambient 22-coordinate image was recovered in the currently accessible published summary.

**Missing original input:** authentic 22×6 saturated rank-six transport matrix `T` (referred to in RQT-216/RQT-224 evidence bundles). It was not located in the inspected Stoicheion/Quanta public Git trees or the targeted conversation/Library search. A single known equation `T*c_initial=r16_initial` does **not** determine `T*c_B2`. No branch-2 ambient root16 or genuine Branch-2 root16–17 Wall pairing is asserted.

**New strict validation algorithm (local executable attached):** take 22×6 integral `T`, assert rank=6 and its initial witness transport, construct `r16_B2=T*c_B2`, check original 22D norm −2, h-orthogonality, integral reflection, and compute `H(r17,r16_B2)` using original Gram/X. Accept only if that pairing equals zero. Without `T`, return PENDING.

**Root18 first-stage PASS on the published frozen Branch-2 F4/H4; complete original 17-root ambient Wall replay PENDING; root19 OPEN; full 21-word OPEN.** Conditional selected-corridor ledger unchanged: 647 excluded, 73 unresolved of 720; zero new exclusions. Seven-level base-60 WAKAKU cross retained as navigation, not exhaustively traversed.

Sources: [RQT-216](https://github.com/DavidWise01/stoicheion/blob/main/research/rqt/RQT-216-rank-six-Wall-boundary.md), [RQT-224](https://github.com/DavidWise01/stoicheion/blob/main/research/rqt/RQT-224-sixteenth-integral-wall-root.md), [RQT-236](https://github.com/DavidWise01/stoicheion/blob/main/research/rqt/RQT-236-branch2-first-root-gate.md), [RQT-241](https://github.com/DavidWise01/stoicheion/blob/main/research/rqt/RQT-241-explicit-seventeenth-root.md), [Quanta RQT-537](https://github.com/DavidWise01/quanta/blob/main/research/RQT-537-BRANCH-LINEAGE.md).

**Next RQT-539:** recover the full 6D→22D transport from RQT-198/215/216 ancestor basis matrices, then verify the *correct* Branch-2 root16 and its one-sided Wall pairing. Local complete verifier, exact JSON, JPEG and self-contained JPEG-embedded HTML are conversation artifacts. GitHub HTML is text edition; Pages unverified.
