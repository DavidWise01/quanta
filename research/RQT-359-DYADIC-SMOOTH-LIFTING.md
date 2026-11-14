# RQT-359 — Smooth 2-adic null sheets and exact 64-bit local branches

**Status (2026-11-14):** Exact dyadic classification and local construction **PASS**; no exact global integral norm-zero coordinates, original roots 18–21 **OPEN**.

## Provenance
Authentic original RQT-242 frozen Gram F4, determinant checked. Two ternary planes with slopes 194/195 and 201/202, using the exact unimodular reduced coordinate matrices from RQT-355. RQT-351 proved rational isotropy globally and RQT-353A proved divisibility-one for any primitive integral norm-zero vector on either plane. RQT-357/RQT-358 norm equations remain equivalent only with full image-lattice membership enforced. This result uses original reduced ternary coordinates directly and does **not** drop those membership gates.

## Exact calculation and induction
Let `T(a,b,c)=(-ma,b,na,c)`, let the appropriate unimodular V give `z=(z0,z1,z2)`, and define `A=V.T*T.T*F4*T*V`. Since A has even diagonal, `q(z)=z.T*A*z/2` is integer-valued and its first finite difference is
```text
q(z+2^k*w) = q(z) + 2^k*(A*z)^T*w + 2^(2k)*q(w).
```
Modulo 2^(k+1), the last term vanishes for k>=1. Thus if `A*z` has an odd entry, exactly four of the eight binary digit triples w preserve q=0 mod2^(k+1).

For **each** plane, the primitive mod2 null residues are:
```text
smooth:   010, 011, 110, 111
singular: 101
```
The singular residue 101 has `A*z=0 mod2` and `q(z)=2 mod4` for **every** lift to modulo4, and hence cannot occur in any 2-adic isotropic vector. The four smooth classes each lift through every precision. Consequently **every primitive 2-adic null vector has z1 odd**, and at every k>=2 the number of primitive null residues mod2^k is **exactly 4^k**.

| k | 2^k | primitive null residues |
|---|---:|---:|
| 1 | 2 | 5 (four smooth, one singular that dies) |
| 2 | 4 | 16 |
| 3 | 8 | 64 |
| 4 | 16 | 256 |
| 5 | 32 | 1,024 |

The explicit finite census has been run for k<=5 on both planes and matches the induction. For k>=2, every odd height `h=z1 mod2^k` occurs in exactly **2^(k+1)** primitive null residues. These counts concern *residues*, not distinct rational or integer global solutions.

## Two constructed compatible local branches
The executed program chooses `z=(0,1,0)` initially, fixes h=1, and at every step k=1,...,63 tries all four bit pairs for z0,z2. Exactly **two** work each time. It publishes exact `z mod2^64` and the corresponding original `u=T*V*z mod2^64`, verifying `q(z)=u.T*F4*u/2=0 mod2^64`. The exact integer norms of these finite representatives are **not zero**. They are finite-precision 2-adic witnesses, not exact integer null vectors or roots.

## Consequence and next target

RQT-359 replaces an unexplained finite parity observation with a proof of **smooth dyadic continuation at all precisions**, plus a deterministic branch constructor. It does *not* solve the full global norm equation, the RQT-358 large-index image-lattice constraint, or the explicit integral root18 construction.

RQT-360 should construct an exact rational point by certified quadratic-form/ideal descent or search a reduced compatible lattice with independent archimedean and local constraints, then verify `u.T*F4*u=0` and `gcd(F4u)=1` directly. Until a globally exact integer witness exists, roots18–21 remain OPEN.

3x3x3 tensor, Josophene/Juliet, braces, and time-angle address metadata remain provenance indexing, not mathematical proof.
