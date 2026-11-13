# RQT-331 — Authentic eighteenth-root modular sieve

**Status: exact finite congruence enumeration PASS, genuine integral root18 OPEN.** All data come from the original frozen branch, not the synthetic bridge lattice.

## Source and transformed coordinates
Original `F4,H4`: [stoicheion RQT-242 verifier](https://github.com/DavidWise01/stoicheion/blob/main/research/rqt/rqt242_mod4_audit.py). Original unimodular reduction `T`, reduced Gram `J=T F4 T^T`: [RQT-254](https://github.com/DavidWise01/stoicheion/blob/main/research/rqt/RQT-254-unimodular-second-height.md).

The exact transform has `det T=-1` and `x=T^T y`. Its inverse yields `y0=-24*x0-22*x1-17*x2-17*x3`. Root parities in original x coordinates are exactly 0111, 1001, 1110.

## Complete residue-lift counts
Enumerate all reduced-coordinate residues y modulo m with original x parity in the three eligible classes and `y^T J y ≡ -2 (mod 2m)`. Each accepted residue at modulus m is lifted to all 16 children at modulus 2m and tested modulo 4m, with no branches omitted.

| y modulus | norm modulus | retained y residues | each original parity |
| ---: | ---: | ---: | ---: |
| 2 | 4 | 3 | 1 |
| 4 | 8 | 24 | 8 |
| 8 | 16 | 192 | 64 |
| 16 | 32 | 1,536 | 512 |
| 32 | 64 | 12,288 | 4,096 |
| 64 | 128 | 98,304 | 32,768 |

The script independently verifies unimodularity, original Gram determinant and frozen-source matrix anchors, and each complete lift census. This is a local **2-adic necessary-condition sieve**, not a proof of an integral root. Existence of p-adic solutions at 2 alone does not imply any global integral vector with exact norm -2.

## Height exclusion
The separately published RQT-254 exhaustive 33,614,572-pair discriminant audit claims no norm -2 vector with `|y0|<=1000`. RQT-331 imports this **as earlier source evidence**; it does not rerun that large computation. The next global search begins at `|y0|>=1001` if that earlier certificate is accepted.

## Lessons, next bound
- Original norm -2 and first parity 0111, 1001, 1110 remain the decisive gate. A genuine root then automatically drops the rational moving rank 4→3; RQT-256 shows that its binary order changes 3→2.
- No exact root18, roots19–21, or 21-word product has yet been produced.
- RQT-332: use the true reduced Gram and certified Schur/discriminant bounds to test a finite y0 interval **above 1000**, and use modular residues for branch-and-bound pruning. State precisely which interval is exhaustive.

## Evidence routing
The 3×3×3 nested cubit with 1 center, 6 faces, 12 edges and 8 corners is address metadata for the search. Josophene {{j}}, Juliet {{n}}, and {brace[box(toroid)]} time/angular addresses are not independent mathematical witnesses. Preserve exact source ancestry and append-only results.
