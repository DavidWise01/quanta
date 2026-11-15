# RQT-404 — Indefinite Ternary Bridge: Integer Cone Sieve

Date: 2026-11-15. Images: ASCII always; JPG if available separately.

## Exact candidate-successor calculation

The actual rank-three restricted F4 Gram was read from the locally
preserved RQT-401 full certificate. The exact RQT-394 cone was enforced:

  177065/100000 < x/y < 178600/100000, y != 0.

For positive y from 1 to 30,000, all admissible x were enumerated
with integer arithmetic. Negative y is covered by (x,y,z) ->(-x,-y,-z).
The quadratic in z is tested by its exact discriminant

  D=(Q02*x+Q12*y)^2
    -Q22*(Q00*x*x+2Q01*x*y+Q11*y*y+2).

A modular sieve rejected nonsquares modulo 64,63,65,11,13,17,19,23.
Only remaining candidates required math.isqrt. This sieve is lossless:
every exact square belongs to every modular square residue set.

## Actual local execution results

All pairs checked: 6,907,699
Nonnegative discriminant: 6,902,493
Passed square sieve modulo 64: 2,588,464
Passed then 63: 1,320,629
Passed then 65: 633,910
Passed then 11: 314,279
Passed then 13: 314,279
Passed then 17: 156,570
Passed then 19: 86,354
Passed then 23: 86,354
Exact square discriminants among survivors: 0
Exact integer root19 vectors found: 0

This is a rigorous finite-coordinate exclusion in the fixed basis, NOT
a global proof, and not a complete ternary quadratic representation
algorithm. There can still be an integer root at much larger coordinates.

## Provenance and open gate

The RQT-386 original norm-minus-two vector is genuine but its
compatibility with the frozen 17-reflection prefix is still unknown.
Therefore this lattice is conditional as the true position-19 successor.

Root19 OPEN; root20 OPEN; root21 conditional.

Next research target: exact rational isotropic-vector construction,
indefinite reduction, or rigorous local-global obstruction, rather
than merely increasing max_y repeatedly.
