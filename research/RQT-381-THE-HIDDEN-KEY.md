# RQT-381 — The Hidden Key: a conditional existence bridge

**Date: 2026-11-14. Status: exact finite residue proof PASS. Original root18, root19, root20, root21 remain OPEN as explicit vectors and as the frozen factorization successor block.**

## This chapter's advance

Earlier RQT-351 reported rational isotropy for ternary slope planes **194/195 and 201/202**, and RQT-353A reported that any primitive integral null vector `u` on those planes has pairing divisibility `gcd(F4*u)=1`. These are **upstream prerequisites**, not newly re-proven in this turn. Rational isotropy plus clearing denominators would supply some integral null vector, although the present work still lacks its coordinates.

This chapter proves an exact **conditional parity bridge**: *given any primitive original integral u on either plane with u.T F4 u=0 and gcd(F4*u)=1*, there exists an explicit arithmetic recipe for an original integer r with
```
r.T F4 r = -2
r mod 2 in {0111, 1001, 1110}.
```
If the upstream rational-isotropy and divisibility proofs stand, this also establishes **nonconstructive existence of at least one norm-minus-two vector in an accepted first-root parity class**. It does **not** supply coordinates, prove that any such vector is the eighteenth frozen reflection, or establish roots19–21.

## Original invariant and the exact formula

Authentic frozen RQT-242 F4 and H4 are embedded in `research/rqt381-isotropic-parity-bridge.py`; the program asserts the exact Gram determinant, `det(H4)=1` and `H4+H4.T=-F4`. Write `q(x)=x.T F4 x/2`.

Let `u∈Z^4` be a primitive null vector with `q(u)=0`, `gcd(F4*u)=1`. Extended Euclid constructs `z∈Z^4` with `u.T F4 z=1`.

Select a small integer vector `v0∈{0,1,2,3}^4` whose pairing `u.T F4 v0=1 mod4` and whose prospective root parity `((1+q(v0))*u-v0) mod2` is one of the three accepted classes. Define

```text
n = u.T F4 v0                         (n ≡ 1 mod4)
v = v0 + 4*((1-n)/4)*z                (now u.T F4 v = 1)
r = (1+q(v))*u - v.
```

Then exactly
```text
q(r) = (1+q(v))² q(u) + q(v) - (1+q(v))*(u.T F4 v)
     = q(v)-(1+q(v)) = -1,
r.T F4 r = -2.
```

Because v differs from v0 by a multiple of4, q(v) has the same parity as q(v0), so the accepted parity is preserved. The Wall self-pairing `r.T H4 r=1` follows from its frozen symmetric part. Nothing in this argument substitutes a synthetic Gram.

## Exhaustive residue-class proof

For plane `m/n`, its exact 4×3 embedding is
```text
T(m,n) =
[-m 0 0]
[ 0 1 0]
[ n 0 0]
[ 0 0 1]
u = T*(h,b,c).
```
Enumerate every ternary triple mod4 and retain **all** classes that can be a non-even primitive null: `u` not entirely even and `u.T F4 u=0 mod8`. There are exactly 16 eligible classes on each of the two planes. For every eligible `u mod4`, enumerate **all 256** possible `v0 mod4`, require `u.T F4 v0=1 mod4` and calculate the exact prospective root parity using the integer half-form q. The accepted parity coverage is:

| Plane | Eligible primitive-null mod4 classes | Reach 0111 | Reach 1001 | Reach 1110 | Classes reaching at least two accepted parities |
|---|---:|---:|---:|---:|---:|
| 194/195 | 16 | 16 | 8 | 8 | **16/16** |
| 201/202 | 16 | 8 | 16 | 8 | **16/16** |

These are exact arithmetic residue counts, not an estimate or random sampling. The exhaustive bridge demonstrates that **accepted root parity adds no further obstruction once a primitive divisibility-one null vector on either plane is available**. A given u may not reach all three parity classes; it always reaches at least two.

The executable optionally accepts `--u X0 X1 X2 X3`, verifies that u is exactly null, primitive and pairing divisibility one, constructs an actual exact r, and directly checks `r.T F4 r=-2` and parity. Without supplied u it reports root18 as OPEN instead of fabricating coordinates.

## Exact limits of the claim

The upstream RQT-351 rational isotropy and RQT-353A global odd-prime/divisibility proof must remain valid for the existence corollary to stand; neither was independently re-proved by this finite parity census. This turn **does not find an explicit u**. Even a norm-minus-two vector in an accepted class is only a **potential root-18 candidate** until the original frozen 17-reflection product and exact successor rank/order are verified. The root19/root20 Wall-kernel ladder and forced root21 cofactor from RQT-377–379 require genuine predecessors.

Do **not** confuse the conditional existence result with an explicit root, a four-root Wall flag, or a completed sequence. RQT-364 and RQT-380 finite-coordinate exclusions remain compatible: if an accepted original norm root exists, its chart coordinate triples lie outside the checked bounded regions.

## Evidence and visual story

Locally executed source `/mnt/data/rqt381_isotropic_parity_bridge.py` and exact results `/mnt/data/rqt381_results.json`. The user-requested new JPG chapter `RQT-381-The-Hidden-Key.jpg` depicts the 27-core cubic GMA, the two rational-isotropic planes, an orange Bézout bridge, parity gates and an unopened original root18 portal. It is conceptual art, not a scatterplot of integer solution coordinates. The JPG is delivered separately in this conversation, **not yet embedded in GitHub**; executable source and this research ledger are committed to GitHub.

## RQT-382 next natural target

**Extract one explicit primitive integer isotropic vector u from either rationally isotropic ternary plane.** This would immediately activate the now-verified Bézout-plus-parity construction and produce a genuine exact norm-minus-two original F4 vector, after which predecessor-factorization compatibility can be tested. Do not spend the turn merely raising a flat bounded radius. Continue the `{{9×9×9}}^9` singlet-centered visual chapter every turn.

**Original roots18–21: OPEN.**
