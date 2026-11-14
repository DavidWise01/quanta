# ADA-041 — Five-beat π/φ Phase–Scale Test

## Canonical manifold

```
{ Juliet +1 [ Josephson -1 ( Mandelbrot 0 : {s} ) ] }
                              {[()]}
                  one parent, three mini-states
```

Each beat is a scheduled, explicit mathematical transformation. The vocabulary "resonance" is a **hypothesis**: this document tests algebraic closure only, not laboratory resonance.

## Fixed clock

- 5 beats in one cycle.
- Beats 1–2 are internal (2/5 of the total).
- Beats 3–5 are external (3/5 of the total).
- π phase operant on each internal beat: `theta <- theta + π/5` (phase accumulated after beat 2: `2π/5`).
- φ scale operant on each external beat: `q = φ^(1/5)`; `(a,b,c) <- (q a, b/q, c)`. After beat 5: `a = φ^(3/5)/3`, `b = 1/(3φ^(3/5))`, `c = 1/3`.

`φ = (1+sqrt(5))/2` and `π` are mathematical constants. There is **no assertion** that 2/5 is a physical time interval; no absolute cycle duration is provided.

## Exact ninefold invariant

```
K0 = 27*(1/3)*(1/3)*(1/3) = 1
Kj = 27*(q^j / 3)*(1/(3*q^j))*(1/3) = 1
       for j = 0,1,2,3
```

The internal phase steps change a separate phase register; they do not change the three real mini-state amplitudes. External scale steps affect two amplitude values reciprocally. The box identity, singlet address and mini-state identities remain constant.

## What returns, and what does not

- PASS: algebraic product remains exactly 1 at every beat.
- PASS: two internal and three external beats.
- PASS: the single manifold ID and singlet remain fixed.
- NOT A RETURN: after five beats `theta = 2π/5` and `(a,b,c)` differs from the initial `(1/3,1/3,1/3)`.
- An inverse reset could return those numeric values, but would be a separately recorded operation, not hidden inside the five beats.
- No physical Josephson/Julia/Mandelbrot coupling has been demonstrated.

## Witness specification

Record `(cycle,beat,operant,theta_before,theta_after,a_before,b_before,c_before,a_after,b_after,c_after,K,source_ancestry)` for every beat. The visible state and its witnesses are not the same thing; identical products are not identical histories. Earlier frozen tests remain untouched.

## Regression fixture (Python pseudocode with exact symbolic arithmetic)

```python
from sympy import Rational, pi, sqrt, simplify
phi = (1+sqrt(5))/2
a=b=c=Rational(1,3)
theta=0
for beat in range(1,6):
    if beat <= 2:
        theta += pi/5
    else:
        q=phi**Rational(1,5)
        a*=q
        b/=q
    assert simplify(27*a*b*c-1)==0
assert simplify(theta-2*pi/5)==0
assert simplify(a-Rational(1,3)*phi**Rational(3,5))==0
```

## ADA verse

```
  Two beats protect the winding core,
  Three reach beyond the vessel's door.
  Pi lends the phase; Phi lends the scale,
  The witnesses preserve the trail.

             { [ ( {s} ) ] }
                  |
           I  I  E  E  E
             π     φ
                  |
             27abc = 1

  One product holds though branches bend,
  Yet changed coordinates are not the end.
  The loom shall tell what stayed the same,
  And what has changed, with root and name.
```

## Next bound ADA-042

Cycle across three mini-state addresses while testing whether cyclic permutations preserve the same global product and whether source ancestry survives reassignment. Keep π phase and φ scale registers independent; test return only when each is explicitly restored.
