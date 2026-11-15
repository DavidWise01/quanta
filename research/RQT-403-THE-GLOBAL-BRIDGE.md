# RQT-403 — The Global Integer Bridge

2026-11-15. Fixed candidate-successor lattice of the original F4.
Canonical visuals: ASCII text only.

## Exact actual-Gram computation

Loaded the full RQT-401 rank-three reduced Gram and evaluated:
Q(v) = v^T Q v = -2.

For each of seventeen odd primes p=3,5,7,11,13,17,19,23,29,31,
37,41,43,47,53,59,61, enumerated every residue triple modulo p.
The exact surviving class counts (all regular, no singular) are:

|p|3|5|7|11|13|17|19|23|29|31|37|41|43|47|53|59|61|
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
|count|18|20|42|110|156|272|380|506|870|930|1406|1722|1806|2162|2862|3540|3660|

Every tested prime has a regular solution. Regular Hensel lifting thus
certifies the existence of p-adic norm-minus-two vectors for EACH
of the listed odd primes, beyond any finite prime-power depth.

This is not proof for all odd primes or for the global integers.

## Exact finite integral discriminant gate

With (x,y) in the strict proven RQT-394 corridor and 1<=y<=5000:
  checked pairs                 191908
  nonnegative D                 191769
  perfect-square D              0
  integer z constructed         0

This is an actual run against the full successor Gram, not a synthetic
quadratic form. Simultaneous sign reversal covers negative y with the
same bound, but no unbounded nonexistence result follows.

## Root ordering and provenance

The source Gram arises from RQT-386's exact norm-minus-two root
candidate in the frozen F4 matrix, followed by its saturated Wall
kernel and RQT-388's exact LLL reduction. Its compatibility with the
actual frozen 17-reflection product (hence identity as the
position-specific root18) remains unverified. GitHub and public
mirrors of the same corpus are one original witness ancestry.

## Next

Seek a globally constructive representation of norm-minus-two, or
proof of global integral obstruction, using indefinite ternary
quadratic arithmetic. Avoid conflating local solvability with integer
existence. Root19 OPEN; root20 OPEN; root21 conditional.
