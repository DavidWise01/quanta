# RQT-548 — Odd-Prime Bridge

**Executed exact finite-field enumeration of simultaneous successor Wall isometries**, using the historical RQT-516 and new RQT-545 4×4 Wall matrices. For each p∈{3,5,7,11,13}, enumerate the full kernel of D_new U−U D_historical modulo p; retain exactly U satisfying UᵀH_new U=H_historical mod p. Gram congruence follows from F=−H−Hᵀ. Every such U has nonzero determinant modulo p.

| Prime | Intertwiner dimension | Isometries mod p | Base isometries with at least one lift to p² |
|---:|---:|---:|---:|
| 3 | 4 | 18 | 18 |
| 5 | 6 | 48 | 24 |
| 7 | 4 | 42 | 42 |
| 11 | 4 | 120 | 120 |
| 13 | 4 | 170 | 170 |
| **Sum** | — | **398** | **374** |

Every p² lift used an exact 16-variable linearized correction and was checked directly against original big-integer Wall coefficients modulo p². The counts in the final column are **liftable base matrices**, not totals of distinct p² descendants. The prime-five kernel has dimension 6 and splits 24/24 into liftable and nonliftable first-level isometries. A single nonlifting branch is not an obstruction for the prime.

**Scope:** finite p/p² congruence existence only. No rational simultaneous Wall isometry, all-prime local certificate, integral GL₄(Z) equivalence, historical root18 transfer, or root19 is established. Root19 OPEN; full21 OPEN; selected historical 720-corridor ledger unchanged at 647 conditionally excluded/73 unresolved. Seven-level base-60 navigation preserved but not exhaustively traversed.

The exact local Python engine, detailed JSON witnesses, JPEG and embedded-image HTML are conversation artifacts. This GitHub viewer is text only; Pages deployment and JPEG upload unverified.

**RQT-549:** solve rational simultaneous Wall-isometry via the centralizer of the common successor operator, and inspect the exceptional prime-five branching at higher powers.
