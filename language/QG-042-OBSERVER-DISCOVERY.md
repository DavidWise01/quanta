# QG-042 — The Observer's Discovery

A player who can choose between playing and watching may next learn that **its scoring rule itself is incomplete**. QG-042 tests a narrower, falsifiable claim: whether a candidate utility model predicts independently supplied outcome labels better than the original QG-041 model on both training and held-out experiences.

## Canonical invariant

```
|||| original games (immutable)
       |
       +-- observation events
       +-- independently supplied outcomes
       |
       +-- CHRONOLOGICAL SPLIT (2/3 train, 1/3 holdout)
       |
       +-- select candidate using TRAIN ONLY
       |
       +-- evaluate on HELD-OUT outcomes
       |
       +-- better on both, with margin? -> ADOPT PROPOSAL
       +-- otherwise                  -> RETAIN BASELINE
       |
       +-- append decision; preserve original
||||
```

QG-041's baseline predictor is `2×novelty + .75×breadth + payoff − cost`. QG-042 compares four **predeclared** alternative weight vectors; training MSE selects the best candidate and an untouched chronological holdout is used once as a gate. No claim is made that the agent invents a novel equation. It searches a bounded predefined model family.

The new outcome label is a **separate supplied proxy**, not an independent proof of subjective fun or comprehension. Tests use deterministic synthetic labels whose generating coefficients are known. Altered source events, labels, chosen result and duplicate evaluation fail local replay.

## Guardrails

- At least 12 records, with both play and observation represented in training and holdout.
- A model must beat the baseline on **both** splits by the specified positive improvement margin.
- The holdout is not used to choose a candidate; repeated manual proposals against the same holdout could still overfit it and require additional reserved tests.
- A 24! declaration alone never authorizes a preference change or any model adoption.
- Historical observations remain unchanged. An adopted predictor changes only a new model-selection record, not the QG-041 ledger.
- Local JSON replay is not externally authenticated provenance; no autonomous lifelong learning or validated human enjoyment is claimed.

## Files
- [Kernel](./observer-discovery.mjs)
- [Eleven tests](../tests/observer-discovery.test.mjs)
- [Browser laboratory](../observer-discovery.html)
