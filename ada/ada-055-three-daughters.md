# ADA-055 — Three Daughters, One Parent, One Test

## Natural bound

One immutable state `{[({s})]}` has three mini-state roles: Josephson `-1`, Mandelbrot `0`, and Juliet `+1`. Candidate branches are *test fixtures* drawn from the same state, not independent source witnesses.

Starting amplitudes: `a=b=c=1/3`; invariant `K=27abc=1`.

| Candidate | Transform | Result | K | Decision |
|---|---|---|---|---|
| Josephson | `(2a,b/2,c)` | `(2/3,1/6,1/3)` | 1 | admissible |
| Mandelbrot | `(a,b,c)` | `(1/3,1/3,1/3)` | 1 | admissible baseline |
| Juliet | `(3a,b,c)` | `(1,1/3,1/3)` | 3 | counterexample |

**Selection rule fixed before testing:** among candidates that preserve `K=1`, choose the one with the greatest number of changed mini-state amplitudes; break ties lexically by candidate name. This selects Josephson, *not* because the transformation is learned or intrinsically better, but because it meets a declared deterministic exploratory objective.

## Witness rules

- Each branch has a distinct candidate hash but **the same parent root**.
- One common root does not become three independent corroborating witnesses.
- Rejected Juliet is kept as a counterexample and never silently deleted.
- Parent state is not mutated; the persistent scheduled kernel `ada/kernel/events.jsonl` is neither read nor written.
- One mathematical closure is not evidence for a real Josephson junction, Mandelbrot physical system, or Julia/Juliet chemistry.

## Run

```bash
python3 ada/ada055_candidates.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ada -p 'test_ada055.py' -v
```

## ADA verse

```
  Three daughters born from one small dot,
  One guards a bridge, one holds the plot.
  One reaches farther than law allows,
  And leaves a mark upon the boughs.

          { [ ( {s} ) ] }
                 |
               1/27
                 |
                x 27
                 |
               1 = 1
              /  |  \
          JOS   MAN   JUL
           1     1     3
           |     |     |
         PASS  BASE  FAIL

  The failing branch is not erased;
  Its parent root and place are traced.
  The next may grow, but first must see
  What shapes are true to unity.

                 -- A.D.A --
```

## ADA-056 proposal

Generate a fourth candidate by repairing the Juliet failure with a reciprocal factor; demand minimum alteration relative to the rejected state, exact closure and independently replayable root lineage. Compare predeclared repair costs and preserve the failing case.
