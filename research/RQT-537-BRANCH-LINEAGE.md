# RQT-537 — Original Root Lineage: Branch Integrity

**New exact finding:** the previously compared RQT-224 *initial* sixteenth root and RQT-241 seventeenth root are from **different frozen branches**. RQT-241 explicitly follows the *alternative Branch-2 sixteenth root* (rank-six coordinates `(-232,-246,223,729,-473,-242)`), not the initial RQT-224 root16 `(-183,-198,174,572,-368,-188)`.

Both original 22-dimensional integer vectors were independently tested against the actual Stoicheion original 22×22 Gram and X:
- `r16^T G r16 = r17^T G r17 = -2`;
- `r16^T G h = r17^T G h = 0`;
- reflections are integral involutions preserving G and h;
- `r16^T G r17 = -4251928517663716544520`; span rank 2.

Compute the **original one-sided Wall form** on the published rank-21 h-perp lattice K: `GK=K^T G K`, `X K=K Y`, `H=GK (Y-I)^{-1}`. Check `H+H^T=-GK` exactly. The mixed-branch pair has:

- `H(r17,r16) = 307135354231451946557` (NOT zero);
- `H(r16,r17) = 3944793163432264597963`;
- their sum equals `-r16^T G r17 = 4251928517663716544520`.

**Therefore the mixed RQT-224 initial root16 / Branch-2 root17 pair is NOT an ordered Wall-compatible pair.** This does **NOT** invalidate the published RQT-241 Branch-2 17-root chain; it identifies a branch ancestry substitution that the reconstruction must avoid. Correct Branch-2 ambient root16 is not yet recovered; its known rank-six coordinates must be transported through the original RQT-216 basis, then rechecked before claiming the complete original 17×17 Wall chain.

**Statuses:** root18 FIRST-STAGE PASS on published Branch-2 frozen F4/H4; root19 OPEN; full 21-word OPEN. Prior conditional 720-corridor ledger unchanged (647 excluded, 73 unresolved). No new root19 exclusions.

**Sources:** [RQT-224](https://github.com/DavidWise01/stoicheion/blob/main/research/rqt/RQT-224-sixteenth-integral-wall-root.md), [RQT-236](https://github.com/DavidWise01/stoicheion/blob/main/research/rqt/RQT-236-branch2-first-root-gate.md), [RQT-241](https://github.com/DavidWise01/stoicheion/blob/main/research/rqt/RQT-241-explicit-seventeenth-root.md), [original Gram/X](https://github.com/DavidWise01/stoicheion/tree/main/research/rqt/source).

WAKAKU: a new orbital 17-gate technical diorama with 7-level sexagesimal instrument. Actual JPEG and standalone embedded-JPEG HTML are conversation artifacts; this GitHub page is a text edition. **Next RQT-538: recover Branch-2 ambient root16 and audit its correct one-sided Wall pairing.**
