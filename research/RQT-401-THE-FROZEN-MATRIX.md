# RQT-401 — The Frozen Matrix Test

Date: 2026-11-15. Canonical visual medium: ASCII.

## What was actually executed

The original integral RQT-386 norm-minus-two vector was reconstructed
from the published primitive null vector and exact Bezout/parity method.
Its F4 norm -2 and H4 self-pairing 1 were checked.

A saturated rank-three kernel was built for the successor Wall equation,
followed by exact integer LLL reduction. The reduced basis has maximum
coordinate bit-length 644, matching RQT-388. Full reduced Gram Q max bit
length: 1353.

The local congruence condition v^T Q v = -2 (mod m) was enumerated
for every triple modulo m, with exact Python integers.

| modulus | survivor triples |
|---|---:|
| 2 | 8 |
| 4 | 32 |
| 8 | 192 |
| 16 | 768 |
| 32 | 3072 |
| 64 | 12288 |
| 5 | 20 |
| 7 | 42 |
| 9 | 162 |

Counts at 5,7,8,9 reproduce the prior RQT-388 record. The new 2-adic
counts demonstrate no total obstruction through 64. This is not an
all-level 2-adic proof or an integer root19 witness.

SHA256 of JSON-compact string-valued reduced Gram:
5f4f49b1d75d60d61961b8a0aede915707f6c5cf11e1a9d7e71f1d3a7d83c809

## Reproduction

Run research/rqt401-frozen-matrix.py, with canonical RQT-386,
RQT-377 and RQT-388 scripts present and SymPy installed.
The optional --out path writes the FULL basis and Gram matrix, not
merely the compact certificate. Run the RQT-394/395/398/400 validators
against the generated full kernel with field restricted_Gram.

## Important conditionality

The RQT-386 authentic norm-minus-two vector has not yet been certified
as reflection position 18 of the original frozen 17-reflection product.
Thus this is the exact successor lattice *conditional on that choice*.
No position-specific frozen root19 or later reflection is claimed.

Root19 OPEN; root20 OPEN; root21 conditional.
The repository chapter and all diagrams are ASCII only.
