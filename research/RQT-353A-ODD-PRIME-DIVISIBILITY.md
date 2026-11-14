# RQT-353A — Complete divisibility-one proof for two genuine isotropic planes

**Exact corrected theorem (2026-11-14).** This is the normative addendum to RQT-353. The initial parity-only suggestion that all three planes automatically had gcd(Fu)=1 was too strong. The mod8 enumeration alone establishes **odd** gcd, not gcd=1. An independent odd-prime audit now proves gcd=1 for **two** planes, leaving a 3-primary caveat for the third.

## Frozen source
Authentic RQT-242 F4, RQT-351 Hasse–Minkowski proof of rational isotropy for the planes 194/195, 199/200 and 201/202, and RQT-334 Bézout construction and accepted first-root parity gate. No synthetic bridge or invented integer vector.

## Exact theorem and proof

Given coprime (m,n), let `T(a,b,c)=(-ma,b,na,c)`. The map T preserves primitive content: since gcd(m,n)=1, gcd(Tt)=gcd(t). A nonzero rational isotropic point exists in each of the three planes by the previously replayed RQT-351 theorem. Clearing denominators and dividing by gcd produces a primitive integral null vector `u=Tt`.

For a primitive integer `u`, the integer pairing divisibility `d=gcd(F4u)` divides `|det(F4)|`: use `adj(F4)F4u=det(F4)u` and gcd(u)=1. The exact determinant factorization is

```text
|det F4|=2² * 3² * 4966811
             * 140001169580740529
             * 330823854880640721967014002817981344723960683.
```

RQT-353 exhaustively checked all primitive mod8 null ternary residues on each plane; all 64 per plane have `F4u != 0 mod2`. Thus `2∤d`.

For each odd prime p dividing det(F4), test the 4×3 matrix `F4*T` modulo p. If it has full column rank 3, `F4u=0 modp` implies t=0 modp, contradicting primitive t. Hence `p∤d`.

## Exact rank census

| plane | p=3 | p=4966811 | p=140001169580740529 | p=330823854880640721967014002817981344723960683 |
|---|---:|---:|---:|---:|
| **194/195** | 3 | 3 | 3 | 3 |
| **199/200** | **2** | 3 | 3 | 3 |
| **201/202** | 3 | 3 | 3 | 3 |

Therefore **EVERY primitive integral isotropic u in plane 194/195 or 201/202 has d=1**. For the 199/200 plane, only a possible power of 3 remains; the same universal conclusion is not established by this proof. The local null congruence mod 9 can allow the 3-primary class, so claiming it impossible would be incorrect.

Because RQT-351 proves primitive integral null vectors exist in both fully certified planes, RQT-334's exact Bézout normalization can construct a primitive integer root of norm -2 in an accepted first-root parity (one of `0111,1001,1110`). This is an **existence theorem**, not an explicit coordinate realization and **not** the remaining three-root Wall completion.

## Execution evidence

`research/rqt353a-odd-prime-divisibility.py` recomputes all 192 primitive null residues mod8 and all 12 odd-prime rank tests from original F4, with exact arbitrary-precision modular elimination. Local executed copies: `/mnt/data/rqt353a_global_divisibility_audit.py`, `/mnt/data/rqt353a_audit_result.json`. RQT-351's own original local-global verifier was separately replayed successfully in this turn. No root coordinates are asserted.

## RQT-354 next target

Construct explicit integral isotropic coordinates in plane **194/195** or **201/202**, where d=1 is guaranteed for any primitive null vector, using an exact conic/ternary solver; verify actual coordinates and apply exact Bézout reflection, rank/order tests and downstream RQT-257 Wall orthogonality. The third plane's 3-primary issue can be investigated independently.

**Original explicit root18 and roots19–21 OPEN.** The nested 3×3×3 cubit, Josophene/Juliet and time-angle fields remain evidence provenance metadata.
