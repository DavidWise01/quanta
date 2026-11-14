# RQT-365 — The three accepted root-18 parity classes are 2-adically unobstructed

**2026-11-14. Exact finite 2^80 construction PASS; no exact integral norm-minus-two vector found. Root 18 OPEN; roots 19–21 OPEN.**

## Source ancestry
Original frozen `F4` and `H4` from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`. This verifier checks the original Gram determinant, `det(H4)=1`, and `H4+H4.T=-F4`. No synthetic Gram or modified norm is used.

RQT-364 independently performed a billion-triple finite search in an exact unimodular chart and found no norm -2 vector with first three chart coordinates in [-500,500]; this result remains valid, but does not settle global existence.

## Exact accepted-parity theorem

Let `q(r)=r.T*F4*r/2` (integer-valued since F4 is even). The required norm-minus-two condition is `q(r)=-1`, and the accepted root18 parity classes from the existing RQT-257 gate are:

```
0111   1001   1110
```

The exact mod2 gradients `F4*r mod2` in those respective classes are:

```
0111 -> 0011
1001 -> 1001
1110 -> 1010
```

All are nonzero, so each class is **smooth** mod2. The exact Taylor identity for any integer binary update `d∈{0,1}^4` and k>=1 is:

```
q(r+2^k*d) = q(r) + 2^k*(F4*r).T*d + 2^(2k)*q(d).
```

If `q(r)=-1 mod2^k`, exactly **8 of the 16 possible 4-bit updates** satisfy `q(r+2^k*d)=-1 mod2^(k+1)`. The odd gradient persists under binary lifts. This proves indefinite 2-adic lifting in each accepted parity class; there is **no obstruction at the prime 2** to a norm-minus-two vector in one of these classes.

## Exact constructive finite witnesses

The executable `research/rqt365-accepted-root-parity-2adic.py` selects an odd gradient coordinate and adds a single bit when necessary, producing concrete representatives with `q(r)=-1 mod2^80`:

```text
parity 0111: r = [0, 1, 622629194860633805609029, 1]
parity 1001: r = [1026490334254705739787745, 0, 0, 1]
parity 1110: r = [1015889021166329609411595, 1, 1, 0]
```

All three mod2^80 norms and original Wall self-pairings are checked exactly. Their integer norms are **not** -2, so these are local 2-adic representatives, not exact integer roots.

## Root-18 status

An authentic integral root18 has **not** been found. The RQT-362 conditional Bézout extractor and its 17-prefix diagnostic do not create an input vector; moreover the RQT-363 correction holds: the six RQT-257 Wall pairings are internal to the candidate four-root block, and H-orthogonality against all 17 predecessors is not a justified universal gate.

These local 2-adic solutions, even at large precision, do not prove that the integer lattice represents -2 or that an integer candidate extends the frozen 17-reflection prefix. Finding an exact global candidate still requires a constructive indefinite quadratic-form or norm-equation solver and exact original F4/H4 verification.

## RQT-366 natural move

Instead of repeating binary lifts or increasing search radius, pursue a certified global integer representation algorithm, exploiting the two RQT-351 rationally isotropic planes and RQT-353A pairing-divisibility-one theorem, or use a full-rank indefinite quadratic form algorithm. Explicit integer coordinates are required before root18 can close. The nested 3×3×3 cubit, Josophene/Juliet and time-angle notation remain metadata.

**This is a necessary local-root gate closed; original roots18–21 remain OPEN.**
