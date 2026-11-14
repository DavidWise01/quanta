# RQT-352 — Explicit-coordinate search on three rationally isotropic planes

**2026-11-14 | Exact bounded search: PASS; no integer witness in the tested range.** Authentic frozen symmetric F4 from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`; original integral roots 18–21 **OPEN**.

## Constructive status and scope

RQT-351 established, using exact local-global conditions and Hasse–Minkowski, that the ternary planes of slopes 194/195, 199/200, 201/202 are each isotropic over the rationals. The next task is to instantiate integer coordinates, not to retest abstract existence.

On each plane write `x=(-m*a,b,n*a,c)`, where `(a,b,c)` is integral. Let `G=T^T F4 T` be the exact ternary Gram. The lower-right 2x2 block `P=-G[1:3,1:3]` is positive definite. With `v=P^-1 G[1:3,0]` and `beta=G00+G[0,1:3] P^-1 G[1:3,0]>0`, the isotropy equation is exactly
```text
(b-v0*a,c-v1*a)^T P (b-v0*a,c-v1*a) = beta*a².
```
Cauchy–Schwarz yields the necessary and exact projected bound
```text
(b-v0*a)² <= beta*a² * (P^-1)[0,0].
```
For each integer a=1,...,1000 the verifier constructs **outward rational bounds** on b, tests the boundary inequalities exactly, then solves for c via a quadratic integer discriminant and integer square root, with no artificial cutoff on c.

## Executed ledger

| slope m/n | tested positive a | candidate (a,b) pairs | nonnegative discriminants | perfect squares | exact integer isotropic points |
|---|---|---:|---:|---:|---:|
| 194/195 | 1..1000 | 196406 | 189393 | 0 | 0 |
| 199/200 | 1..1000 | 249206 | 242207 | 0 | 0 |
| 201/202 | 1..1000 | 267470 | 260463 | 0 | 0 |
| **Total** | | **713082** | **692063** | **0** | **0** |

Negative a follows by x -> -x. At a=0, the ternary restriction becomes the negative-definite transverse form, so only the zero vector is isotropic. Hence **every nonzero integer isotropic point in these three planes must have |a|>=1001**. This is a finite-height exclusion, not a proof of global absence, and does not contradict RQT-351 rational existence.

The first full SymPy ternary diophantine solver attempt on slope 194/195 did not complete within the bounded execution window. That timeout is **not mathematical evidence of nonexistence** and is not used in the proof.

## Root-chain status

No actual integral isotropic u was constructed. Therefore neither `gcd(F4u)=1` nor the RQT-334 Bézout construction of exact root18 can yet be evaluated on a witness. The original exact roots18–21 and full Wall completion remain OPEN. Earlier 25/31 rational-slope obstructions remain distinct certificates and are not replaced by this result.

## Executable evidence

`research/rqt352-explicit-isotropic-height1000.py` is the GitHub stand-alone exact verifier. Local executed source: `/mnt/data/rqt352_explicit_bounded.py`; actual execution output: `/mnt/data/rqt352_bounded_result.json`.

## RQT-353 next natural target

Improve the constructive conic solver rather than merely raising the integer height: use controlled rational diagonalization, LLL/ideal reduction, or certified quaternion splitting to construct a rational point on one of the three known-solvable ternary quadrics; then primitive-normalize and test actual exact F4 norm, pairing divisibility, parity, rank drop, and Wall completion. No modular approximate witness may be promoted to an exact root.

The 3x3x3 nested cubit, Josophene/Juliet, brace-box-toroid, and time-angle addresses are research/provenance metadata, not mathematical witnesses.
