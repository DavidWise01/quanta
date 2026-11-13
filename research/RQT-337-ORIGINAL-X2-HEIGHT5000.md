# RQT-337 — Original frozen lattice: new x2-height obstruction

**PASS: exact exhaustive finite calculation.** Genuine original roots 18–21 remain OPEN.

## Original source

Authentic integral Gram `F4` from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`; no synthetic bridge substitution.

## Positive-direction coordinate and exact bounds

In original coordinates `x=(x0,x1,x2,x3)`, RQT-336 proved that the restriction to `x2=0` is negative definite. Fix a positive integer `t=x2` and write `z=(x0,x1,x3)`. Let

```
P = -F4[[0,1,3],[0,1,3]]  # positive definite
b = F4[[0,1,3],2]
v = P^-1 b
beta = F4[2,2] + b^T P^-1 b > 0.
```

Then the exact quadratic identity is

```
x^T F4 x = beta*t² - (z-t*v)^T P (z-t*v).
```

For target norm `q=0` or `q=-2`, the projected `(x0,x1)` coordinates lie in the ellipse with matrix `K=(P^-1[0:2,0:2])^-1`:

```
alpha*(x0-v0*t)^2
 + K11*(x1-v1*t + K01/K11*(x0-v0*t))^2
 <= beta*t²-q
alpha=K00-K01²/K11>0.
```

The Python script constructs rational outward bounds, asserts boundary inequalities exactly and enumerates every integer `(x0,x1)` enclosed at each `t`. It solves the remaining `x3` quadratic via its **exact integer discriminant**, with no arbitrary bound on `x3`.

## Exact execution for 1 <= x2 <= 5000

| Target norm | Enumerated coordinate pairs | Nonnegative discriminants | Perfect-square discriminants | Integer solutions |
|---|---:|---:|---:|---:|
| 0 | 1,729,528 | 1,156,603 | 0 | 0 |
| -2 | 1,729,528 | 1,156,603 | 0 | 0 |
| **Total** | **3,459,056** | **2,313,206** | **0** | **0** |

All negative `x2` heights are covered by `x → -x`. RQT-336 proves there are no nonzero isotropic vectors on `x2=0`, and a negative-definite slice also cannot have norm -2 if its nonzero integral minimal norm is less than -2; **do not infer this second claim merely from definiteness**. The script's search bounds apply only to `1<=|x2|<=5000`. For norm 0, `x2=0` contains only the zero vector. For norm -2, independently check the `x2=0` plane before asserting a global lower bound.

The strongest unconditional new result from this turn is `|x2|>=5001` for **nonzero integral isotropic vectors**, and a negative norm -2 exclusion for `1<=|x2|<=5000`. The claimed norm-minus-two global height bound needs the `x2=0` case separately verified.

## Mathematical boundary

This is an exhaustive *finite-height* no-witness result. It does not contradict RQT-247's global existential theorem, and it does not instantiate root 18. The 21-reflection chain remains open.

## Next RQT-338

Audit the negative-definite plane `x2=0` for norm -2 using an exact integral minimum bound; then construct a rational isotropic witness via a global quadratic solver or prove a larger coordinate lower bound. Maintain source/derived-witness ancestry separately.
