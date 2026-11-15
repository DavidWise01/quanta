# RQT-384 — The Conic Decoder: global coordinate-slice obstruction

**Date: 2026-11-14. Exact original F4/H4 calculation PASS. No original integer isotropic vector or roots18–21 recovered.**

## The result

RQT-382 excluded nonzero ternary isotropic vectors whose two selected chart coordinates lie in ±10000; RQT-383 tested 264 local p-adic branches without constructing a global integer null vector.

RQT-384 supplies a **global** (unbounded) exclusion on two authentic rationally isotropic plane forms: in either exact RQT-352 unimodular ternary chart `z=(h,x,y)`, a nonzero rational isotropic vector satisfying `z.T A z=0` **must have all three coordinates nonzero**.

This assertion depends only on exact integer binary-form arithmetic, not the earlier rational-isotropy claim. It is compatible with the upstream assertion that both ternary planes have rational null points, because those points must lie off all three coordinate lines.

## Original matrices and binary proof

Use the frozen original `F4` and `H4` from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`, with `det(H4)=1`, `H4+H4.T=-F4` and the independently verified `det(F4)`. For slope m/n (194/195 or 201/202), let

```text
T(m,n)=[[-m,0,0],[0,1,0],[n,0,0],[0,0,1]]
V194=[[1,3,1],[-25,-74,-24],[113,340,113]]
V201=[[1,2,1],[-26,-51,-25],[117,235,117]]
A=V.T*T.T*F4*T*V.
```

Setting any one of `h,x,y` to zero leaves a nondegenerate binary quadratic `a s²+2bst+ct²=0`, with exact half-discriminant `D=b²-ac`. A nonzero rational solution requires D to be a nonnegative rational square; since D is an integer, that requires a nonnegative perfect **integer** square.

The exact computed half-discriminants are:

| Plane | h=0 | x=0 | y=0 |
|---|---|---|---|
| 194/195 | 7871344764190723989698871343936405833 | -2020692228609206586199528939517571540 | 968610353976935876931240734104630129 |
| 201/202 | 5737024439397272476664404525448214457 | -3272928109767528305742489923852754456 | 2007258792882010936946802311921413609 |

Both negative values are impossible squares, and every positive value failed an exact `math.isqrt` perfect-square test. Thus **all six** coordinate-zero ternary slices are rationally anisotropic. Therefore

```text
if z.T A z = 0, z ∈ Q³ nonzero:
     h ≠ 0, x ≠ 0, y ≠ 0.
```

No finite coordinate cutoff or modular-only witness is involved.

## Exact conditional conic parametrization

Given any **actual integral null seed** `u0∈Z³`, `u0.T A u0=0`, and any integer direction `w∈Z³`, define

```text
Q = w.T A w
P = u0.T A w
z = Q*u0 - 2*P*w.
```

Direct expansion gives `z.T A z=0` identically, because the cross term cancels the `w.T A w` term. Whenever z is nonzero, divide by the gcd of its three coordinates to obtain a primitive integer null vector. The original rank-four vector is `U4=T*V*z` and must satisfy `U4.T F4 U4=0` exactly.

**This is a seed-to-family constructor, not a seed-finding algorithm.** It parametrizes rational points on a smooth ternary conic *after a rational point has been supplied*. It does not show any such point exists or provide one on the authentic planes.

The executed local `/mnt/data/rqt384_conic_decoder.py` verified the six global exclusions and generated numerous distinct exact null vectors on a synthetic test conic `h²+x²-y²=0`, seeded by `(1,0,1)`. It did **not** generate an authentic original F4 null vector. The executable supports `--plane 194/195 --seed h x y` or `--plane 201/202 --seed h x y`, and will reject an invalid seed by exact arithmetic.

Local results: `/mnt/data/rqt384_conic_decoder_results.json`.

## Architecture and JPG story

The GMA search architecture remains nine nested generations of **9×9×9 = 729 microcells** around the `||||` singlet, with 27 spatial cores. The narrative JPG **RQT-384-The-Conic-Decoder.jpg** depicts the two genuine ternary planes, a locked null-vector gate and the conditional decoder. It was rendered in this conversation; it is **not a graphical plot of exact integer solutions** and has **not been uploaded to GitHub**.

## Next RQT-385

Acquire a true **original integral null seed** through a certified rational-conic solver, ideally via factored quaternion/ternary norm descent rather than further finite-radius enumeration. Then verify both the ternary and original F4 norms, run the exact conic decoder and RQT-381 Bézout bridge, and check accepted root18 parity and frozen 17-reflection factorization before promoting a vector to root18. The RQT-377→379 exact Wall kernel ladder remains ready for the subsequent roots.

**Original roots 18, 19, 20 and 21 remain OPEN.**
