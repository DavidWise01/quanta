# RQT-596 — Integral Orbit Closure: Algebraic Trace Obstruction

## Certified result

Focus: surviving selected family **28**, ray `[45,-13,18]`, offset `[-1,-1,0]`, using RQT-583 exact Pell archive and RQT-591 exactly rederived 4×4 Gram.

In RQT-595 a rational norm-one element was constructed:
```text
N = 358073442534422222735285217125379300
U = 716146885068844444593653885835030325
V = 1196784763496631790
W = -876916548415728275
lambda = (U+V sqrt(N))/W
U² - N V² = W²
```

The element's algebraic trace is `2U/W`. It is **not an integer**; reduced denominator `2698204764356087` (exact `gcd(2U,abs(W))=325`). Hence this rational multiplier is not an algebraic integer. **No positive power of this multiplier can be an algebraic integer**, because if `lambda^k` were integral, then `lambda` would be integral over the algebraic integers by `x^k-lambda^k=0`, and thus integral over Z by transitivity. Therefore positive powers of this specific rational multiplier cannot give integral Pell units.

This is a rigorous exclusion of **one proposed orbit generator and all its positive powers**, **not** a no-solution theorem for the generalized Pell equation and **not** a new all-scale exclusion of family 28.

## Exact checks executed

- RQT-583 SHA-256 `5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92`.
- RQT-591 *rederived* reduced Gram SHA-256 `f842ede2ac064c20a18760381a8d411361e864caf1c8cdea4598dd7d7879b228` (does not match original archived RQT-575 reduced-Gram bytes).
- RQT-595 U,V,W exact replay and rational norm-one identity.
- Generalized Pell/discriminant identity at signed parameter values.
- Exact nonintegral trace and denominator.

## Integral coordinate recovery gates

Even a rational action may map a **special** integer Pell pair into another integer pair if divisibility holds:
```text
W | (U X + N V Y)
W | (V X + U Y)
X' ≡ B (mod 2 A)
u = (-b(v) ± sqrt(Δ(v)))/a ∈ Z
q_F(u,v) = -2
```
No such generalized Pell seed has been verified, and this trace result alone does not rule out special integer pairs. Existence of other integral Pell units also remains unresolved.

## Status and next natural bound

Selected-family ledger unchanged: **82/135 excluded (60.74%), 53 unresolved**; selected corridors are not the entire rank-four lattice. Original 22D Wall replay NOT PERFORMED; Root 19 OPEN.

**RQT-597:** factor the Pell coefficient into square and squarefree parts, derive a legitimate integral Pell-unit search in the reduced quadratic order, and analyze congruence stabilizers of `X ≡ B (mod 2A)`. Prove only what the actual integral arithmetic establishes.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
