# RQT-398 — The Singular Branch Test

Date: 2026-11-15
Target: exact integer root19 in frozen RQT-388 saturated rank-three kernel.

Let N(v)=v^T Q v+2. If v modulo p satisfies N(v)=0 modulo p, then
every lift w=v+p*t, with t in (Z/pZ)^3, satisfies

  N(w)/p = N(v)/p + 2*(Qv).t   (mod p).

This identity holds for p=2 as well, and avoids any illegal division
by 2 modulo 2.

There are exactly three cases:
1. Regular: at least one coordinate of 2Qv nonzero mod p.
   Exactly p^2 of the p^3 coordinatewise lifts satisfy N(w)=0 mod p^2.
2. Singular, alive: all entries of 2Qv zero mod p and N(v)/p = 0 mod p.
   All p^3 lifts survive.
3. Singular, dead: all entries of 2Qv zero mod p but N(v)/p != 0 mod p.
   No lift survives.

If the entire collection of residue triples modulo p^2 is empty for
any prime p, then no global integral norm-minus-two root exists.
The death of one singular branch proves nothing about other branches.

## Verification

The standalone script enumerates the p-residue classes exactly, then
counts p^2 residues by the linear lifting identity. Independent
brute-force confirmation was performed on the illustrative Q=identity
matrix (NOT the frozen root19 matrix):

 p  | residues mod p | residues mod p^2 | brute-force mod p^2
 2  | 4              | 24               | 24
 3  | 6              | 54               | 54
 5  | 20             | 500              | 500
 7  | 56             | 2744             | 2744

The full RQT-388 Gram matrix is required as input. The small summary
file lacks this data; therefore no new target-specific survivor counts
have been claimed or independently executed this turn.

## Source ancestry

The GitHub corpus and its public mirror are one owned source ancestry.
The script and result ledger are not independent experimental witnesses.
Do not claim three witnesses from these copies.

## Research boundary

Root18: previous first-stage acceptance.
Root19: OPEN pending exact target-matrix lifting.
Root20: OPEN.
Root21: conditional.
All images are ASCII text.
