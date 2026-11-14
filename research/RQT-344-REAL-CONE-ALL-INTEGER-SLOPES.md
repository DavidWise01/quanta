# RQT-344 — Exact original-lattice real cone and all-integer-slope exclusion

**Verified by exact SymPy and integer arithmetic.** Authentic frozen `F4`/`H4` from `DavidWise01/stoicheion/research/rqt/rqt242_mod4_audit.py`; original integral roots 18–21 **OPEN**.

## Change from the prior local sieve

RQT-342 and RQT-343 used local congruences to exclude integer-indexed ternary planes `x0=-k*x2`. RQT-344 finds that these integer-indexed planes are **all** rationally anisotropic, by a combination of exact **real** and 5-adic obstructions.

## Exact Schur proof

Split the coordinates into `a=(x0,x2)` and `b=(x1,x3)`. The transverse block `C=F4[[1,3],[1,3]]` is negative definite. Write `A=F4[[0,2],[0,2]]`, `B=F4[[0,2],[1,3]]` and `K=A-B C^-1 B^T`.

Completing the square in `b` gives the identity

```text
x^T F4 x = a^T K a + (b+C^-1 B^T a)^T C (b+C^-1 B^T a)
           <= a^T K a.
```

For `x0=-k*x2`, set `P(k)=(-k,1) K (-k,1)^T`, so any nonzero isotropic vector with `x2 !=0` requires `P(k)>=0`.

The exact rational verifier certifies:

```text
P''(k) < 0,
P(0) < 0, P'(0) > 0,
P(1) > 0,
P(2) < 0, P'(2) < 0.
```

Consequently P(k)<0 for every **integer** k<=0 or k>=2; each corresponding whole ternary restricted form is negative definite. The sole exceptional integer k=1 has some real null directions but the independently replayed primitive residue search modulo25 gives **zero** norm-zero primitive triples on `x0=-x2`. Clearing denominators of a nonzero rational isotropic triple would produce a primitive integer triple, contradiction. Therefore **no integer k yields a nonzero rational isotropic point** in this family.

This is a theorem for this integer-slope family, not a claim that F4 is globally anisotropic; rational noninteger slopes remain possible.

## Narrow full-space slope window

Exact outward rational endpoints satisfy

```text
L = 19893/20000 = 0.99465
R = 2503/2500 = 1.0012
P(L)<0, P'(L)>0; P(R)<0, P'(R)<0.
```

Hence any nonzero rational isotropic point on the full F4 requires

```text
19893/20000 < -x0/x2 < 2503/2500
x0+x2 != 0.
```

The second condition follows from the exceptional k=1 5-adic obstruction. Since earlier RQT-341 excludes x2=0, this ratio is defined.

Moreover `P(L),P(R)<-2/5011²`, so the same outer interval is necessary for every genuine original integral norm-minus-two root when combined with the previously certified RQT-337/339 lower height `|x2|>=5011`. Do not treat this as a new unconditional proof of the old height bound.

## Verified implementation

`research/rqt344-real-cone-integer-slope.py`; the equivalent local verifier was executed at `/mnt/data/rqt344_real_cone_integer_slices.py`, including complete primitive modulo25 enumeration for the exceptional plane. No heuristics, floating point, assumed witness, or arbitrary search cutoff.

## Next natural target: RQT-345

Replace integer k with **rational** slopes `k=m/n` strictly inside the cone and `m!=n`. Investigate small nonzero `|m-n|`, with a certified rational ternary isotropy algorithm for each plane or direct four-dimensional quadric solver. Apply exact norm, gcd pairing divisibility, required root parity, and Wall completion tests before announcing any eighteenth root.

Source ancestry: both real cone and modular checks are derived computations from one original F4/H4. Somatic tensor/brace/torus, Josophene/Juliet and time-angle coordinates remain metadata, not mathematical evidence.
