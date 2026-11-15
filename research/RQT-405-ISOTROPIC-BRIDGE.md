# RQT-405 — The Isotropic Bridge: closed by a two-adic obstruction

Date: 2026-11-15. Original F4/H4 candidate-successor fixed rank-three lattice.
New JPG created in conversation; this repository chapter retains the ASCII diagram.

## Exact global theorem

Let Q be the full reduced integral 3x3 Gram stored in the RQT-401 certificate.
Every entry of Q is even, and A=Q/2 satisfies

A mod 4 = [[1,0,1],[0,2,3],[1,3,3]].

For a primitive integer vector v, its parity vector is a nonzero element
of (Z/2Z)^3. Since A is symmetric,

(v+2t)^T A (v+2t) = v^T A v + 4*v^T A t + 4*t^T A t,

so A's norm modulo 4 depends only on the parity of v.

Enumerating all seven primitive parity patterns gives:

001 -> 3
010 -> 2
011 -> 3
100 -> 1
101 -> 2
110 -> 3
111 -> 2

No residue is zero. Thus primitive integral v cannot satisfy Q(v)=0,
because Q(v)=2A(v) is nonzero modulo 8.

Every nonzero rational isotropic vector, after clearing denominators and
dividing by coordinate gcd, would give a primitive integral null vector.
Therefore the rational quadratic cone Q(v)=0 has no nonzero rational point.
Equivalently the ternary form is anisotropic over Q (indeed over Q_2).

This is an unbounded obstruction. It does not apply to Q(v)=-2, because
the mod-4 half-norm target becomes -1 = 3 modulo 4, which occurs in
several primitive parity classes.

## Verification

The verifier enumerates all seven parity classes and all eight lifts
from each parity class modulo 4, asserting invariance. It was executed
against the full RQT-401 Gram held in the current local workspace.
This proof pertains to the successor lattice conditional on the
RQT-386 candidate being the correct position-18 reflection; compatibility
with the frozen prior 17 reflections remains unverified.

Status: rational isotropic route CLOSED; integer root19 OPEN.
Next: work with inhomogeneous norm -2 representations, not rational-null
parametrization. Root20 OPEN; root21 conditional.
