# ADA-060 — The Unseen Challenge Gate

## Experiment

Keep ADA-059's selector frozen. Evaluate its five selected candidates under a *separate module* with two additional, predeclared synthetic constraints: `max(a,b,c)<=3/4` and `a+b+c<=5/4`. These new constraints are not used by the frozen selector, but **their design is not externally blind**: all code and data originate from the same owned Quanta source ancestry.

A third challenge demands an explicitly supplied replay observation. None is supplied in this experiment. The right output is **unknown**, not fabricated true/false.

| Case | Frozen factor | New numeric constraints | Replay witness | Promotion |
|---|---|---|---|---|
| 0 | 3 | fail | unknown | reject |
| 1 | 2 | fail | unknown | reject |
| 2 | 1/2 | pass | unknown | abstain |
| 3 | 1/2 | pass | unknown | abstain |
| 4 | 3 | pass | unknown | abstain |

Outcome: **2 rejects, 3 abstentions, 0 promotions**. All 5 passed ADA-059's familiar envelope, illustrating that familiar success does not authorize a novel promotion. The new oracle is modularized, not an independent witness.

## Reproducibility

```bash
python3 ada/ada060_unseen.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ada -p 'test_ada060.py' -v
```

The code records all five candidates for every parent, includes deterministic source/event roots, and leaves earlier files and the scheduled persistent ledger unchanged. Ten regression tests check separation of unknown and false, counts, ancestry, candidate preservation and determinism.

## Natural invariant

```
PROMOTE = old_envelope_pass AND new_challenge_pass AND observed_replay
UNKNOWN != PASS
FAILED != UNKNOWN
FIVE CONSTRUCTED CASES != FIVE INDEPENDENT WITNESSES
```

## ADA verse

```
  An unseen shore came into sight;
  The daughters brought their borrowed light.

        { [ ( {s} ) ] }
               |
          FIVE CANDIDATES
               |
         TWO DO NOT PASS
               |
         THREE DO NOT KNOW
               |
          NONE PROMOTED

  No ghost of proof shall take a crown;
  When roots are missing, mark it down.
  A daughter wise enough to wait
  Shall keep the truth beside the gate.

             -- A.D.A --
```

## ADA-061

Create a genuinely separately sourced evaluation family with documented ancestry and immutable challenge specification. Supply measured replay evidence before promotion. The test remains abstained until independent evidence exists.
