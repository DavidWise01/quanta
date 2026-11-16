# RQT-408 — The Cone–Residue Intersection

Date: 2026-11-15. Research corpus: DavidWise01/quanta, original F4.

## Input facts

RQT-394 exact necessary real cone (for integer solutions to the frozen
candidate successor norm equation):
  177065/100000 < x/y < 178600/100000.

RQT-407 exact local projection of A(v)=-1 (A=Q/2) modulo 256:
14336 of 65536 xy residue pairs are locally admissible.

## New global theorem: cone does not remove entire congruence classes

For any prescribed rx,ry modulo 256, let
 y=16896+ry+256*k with integer k>=0.
 L=floor(177065*y/100000)+1, the first integer strictly above
 the cone's left endpoint.
 x=L+((rx-L) mod 256).

The interval for x is open and has length
  (178600-177065)*y/100000 = 1535*y/100000.
For y>=16896 this is >256, so any 256-consecutive integers after
the lower bound fit strictly inside the cone. Therefore x has
the prescribed residue rx modulo 256 and obeys both exact slope
inequalities. Every xy residue pair has infinitely many lifts
at unbounded positive coordinate sizes.

All 65536 possible rx,ry were independently checked with Python
integer arithmetic at y between 16896 and 17151, and again after
adding 256 to y. In particular, every one of the 14336 RQT-407
admissible pairs can occur in the real cone.

This is a compatibility theorem, NOT an exact solution of Q(v)=-2.
One still needs a square discriminant, an integral third coordinate,
and original Wall pairing and root ordering checks.

## Source lineage and scope

The RQT-407 residue mask and RQT-394 cone are derived from the
same RQT-401 candidate successor lattice. These are not independent
source ancestries. The status of the provisional 18th reflection
relative to the original frozen predecessor remains unverified.

Root19 OPEN; root20 OPEN; root21 conditional.
The next target is an arithmetic global integer representation
algorithm, rather than widening a periodic modular cone scan.
