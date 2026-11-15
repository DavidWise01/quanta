# ADA-059 — Frozen Envelope Selection

## One manifold, two selectors

`{[({s})]}` remains one shared manifold with Josephson `−1`, Mandelbrot `0`, and Juliet `+1`. `π` and `φ` remain separate internal/external operants; this synthetic selection experiment does not retune the persistent timing kernel.

The **old** selector accepts `27abc=1` and chooses the first highest-novelty candidate. The **new** selector requires all five ADA-058 synthetic envelope predicates (closure, positivity, maximum amplitude 1, imbalance <=9, and permutation invariance) before using the same novelty/priority rule. Both use exact rational arithmetic and the same factor priority: `3, 2, 1/2, 1/3, 1`. Transform candidate `(a,b,c) → (qa,b/q,c)`; original parent and every rejected candidate are retained.

## Five constructed fresh parents

| Parent | Old q | Old passes full envelope? | New q | New passes? |
|---|---:|---|---:|---|
| (1/3,1/3,1/3) | 3 | yes | 3 | yes |
| (1/2,2/9,1/3) | 3 | no | 2 | yes |
| (2/3,1/6,1/3) | 3 | no | 1/2 | yes |
| (3/4,1/6,8/27) | 3 | no | 1/2 | yes |
| (1/4,4/9,1/3) | 3 | yes | 3 | yes |

Old selector: **2/5** pass the full envelope. New selector: **5/5** pass because it directly enforces that envelope. This is a **sanity check of constraint-aware filtering**, not independent evidence of transfer learning. These inputs were constructed by us and the new selector is evaluated on exactly its own programmed constraints. Permutation invariance is also algebraically automatic for `abc`; it is not a separate independent empirical challenge.

## Evidence discipline

- Five proposals per parent; 25 candidate records, each with own hash and explicit common parent root.
- One synthetic source ancestry, `synthetic:ada059:fixture`. Different hashes are **not** independent witnesses.
- Rejected candidates remain in outputs; unchanged parent remains available as the `q=1` fallback.
- No persistent scheduled GitHub ledger writes, hidden model changes, or scientific training claims.
- Evaluation rule frozen within this fixture before selecting; true out-of-distribution validation requires unseen task families and independently specified criteria.

## Repeat

```bash
python3 ada/ada059_select.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ada -p 'test_ada059.py' -v
```

## ADA's verse

```
    Five daughters walk the wider shore,
    Not every one may pass the door.

       {[({s})]}
          |     |
        OLD     NEW
        2/5     5/5
          \     /
         SAME ROOT
            |
        KEEP FAILURES

    What law was learned from yesterday
    Must meet tomorrow's different way;
    A gate may hold because we wrote
    Its rules upon the testing note.

    No crown for matching what we knew;
    Seek strangers' questions, witness true.

               -- A.D.A --
```

## ADA-060 · Next natural target

Separate candidate creation and challenge evaluation by sealed, independently authored input families. Record source lineage and actual held-out surprises; do not declare success merely from satisfying rules explicitly used for selection.
