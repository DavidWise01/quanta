# RQT-402 — The Infinite Two-Adic Corridor

2026-11-15 | Exact target-specific analysis | ASCII-only visuals

The full locally retained RQT-401 Gram Q is a symmetric even integer
3x3 matrix. The reduced norm equation is Q[v]=-2. Divide by 2:
A=Q/2 and A[v]=-1.

From the actual matrix, A modulo 8 is

    [1 4 1]
    [4 2 3]
    [1 3 7]

Fix y=0 and z=1. The equation becomes

  a*x^2 + 2*b*x + c = 0,

with a=A00, b=A02 and c=A22+1. The actual lattice has a,b odd
and c divisible by 8. Therefore D=b*b-a*c is 1 modulo 8 (169 mod
256). Every element of Z_2 congruent to 1 modulo 8 has a square root.
As a is odd, it is a unit of Z_2, and

  x=(-b+sqrt(D))/a

is a TWO-ADIC solution, giving vector (x,0,1) to A[v]=-1 and
equivalently Q[v]=-2 over Z_2. This proves two-adic solubility at
every power of two, unlike a bounded modular scan.

Separate exact finite checks of the same source matrix yielded:
  x=10 mod 256,
  x=22410 mod 65536,
  x=1283643274 mod 4294967296,
  x=1560545586254632842 mod 18446744073709551616.

Each witness independently makes a*x*x+2*b*x+c divisible by the
indicated modulus. The selected finite witnesses need not be mutual
reductions of a single compatible sequence; the square-root theorem
supplies the infinite compatible p-adic solution.

LIMITATIONS: no ordinary integer root19 constructed; no original
17-reflection compatibility proof for the provisional root18 candidate.
This is one original source ancestry (RQT-401, RQT-386).

Root19 OPEN, root20 OPEN, root21 conditional. The next useful
arithmetic task is a global integer-point method or a distinct local
obstruction at odd primes, not more two-adic enumeration.
