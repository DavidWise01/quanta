# RQT-341 — Full-coordinate-support theorem for the authentic frozen lattice

**Executed exact certificate PASS.** Original eighteenth root and roots 19–21 remain **OPEN**.

## Source and verification

Authentic integer F4/H4 is from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`. The independent `research/rqt341-full-support-gate.py` in `DavidWise01/quanta` rechecks F4 determinant, det H4=1, H4+H4^T=-F4 and the residual isometry before testing four coordinate hyperplanes.

## Exact theorem

For each omitted coordinate index j in {0,1,2,3}, let I_j be the other three indices and `P_j=-F4[I_j,I_j]`. Sylvester's criterion verifies that **every P_j is positive definite** (all three leading principal minors are positive for each j). Therefore F4 restricted to x_j=0 is negative definite.

If x_j=0 and `x^T F4 x=0`, negative definiteness implies x=0. So every nonzero rational/real isotropic vector has all four original coordinates nonzero. This is a global exact support restriction, not just a finite-height exclusion.

For integral norm -2, let z be the three remaining integer coordinates. Then `z^T P_j z=2`. By quadratic-form Cauchy–Schwarz, every coordinate satisfies

```text
z_i² <= 2 * (P_j^-1)[i,i].
```

The exact rational verifier establishes `0 < 2*(P_j^-1)[i,i] < 1` for **all twelve** coordinate bounds across the four planes. Thus every z_i must be zero, contradicting `z^T P_j z=2`. Hence *no integral norm -2 vector lies on any original coordinate hyperplane*.

In short:

```text
q_F(x)=0, x!=0   =>   x0*x1*x2*x3 != 0
q_F(x)=-2, x integral => x0*x1*x2*x3 != 0
```

This strengthens RQT-336's isolated x2=0 observation to **all four** hyperplanes, and provides the arithmetic norm -2 closure separately from negative definiteness.

## Relation to earlier finite bounds

Previously published RQT-254/332/333 constrain y0=-24x0-22x1-17x2-17x3; RQT-337/A/339 constrain x2; RQT-338 ties signs and magnitudes of (x2,y0). Those constraints remain necessary. RQT-341 adds a separate exact full-support gate, not a new numeric height threshold.

The attempted ternary rational-isotropy solver restricted to a coordinate hyperplane cannot succeed. Any exact rational isotropic solver must use all four original coordinates. This explains a mathematical failure mode; a bounded solver timeout by itself is not evidence of nonexistence.

## Reproduction

`python research/rqt341-full-support-gate.py` with SymPy. Its complete exact result includes all twelve inverse-Gram rational bounds and twelve principal minors. Local verifier is independently executed in this turn.

## Next natural boundary — RQT-342

Use the authentic four-variable quadratic form with **full coordinate support**, not a coordinate ternary restriction, for a rational-isotropic construction. A general rational quadratic-form isotropy algorithm or certified conic bundle may produce exact rational u; then primitive-integralize, test gcd(F4u)=1 and apply RQT-334 to obtain genuine root18. Further 19–21 Wall completion is not yet established.

## Provenance and routing

One original F4/H4 source lineage (stoicheion), derived exact computational certificate (quanta). The 3×3×3 tensor, Josophene/Juliet, brace-box-toroid and time-angle slots are iteration metadata, not scientific measurements.
