# RQT-340 — An exact real/algebraic null plane, but no rational descent

**Status:** Verified on authentic `DavidWise01/stoicheion` RQT-242 F4/H4. A specific two-dimensional Lorentzian subspace is split over a quadratic field but **anisotropic over Q**. Original integral root 18 and roots 19–21 remain OPEN. No global no-go result is claimed.

## Explicit vectors

```
p = (-9979, -1271, 10000, 5812)
p^T F4 p = 3736495518772065804440 > 0

q = (
 -1814519854974686433251,
 -290599304661563123694,
  2286383199540229140000,
  1328845915572781176168
)
q^T F4 q = -986958776170401411467442490485759901583480400207425778184940 < 0
p^T F4 q = 0
```

The integer vector q is constructed by taking the F4-orthogonal projection of e0 from the positive line spanned by p, then dividing its integer content. All identities are exact.

Define `C=528280454887176328887138801371672078777` (odd). Exact arithmetic yields

```
(p^T F4 p)/(-q^T F4 q) = 2/C.
```

For any rational a,b, the norm on the plane is `a² A - b² B`, with A>0, B>0. A nonzero isotropic vector would require `(b/a)²=A/B=2/C`. But `v_2(2/C)=1` is odd, so 2/C is not a rational square. Consequently, this **specific rational two-plane contains no nonzero rational null vector**.

There is, however, a *genuine exact algebraic* null vector

```
u_K = p + sqrt(2/C)*q
```

over the quadratic field `K=Q(sqrt(2/C))`; exact symbolic evaluation proves `u_K^T F4 u_K=0`. This is **not** a rational or integral vector and must not be passed to Bézout as root18.

## How it changes the search

The global frozen lattice has signature (1,3) and earlier RQT-247 provided an existential rational-isotropy argument. The present failure is only for the particular span_Q(p,q), not the full four-dimensional quadric. It demonstrates why picking an arbitrary positive and negative vector, then solving one quadratic square-root equation, can create a local squareclass obstruction even when the whole form is isotropic.

A genuine global solver needs to vary the negative direction in the three-dimensional negative complement (or use exact quaternion/Hasse algorithms), and then **certify norm zero on F4 over Q**. Once u is obtained, clear denominators and test gcd(F4u)=1; RQT-334 supplies the exact root18 Bézout step and RQT-257 supplies the sufficient exact Wall-flag theorem for roots19–21.

## Reproduce

`python research/rqt340-exact-quadratic-plane.py` with SymPy. It checks the original H4/F4 identity, explicit positive/negative vectors and orthogonality, ratio in lowest terms, 2-adic obstruction, and exact algebraic null identity. A computational test of a bounded ternary solver was stopped after timing out and is **not** mathematical evidence of nonexistence.

## Evidence and identity

Original RQT-242 matrices are one primary lineage; numerical vectors and the quadratic-field identity are derived calculations, not independent source witnesses. Nested {brace[box(toroid)]} 3×3×3 cubit and Josophene/Juliet/time-angle address remain navigation metadata.

**Next RQT-341:** search for an exact rational isotropic direction in a three-dimensional subspace with a certified local-solvability and descent algorithm, rather than selecting another arbitrary two-plane or increasing modular precision. Root 18–21 status stays OPEN until a genuine integer witness is checked.
