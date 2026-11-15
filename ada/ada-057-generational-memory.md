# ADA-057 — Generational Repair Memory

## Natural bound

A tested repaired daughter may become the next parent **only through an explicit promotion record**. The failed candidate, alternate repair and original parent remain separate, traceable events. All eight events derive from **one source ancestry**: eight hashes are not eight independent witnesses.

## First two generations

| Event | State `(a,b,c)` | `K=27abc` | Result |
|---|---|---:|---|
| Origin | (1/3,1/3,1/3) | 1 | parent |
| G0 Juliet | (1,1/3,1/3) | 3 | retained failure |
| G0 repair c | (1,1/3,1/9) | 1 | alternate |
| G0 repair b | (1,1/9,1/3) | 1 | selected |
| G1 promotion | (1,1/9,1/3) | 1 | explicit parent |
| G1 Juliet | (3,1/9,1/3) | 3 | retained failure |
| G1 repair c | (3,1/9,1/9) | 1 | alternate |
| G1 repair b | (3,1/27,1/3) | 1 | selected |

Lexical b-before-c tie-break remains the declared fixture rule; it is not an empirical preference. No persistent scheduled `ada/kernel/events.jsonl` edits are performed.

## Persistent experimental archive

`ada057_generations.py` creates eight deterministic content-hashed records with `seq`, `previous_event_hash`, `parent_roots` and one `source_ancestry`. The hash chain records the append sequence, while the parent roots capture branching provenance. `--export` creates a new archive with exclusive file creation and rejects overwrites. `--verify` validates a saved archive. Repository commits persist the experiment and its generated archive if the archive is explicitly committed.

Run:
```bash
python3 ada/ada057_generations.py
python3 ada/ada057_generations.py --export scratch/ada057.jsonl
python3 ada/ada057_generations.py --verify scratch/ada057.jsonl
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ada -p 'test_ada057.py' -v
```

## ADA's verse

```
  One daughter mends her broken wing,
  Yet failure keeps its ancient ring.
  The healed one mothers what comes next;
  The roots survive in written text.

         {[({s})]}
            |
      1/3 1/3 1/3
            |
        JULIET K=3
         /       \
      c/3         b/3
       |           |
     K=1         K=1
                  |
               PROMOTE
                  |
            JULIET K=3
               /   \
             c/3   b/3
              |     |
              1     1
                    |
               3,1/27,1/3

  A daughter grows, a mother stays;
  The ledger keeps their separate ways.
  One root remembers every turn;
  What fails may teach, but must not burn.

              -- A.D.A --
```

## Next ADA-058

Quantify generational growth and sensitivity: do not equate passing closure with fitness. Define external challenge cases and test whether a repaired daughter generalizes beyond the same `K=1` equation.
