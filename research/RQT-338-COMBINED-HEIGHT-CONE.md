# RQT-338 — Combined height-and-cone search gate

**Status:** Exact new necessary inequalities for both norm-zero and norm-minus-two vectors of the **authentic frozen** rank-four RQT-242 lattice. Roots 18–21 remain OPEN. The earlier separate height searches are imported as previous source certificates, not rerun here.

## Source and ancestry

Gram F4 and Wall H4 are the original matrices from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`. Independent finite-height source certificates: RQT-254, RQT-332, RQT-333 establish `|y0|>=1021` for norm -2, with `y0=-24x0-22x1-17x2-17x3`. RQT-337 and RQT-337-A establish `|x2|>=5001` for nonzero norm-zero and norm-minus-two vectors. Those searches are not re-executed by this script.

## Exact unimodular joint chart

Use the integer change of coordinates `z=Ux`:

```text
U =
[  0   0   1   0]   z0 = x2
[-24 -22 -17 -17]   z1 = y0
[  1   0   0   0]   z2 = x0
[  0 -13   0 -10]   z3 = -13*x1-10*x3

det(U)=+1.
```

Thus the chart preserves the complete integer lattice exactly; no divisibility congruence is lost.

Set `J=U^-T F4 U^-1` and split its lower-right 2×2 block `N=J[2:4,2:4]`. Exact principal-minor tests show `N` negative definite. The projected Schur matrix

```
K = J[0:2,0:2] - J[0:2,2:4]*N^-1*J[2:4,0:2]
  = (U[0:2,:] F4^-1 U[0:2,:]^T)^-1.
```

is an exact symmetric rational matrix of signature (1,1) with all three independent entries **negative**. Completing the square in `(z2,z3)` establishes the *necessary* inequality for `q=x^T F4 x`:

```
q <= (x2,y0)^T K (x2,y0).
```

A positive-cone projection therefore demands `(x2,y0)^T K(x2,y0)>=q`. It is not a sufficient test for integrality because the optimal transverse coordinates may be nonintegral.

## The combined bound

For any nonzero integral isotropic vector, or any integral norm-minus-two root, the earlier RQT-337/A exclusion gives `|x2|>=5001`. Write `t=y0/x2`. The scalar quadratic `P(t)=K00+2 K01 t+K11 t²` is concave, and exact rational tests show

```text
P(-63/250) < -2/(5001²),
P(-2/125)  < -2/(5001²),
P'(-63/250)>0, P'(-2/125)<0.
```

Thus for `t<=-63/250` or `t>=-2/125`, `q<=x2² P(t)<-2`, ruling out both `q=0` and `q=-2`. Therefore every possible root or isotropic vector satisfies:

```text
x2*y0 < 0
2/125 < |y0|/|x2| < 63/250.
```

For a norm-minus-two eighteenth-root candidate, **combine all constraints**:

```text
|x2| >= 5001,
|y0| >= 1021,
x2*y0 < 0,
(2/125)|x2| < |y0| < (63/250)|x2|.
```

In particular same-sign coordinate pairs are forbidden, and the absolute ratio lies strictly between 0.016 and 0.252. The individual height bounds do not become numerically larger solely from this intersection; the advancement is the exact **coupling and cone filter**.

## Verification and limits

Run `python research/rqt338-combined-height-cone.py` with SymPy. It asserts authentic F4/H4 identities, det(U)=1, negative definiteness of the transverse plane, exact Schur identity, and rational inequalities. Original root18 and roots19–21 remain OPEN.

## Next RQT-339

Use the joint unimodular chart to enumerate lattice candidates on the admissible wedge; parameterize the remaining two coordinates with rigorous conditional bounds and simultaneously impose the RQT-331 parity/modular screens. This may prune drastically compared with independent height sweeps. No root should be promoted before its exact norm, parity, divisibility, rank drop and downstream Wall conditions are certified.

The user-defined 3×3×3 nested cubit, Josophene, Juliet and time-angle coordinates remain metadata and iteration addressing, not substitute proof objects.
