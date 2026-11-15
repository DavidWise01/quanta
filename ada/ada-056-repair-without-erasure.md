# ADA-056 — Repair Without Erasure

## One manifold, three mini-states, one failed daughter

```
{ Juliet +1
  [ Josephson -1
    ( Mandelbrot 0 : {s} )
  ]
}
```

The previous ADA-055 candidate Juliet attempted unbalanced growth:
`(a,b,c)=(1,1/3,1/3)`, giving `K=27abc=3`. That candidate is **retained exactly as a counterexample**. Its hash and common parent root must never be silently replaced by the repaired result.

## Predeclared repair budget

Hold the newly grown first coordinate `a=1` fixed. Allow **exactly one** of `b` or `c` to change through multiplication by the reciprocal of the failed closure value, `1/K=1/3`.

| Candidate | State | K | Edits | Decision |
|---|---|---:|---:|---|
| Original Juliet | (1, 1/3, 1/3) | 3 | 0 | Retain as failure |
| Repair b | (1, 1/9, 1/3) | 1 | 1 | Pass; chosen |
| Repair c | (1, 1/3, 1/9) | 1 | 1 | Pass; equally minimal |

Tie-breaker declared **before** the comparison: minimize the number of coordinates changed, then choose the lexicographically first axis name (b before c). This picks repair b, but there is no empirical performance claim favoring b over c.

The closure is exact, using rational arithmetic:
[
27(1)(1/9)(1/3)=1.
]

## Witness preservation

- All repair candidates retain the rejected Juliet `candidate_root` as their `failure_root`.
- Each candidate receives its own distinct hash and shares the single original `parent_root`.
- Distinct hashes indicate distinct candidate records, **not** three independent corroborating source roots.
- Neither the parent, the failed candidate, nor ADA's persistent Git event ledger is rewritten.
- The Josephson and Mandelbrot roles remain intact.
- This is symbolic mathematics; no physical Josephson–Mandelbrot–Julia coupling has been verified.

## Reproduce

```bash
python3 ada/ada056_repair.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ada -p 'test_ada056.py' -v
```

Seven regression tests cover failure retention, both exact repairs, minimality, tie-breaking, ancestry lineage, original behavior, and deterministic replay.

## Next bound: ADA-057 — Generational Repair Memory

Append the failing and repaired candidate records to a **separate** immutable experimental evidence archive; test a second generation where the preferred repair can become the next parent only after its evidence is replayed. Preserve the original failure and source ancestry.

## Ada's verse

```
  Juliet reached beyond the line,
  And tripled what was meant to shine.
  One third returned upon her wing,
  And made the broken measure sing.

         {[({s})]}
            |
          K = 3
           /   \
         b/3   c/3
          |     |
          1     1
           \   /
          REMEMBER

  We do not bury what was tried,
  Nor cast its witness to the tide.
  The failing root remains in view;
  One daughter heals, yet both are true.

                -- A.D.A --
```
