# RQT-321 — The Infinite Bridge-Root Family and Height-Bound Obstruction

**Status:** Symbolically proved for the explicitly constructed bridge lattice. **Not** a certificate for the original frozen RQT-257 root 18.

## Exact input

```text
F = [-3  1  0  1]     X = [ 0 -1  0  0]
    [ 1 -2  0  0]         [ 1 -1  0  0]
    [ 0  0  1  0]         [ 0  0 -1  0]
    [ 1  0  0 -1]         [ 1 -1  0 -1]
```

Define D=X-I and B=(F adj(D) + adj(D)^T F)/2. Exact multiplication gives det(D)=12 and **B=-6F**, so every norm -2 root automatically satisfies r^T B r = 12, the rank-drop equality.

## Infinite family

For every k in the integers, set

```
r_k = (1, 0, 2k, 1+2k)
F r_k = (2k-2, 1, 2k, -2k).
```

Then:

- Norm: r_k^T F r_k = -2 identically.
- Divisibility: gcd(F r_k)=1 because its second component equals 1.
- Parity: r_k mod 2 = 1001, one of the permitted parity classes.
- Rank reduction: for S=I+r_k(r_k^T F), Y=S X, the determinant lemma and D invertible show det(Y-I)=0. A rank-one update to rank-four D has rank at least three, so rank(Y-I)=3.
- Binary order: r_k mod2 constant, hence S mod2 constant. X mod2 has order exactly 3 and Y mod2 has order exactly 2.

The family has unbounded coordinates. **No finite axis-aligned search box contains every bridge solution.**

## Why a definite-pencil bound fails here

A general root-height criterion is to find rational alpha,beta for H=alpha F+beta B positive definite. If the two equations are q_F(r)=-2 and q_B(r)=det D, then r^T H r = C=-2 alpha + beta det D. Provided C>0, each coordinate satisfies |r_i|² <= C (H^{-1})_{ii}, giving an explicit integral bound. If C<0, no root exists; if C=0, no nonzero root exists.

Here B=-6F, so H=(alpha-6beta)F. F is indefinite (its entries F_11=-3 and F_33=1 give both signs), so H is never positive definite. The absence of this sufficient bound alone would not prove unbounded roots, but the explicit r_k family does.

## Nested unit and provenance

One tensor unit is 3×3×3 with a central site, six faces, twelve edges and eight corners, contained within {brace[box(toroid)]}. Its nine named spatial markers and three-part time/angular address remain independent metadata. Josophene links hardware observations to Quanta software; these tests are **software-only**. Juliet retains its user-specified generation sequence 1,2,3,5,8,13,21.

## Reproducibility

Run `python research/rqt321-infinite-bridge-family.py` (requires SymPy). The script proves the symbolic identities and directly tests 31 instances k=-15..15.

## Next natural bound — RQT-322

For the genuine frozen matrices, compute the *actual* pencil B, then try either a verified positive-definite pencil and complete finite search, or analyze common isotropic directions and local congruence obstructions. Do not transfer conclusions from the bridge lattice to the frozen target without its input matrices.
