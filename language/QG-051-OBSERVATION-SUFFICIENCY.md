# QG-051 — Observation Sufficiency

## Invariant

**Sufficiency is a property of what was observed, not simply how far the observer traveled.**

```text
    ALLOWED WALK
   1 1 2 3 5 8 13
   | |
   | +-- PHASE at same vertex
   +---- AMPLITUDE at first vertex
          |
    retain all compatible roots
          |
   do observed features distinguish them?
          |
    YES -> label within declared model
    NO  -> preserve ambiguity
```

This is a finite candidate-class experiment, not a universal inference theorem. The eight candidate synthetic generators have `k∈{1,2,3,4,5,6,7,8}` and share an embedded `n=13` vertex grid. Position `j` means `theta_j=2π(j mod 13)/13`. The only permitted walk is `1,1,2,3,5,8,13`.

At the **first 1**, measure amplitude `A_k(theta)=0.55+0.45 cos(k theta)`. Roots `k=5` and `k=8` are aliases because `8=13-5`; similarly `k=6` and `k=7`. The same amplitude alias persists at **every** regular 13-grid vertex, so more sampling along that same grid cannot resolve the ambiguity.

At the **second 1**, remain at the same vertex and measure the phase-oriented channel `P_k(theta)=sin(k theta)`. For `k` and `13-k`, the sine signs differ at `theta=2π/13`. Therefore one amplitude sample plus one phase sample at the same permitted position distinguishes every root in this finite eight-candidate class.

For roots 1, 2, 3, 4, one amplitude measurement is already unique among eight candidates. For roots 5, 6, 7, 8, two channel measurements at the same position suffice. With zero samples, eight roots remain possible. This gives the earliest identification under the **declared ordered measurement schedule**, not a proof of globally minimum sensor design. Phase alone might also identify candidates in this particular model; the user-defined schedule still begins with amplitude.

No new physical vertex is visited for the phase measurement. The repeated 1 is a second observation event at the same point, with distinct information. All subsequent Fibonacci checkpoints are still logged, even if identity was resolved earlier.

### Boundaries and tests

- The observer does not see the hidden root except through measured values; the lab's root selector sets the fixture.
- Sufficiency means distinguishing the eight **listed** cosine-frequency hypotheses, not every imaginable generator.
- Floating point comparisons use a fixed declared tolerance `1e-9`.
- This is neither Mandelbrot identification nor a model of a Josephson junction, laptop hardware, or Planck length.
- Append-only-value replay checks prevent inconsistent edits but do not authenticate a fully rewritten history.

```sh
node --test tests/ambiguous-roots.test.mjs tests/observation-sufficiency.test.mjs
```
