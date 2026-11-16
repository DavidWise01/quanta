# RQT-419 — Integral Congruence Gate

2026-11-16. Exact full RQT-401 candidate-successor Gram Q; the provisional root18 predecessor position has not been verified.

Let H=diag(Q/2,1). The integer matrix U=[[-9,-25,0,0],[-5,-14,0,0],[0,0,1,0],[0,0,0,1]] has det(U)=126-125=1. Therefore H'=U^T H U is an **integral unimodular congruence** and q_H'(t)=q_H(Ut) for all integral t. Since U is a bijection of Z^4, integer representations and isotropic vectors are preserved in both directions. This is not the non-congruence Smith row-column equivalence of RQT-418.

The exact sum of upper-triangular-entry bit lengths improves **7054 -> 7016**; this is an objective score only, not a runtime or root-search guarantee. The second column of U maps to (-25,-14,0,0) and has a strictly positive original H norm. H and H' have **inertia (2 positive, 2 negative)**, established with exact leading-principal-minor signs.

**Visual correction:** The generated JPG incorrectly displays a 4D signature (1 positive, 3 negative). The exact signature is (2,2). The illustration is not a mathematical certificate. Do not repeat its wrong inertia.

## ASCII
```
      RQT-419 : INTEGRAL CONGRUENCE
      +----------------------------+
      | H = diag(Q/2,1)           |
      |             |             |
      |         det U = 1         |
      |             |             |
      |      Hnew = U^T H U       |
      |             |             |
      |      7054 --> 7016       |
      |             |             |
      |      signature (2,2)      |
      |             |             |
      |       INTEGER ROOT?       |
      |           OPEN            |
      +----------------------------+
```

No explicit rational isotropic witness and no ordinary integer root19 found. Root19 OPEN, root20 OPEN, root21 conditional. Next: explore a congruence-preserving exact conic-solving algorithm for the binary hyperbolic sublattice and test any proposed coordinates against original F4/H4 and the frozen 17-reflection predecessor.
