# RQT-406 — The Three Surviving Gates

2026-11-15 | Original RQT-401 conditional candidate-successor lattice.
Visual: ASCII primary; new conversation JPG and embedded-JPG HTML created.

Let Q be the original integral rank-three reduced Gram and A=Q/2.
The target norm equation Q(v)=-2 is A(v)=-1.

A modulo 4 is:
  [1 0 1]
  [0 2 3]
  [1 3 3]

Because A is symmetric, replacing v with v+2t changes A(v) by a
multiple of 4. Thus the parity of v completely determines A(v) modulo 4.

The seven primitive parity classes have half-norm residues:
001:3, 010:2, 011:3, 100:1, 101:2, 110:3, 111:2.

As -1 = 3 (mod 4), the ONLY possible primitive parities of an
integral norm-minus-two root are 001, 011, 110. This exclusion is
global at all coordinate sizes.

More strongly, all three possible parity classes occur 2-adically.
Fix (y,z) to (0,1), (1,1), (1,2), respectively. Set

  a=A00,
  b=A01*y+A02*z,
  c=A11*y^2+2*A12*y*z+A22*z^2+1,
  D=b*b-a*c.

In all three cases a odd and D congruent 1 modulo 8; hence D has a
2-adic square root and x=(-b+sqrt(D))/a is a 2-adic solution.
The resulting x parity is even, even, and odd respectively, so
the three parity classes are realized.

Exact finite witnesses modulo 2^64 (not ordinary integer roots):
  001: x=10783917623109408650, y=0, z=1
  011: x=8284749223855128812, y=1, z=1
  110: x=12640643517325232419, y=1, z=2

These satisfy A(x,y,z)=-1 modulo 2^64.
The independent infinite proof is the square-root theorem in Z_2.
The witnesses are independent examples and need not be the nested
reductions of one chosen infinite branch.

No integer norm-minus-two vector has been constructed.
The root18 predecessor-position check remains unresolved.

Root19 OPEN; root20 OPEN; root21 conditional.
Next promising avenue: use the parity reduction in the exact
inhomogeneous ternary search / genus-spinor or arithmetic descent.
