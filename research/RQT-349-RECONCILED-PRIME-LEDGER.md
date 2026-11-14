# RQT-349 — Exact replay and reconciliation of original-lattice bad-prime evidence

**Executed PASS on authentic frozen F4.** 31 adjacent rational-slope ternary planes; **21 definitively excluded**, **10 unresolved** after scanning odd primes below 100,000. Original integral roots 18–21 remain OPEN.

## Reproducible source
Run `python research/rqt349-reconciled-prime-sieve.py` (SymPy). The program is **self-contained**: it reconstructs F4 directly from original `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`, checks its determinant, regenerates the RQT-348 baseline for primes 3 <= p < 20000, independently replays the three RQT-347 large-prime certificates, then scans the previously inconclusive cases for new primes 20000 <= p < 100000. It needs no uncommitted JSON input.

## Evidence ledger

| Stage | Certified excluded of 31 |
|---|---:|
| RQT-348 bounded p<20000 scan | 16 |
| Recover RQT-347 primes outside bounded range | +3 |
| RQT-349 new primes 20000<=p<100000 | +2 |
| **Total** | **21** |

New exact obstructions:

| plane slope | obstructing prime | exact basis |
|---|---:|---|
| 845/844 | 35327 | v_p(det G)=1, rank-two nonsquare quotient, singular radical Q(v)/p !=0 mod p |
| 849/848 | 38299 | same complete exact prime-square certificate |

The earlier recovered exclusions are `187/188` at `887773937`, `839/838` at `159171641`, and `840/839` at `2316121`. All original RQT-348 short-prime certificates are reconstructed and compared exactly, not simply trusted as list entries.

The **ten unresolved slopes**, after this bounded obstruction test and previous certificates, are:

```
188/189    192/193    194/195    196/197    199/200
200/201    201/202    841/840    844/843    851/850
```

A slope being unresolved **does not mean** its ternary quadratic form is rationally isotropic. The scanner uses a sufficient, not complete, local obstruction: an odd prime dividing det(G) to valuation one, with invertible leading 2x2 block, anisotropic rank-two quotient, and nonlifting radical norm. Failing to find such a prime below 100000 is not positive existence evidence.

## Detailed arithmetic and test

For each rational plane x=(-ma,b,na,c), take `G=T^T F4 T`. At prime p with v_p(detG)=1, invert upper 2x2 minor h mod p. Require its negative `-h` to be a nonsquare; this ensures all primitive mod-p null vectors lie in the radical. Construct the radical generator v=(v0,v1,1) using modular inverse and assert `Gv=0 mod p` and `Q(v)/p !=0 mod p`. The latter prevents a primitive lift modulo p². Thus a rational null vector in this plane is impossible. Every certificate can be reproduced with arbitrary-precision integers.

## Next natural target RQT-350

For the 10 unresolved slopes, test complete local conditions at the exact discriminant factors (not only small simple prime divisors), and attempt a genuine rational ternary or full-four-variable isotropic point. Only an exact vector u with u^T F4 u=0 and gcd(F4u)=1 activates RQT-334's Bézout construction for root18. Until that witness exists, roots18–21 remain OPEN. Do not conflate the three modular checks with three independent primary sources: all derive from one authentic original F4.

The 3×3×3 cubit, Josophene/Juliet, nested bracket geometry and time-angle positions are provenance/indexing metadata.
