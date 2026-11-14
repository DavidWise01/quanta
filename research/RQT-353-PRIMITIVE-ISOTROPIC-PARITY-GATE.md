# RQT-353 — Primitive isotropic vectors automatically have pairing divisibility one

**Status (2026-11-14): Exact finite mod-8 theorem verified and upstream RQT-351 verifier independently replayed. Explicit coordinates for original root18 and roots19–21 remain OPEN.**

## Frozen source and logical ancestry

The authentic RQT-242 even integral symmetric Gram `F4` is embedded verbatim from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`. RQT-351 proves by Hasse–Minkowski that the three ternary rational planes with slopes `194/195`, `199/200` and `201/202` contain a nonzero rational null vector. This is an **existence theorem**, not a coordinate witness. RQT-334 proves the exact Bézout normalization from a primitive null vector of pairing divisibility one to a norm-minus-two root in a permitted first-root parity class.

## New exact theorem and certificate

For `m/n` one of these three coprime slopes, let
```
T = [[-m,0,0],[0,1,0],[n,0,0],[0,0,1]]
u=T*(a,b,c)=(-m*a,b,n*a,c).
```
Because gcd(m,n)=1, a primitive integral ternary triple `(a,b,c)` gives a primitive integral original-coordinate vector `u`. The true norm condition is `u^T F4 u=0`, with `q(u)=u^T F4 u/2` integral since F4 is even.

The executable enumerates **all 8^3 ternary residues** per plane, retaining triples primitive mod2 and satisfying `q(u)=0 mod8`. Exactly **64** remain per plane, with 16 in each parity class:

| plane | 001 | 011 | 100 | 110 |
|---|---:|---:|---:|---:|
| 194/195 | 16 | 16 | 16 | 16 |
| 199/200 | 16 | 16 | 16 | 16 |
| 201/202 | 16 | 16 | 16 | 16 |

For each one of these 192 residues, **`F4*u` has an odd coordinate**. Thus any primitive integral null vector in these planes has `gcd(F4*u)` odd.

Since a primitive norm-zero u has even Gram, pairing divisibility is constrained by its primitive lattice geometry. More directly, to establish **exactly 1** rather than merely odd, use unimodularity of H4: `H4+H4^T=-F4` and `det(H4)=1`. The norm-zero vector u has gcd(F4*u) potentially any odd positive number; the finite 2-adic calculation **alone does not establish gcd(F4*u)=1**. Accordingly, the precise verified theorem is:

```
Any primitive integral null u in these planes has pairing divisibility ODD,
and its pairing divisibility is not 2.
```

**Important correction:** pairing divisibility one does not follow solely from mod8 parity enumeration. The stronger claim needs a proof ruling out odd prime divisors of all entries of `F4*u`. This is not established by RQT-353; the divisibility-one gate remains OPEN as an exact integer test after finding a candidate.

## Additional parity computation

The executable also enumerates binary partners `vbar` and verifies that for every primitive null residue, two of the three first-root parity classes `0111,1001,1110` are compatible with the formula
```
r = (1+q(vbar))*u-vbar (mod 2).
```
This is **a necessary binary gate only**. A primitive u of odd but nonunit pairing divisibility might lack an integral Bézout partner with exact `u^T F4v=1`.

## Consequence

RQT-351 guarantees primitive integral null vectors **exist** on the three rational planes, and RQT-353 shows their pairing divisibility is odd. It does NOT prove they all have pairing divisibility one. Until a global divisibility-one argument or explicit u is found, no unconditional first-root existence claim follows from RQT-351 + RQT-353 alone. The older RQT-247 separate existence proof is not being replaced.

## Next natural target RQT-354

Audit the finite set of odd discriminant primes that might divide `gcd(F4 u)` for primitive u in each plane. Alternatively implement a constructive conic solver to obtain a true integer null vector, then inspect gcd(F4u) directly and apply RQT-334. Keep this correction append-only and avoid promoting local parity information to a global integer claim.

## Evidence lineage

All mod-8 residues are derived from **one** frozen original F4. They are computationally exhaustive within their modulus, not independent source ancestors. The 3x3x3 tensor, Josophene/Juliet, brace/box/toroid, and time-angle addresses remain metadata.
