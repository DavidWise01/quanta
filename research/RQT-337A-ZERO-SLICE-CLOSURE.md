# RQT-337-A — Exact zero-slice closure

The original frozen `F4` is the stoicheion RQT-242 Gram matrix. Let `P=-F4[[0,1,3],[0,1,3]]` be the positive-definite transverse form for `x2=0`.

Any integral vector `x=(z0,z1,0,z2)` with norm `x^T F4 x=-2` would require `z^T P z=2`. By Cauchy–Schwarz for the quadratic inner product, `z_i^2 <= 2(P^-1)_{ii}`. Exact rational calculation verifies each of the three upper bounds `2(P^-1)_{ii}<1`. Thus every integral `z_i=0`, contradicting `z^T P z=2`. Because P is positive definite, `x^T F4 x=0` on this hyperplane likewise implies `z=0`.

Together with the separately executed RQT-337 script checking every `1<=x2<=5000` and central symmetry covering negative `x2`, **every nonzero isotropic integer vector and every integral norm-minus-two root of original F4 must satisfy `|x2|>=5001`**.

This is a finite necessary height bound, not a root witness or proof of global nonexistence. Original root18 and roots19–21 remain OPEN. It resolves the zero-slice caveat explicitly raised in `RQT-337-ORIGINAL-X2-HEIGHT5000.md`. The machine proof is `research/rqt337a-zero-slice-closure.py`; this addendum is append-only and leaves the earlier caveat legible as provenance.
