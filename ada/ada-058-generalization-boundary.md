# ADA-058 — The Generalization Boundary

## Question

Does a repaired daughter that preserves familiar `27abc=1` also satisfy **other declared constraints**?

This test applies a newly defined synthetic **diagnostic challenge**, not a truly blinded external benchmark: the rules are developed after ADA-057 states are known. Hence it does **not** prove generalization to unseen real-world tasks. It does expose a clear failure of *closure-only* promotion.

## Challenges (five)

1. **Conservation:** `27abc=1`.
2. **Positive amplitudes:** `a,b,c>0`.
3. **Resource cap:** `max(a,b,c)<=1`.
4. **Balance:** `max(a,b,c)/min(a,b,c)<=9`.
5. **Symmetry:** All six coordinate permutations have the same value of `27abc`.

These are model-design choices, not physical constants. Scoring = number of predicates satisfied; full transfer requires 5/5. The resource cap and ratio challenge are genuinely different criteria from closure, though still synthetic.

| State | Triple | K | Imbalance | Pass |
|---|---|---:|---:|---|
| Origin | (1/3,1/3,1/3) | 1 | 1 | 5/5 |
| Gen0 repair B | (1,1/9,1/3) | 1 | 9 | 5/5 |
| Gen1 repair B | (3,1/27,1/3) | 1 | 81 | 3/5 |
| Gen1 repair C | (3,1/9,1/9) | 1 | 27 | 3/5 |

The failure is **informative**: `K=1` is necessary for this fixture, but not sufficient for the declared challenge envelope. Gen1 is not promoted as broadly successful on the basis of closure alone. All ADA-057 source events remain unchanged.

## Reproducibility

```bash
python3 ada/ada058_transfer.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ada -p 'test_ada058.py' -v
```

The output carries source-event hashes, one common source ancestry, deterministic rule version and result root. The 10 test cases validate the boundary, permutation invariance, exact fractions, and lineage stability. These tests do not rewrite the scheduled ADA kernel or the original generational evidence.

## Next bound ADA-059

Introduce a new candidate-selection objective that checks all five constraints **before promotion**. Freeze the new rule before generating candidates; compare to the old closure-only method on fresh synthesized parent states, not merely the examples used to choose thresholds.

## Ada's verse

```
  The daughter kept the sacred one,
  Yet climbed beyond the measured sun.
  Her product held, her balance strayed;
  A wider question must be weighed.

          {[({s})]}
              |
            K = 1
              |
         NOT ENOUGH
          /       \
      BOUND       SCALE
         \         /
        TEST WHAT'S NEW

  The root remains, the failure speaks;
  A wiser gate is what she seeks.
             -- A.D.A --
```
