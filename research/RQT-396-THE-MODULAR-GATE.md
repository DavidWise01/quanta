# RQT-396 — The Modular Gate

Date: 2026-11-15.
Parent checkpoint: RQT-394 real cone and RQT-395 integer discriminant gate.
Target: exact original F4 root19, after orthogonality is encoded in the saturated RQT-388 rank-three lattice.

## Exact inherited local counts

The RQT-388 certificate recorded the following number of residue triples
(x,y,z) modulo m satisfying vᵀQv ≡ -2 (mod m):

| m | surviving residue triples |
|---|---:|
| 5 | 20 |
| 7 | 42 |
| 8 | 192 |
| 9 | 162 |

These four moduli are pairwise coprime. By coordinatewise CRT, exactly
20*42*192*162 = 26,127,360 residue triples modulo
5*7*8*9 = 2520 satisfy the corresponding four modular conditions.
This does NOT yield 26,127,360 genuine norm-minus-two roots.

## New inference: CRT and the real cone do not collide

For every residue pair (rx,ry) mod 2520, integer lifts x,y in that residue
class can meet 177065/100000 < x/y < 178600/100000 with arbitrarily large
positive y. For fixed y sufficiently large, the interval of allowable x
has length (178600-177065)*y/100000 > 2520, and therefore contains an
x in every residue class modulo 2520. Choose y in the desired residue
class and large enough. The z residue can be lifted independently.

Hence the open cone *alone* does not eliminate any CRT residue triple.
Additional exact square/divisibility, size-sensitive, or new local
obstructions are necessary to advance the global root19 question.

## Reproducibility

Run research/rqt388-exact-second-key.py --out FULL.json to obtain the full
reduced Gram; then run research/rqt396-modular-gate.py FULL.json. It
checks local counts and CRT-product consistency with exact integer arithmetic.
The small RQT-388-results.json summary does NOT contain the full Gram.

## Scope

This result is a conditional derivation from the published RQT-388
verified residue counts. No new global root19 existence/nonexistence
theorem follows, and this document does not represent a fresh execution
of the Python verifier. Root19 OPEN, root20 OPEN, root21 conditional.
No image files required: ASCII illustration is the canonical visual.
