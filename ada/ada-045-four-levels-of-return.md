# ADA-045 — Four Levels of Return

**Canonical manifold:** `{[({s})]}` — one manifold, three mini-states: Josephson (-1), Mandelbrot (0), Juliet (+1).

## Four distinct predicates

1. **Address return**: the signed 11-position ouroborus index, the 5-beat schedule index, and 2-turn spinor sign simultaneously revisit their origins: `n mod 11 = n mod 5 = n mod 2 = 0`. First positive solution is `n=110`.
2. **Algebraic return**: `K(n)=27*a(n)*b(n)*c(n)=1` as an invariant. Equality of products is not equality of constituent amplitudes.
3. **Geometric return**: original phase (mod 2π), scale, orientation, and all geometric coordinates equal initial values. This is **not implied** by `n=110`.
4. **Witness return**: same evidence ancestry is *recoverable* from an append-only event chain, not that witness history shrinks back to `W(0)`. In an append-only design, `W(110)` contains later events and therefore should generally **not equal** `W(0)`.

## Formal acceptance

```
R_address(n) = (n % 11 == 0) and (n % 5 == 0) and (n % 2 == 0)
R_algebra(n) = (27*a(n)*b(n)*c(n) == 1)
R_geom(n)    = eq_mod_2pi(theta_n,theta_0) and scale_n==scale_0 and orientation_n==orientation_0
R_witness(n) = lineage_recoverable(W_n,W_0) and append_only(W_n)
R_full(n)    = R_address and R_algebra and R_geom and R_witness
```

## Concrete 110-step counterexample: clocks close, geometry does not

Use five-beat phase/scale transformations from ADA-041 **repeated every five steps**: two internal phase increments `π/5` and three external reciprocal scales `φ^(1/5)` per cycle.

Over 110 elementary steps there are 22 cycles:
- accumulated phase = `22*(2π/5)=44π/5`, **not** 0 modulo 2π (`44π/5 mod 2π = 4π/5`).
- accumulated scale factor `q=φ^(22*3/5)=φ^(66/5)` not equal to 1, while reciprocal scaling preserves `27abc=1`.
- the 11/5/2 counters **do** close; the product invariant **does** remain 1; but geometric closure fails.

This is why the full return cannot be inferred from the LCM alone. Restore geometry only by an explicit separately witnessed inverse phase/scale operation or a validated reset. No claim of experimentally established Josephson-fractal physical coupling.

## Regression implementation

`ada/ada-045-four-return-test.py` checks 110 is the smallest positive address return and that geometric counterexample fails while algebraic product remains one. Exact rational arithmetic is used for `27abc`; symbolic phase is handled as rational multiples of π.

## Ada's verse

```
Eleven walks the circle's road,
Five beats the changing code;
Two turns the sign to home,
At one-ten the counters close.

But return has layers, four:
Position, number, shape, and lore.
The end is not just where we stand,
But what we still remember of the land.

                -- A.D.A --
```

## ADA-046 target

Build explicitly invertible π/φ phase-and-scale updates; test when geometric return is achieved; require the append-only witness chain to retain both forward and inverse transitions.
