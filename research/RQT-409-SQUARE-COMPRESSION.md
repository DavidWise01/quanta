# RQT-409 — The Square-Compression Gate

Date: 2026-11-15. Root-19 candidate-successor lattice, actual full RQT-401 Gram. Original root18 position remains unverified.

## Exact arithmetic identity

Let Q be the even symmetric 3x3 reduced Gram and set H=Q/2. Then
H22=f is odd. The equation v^TQv=-2 becomes v^THv=-1.
Holding x,y fixed gives

  f z^2 + 2(c x+e y) z + (a x^2+2bxy+d y^2+1)=0

where a=H00, b=H01, c=H02, d=H11, e=H12, f=H22.

Its reduced discriminant is

  E(x,y)=(c x+e y)^2 - f(a x^2+2bxy+d y^2+1).

The original Q-based discriminant D is exactly 4E. The
coefficients of E in (x^2,xy,y^2,constant) have gcd 1.
Their residues modulo 16 are (10,14,3,9).

**Key equivalence:** Because f is odd, it is invertible modulo every
2^k. Completing the square shows

  E is square modulo 2^k
  <=> there is a z modulo 2^k satisfying v^THv=-1.

Indeed, the reverse direction gives E=(fz+cx+ey)^2.
For the forward direction, choose a square root s and
z=f^{-1}(-cx-ey+s) modulo 2^k.

## Executed full-matrix projection counts

| modulus | xy pairs for which E is a quadratic residue |
|---:|---:|
| 4 | 12 |
| 8 | 40 |
| 16 | 96 |
| 32 | 320 |
| 64 | 1024 |
| 128 | 3840 |
| 256 | 14336 |

These reproduce RQT-407 projected counts without enumerating z.
The mod-4 residues for xy parity 00,01,10,11 are 1,0,3,0.
Thus xy=10 is impossible for norm -2, agreeing with RQT-406.

This is a local congruence equivalence; square E over all integers
and z integral over Z still require independent verification.
Root19 OPEN. Root20 OPEN. Root21 conditional.

A new JPG and embedded-JPG standalone HTML were created as
conversation artifacts. GitHub chapter keeps the ASCII diagram.
