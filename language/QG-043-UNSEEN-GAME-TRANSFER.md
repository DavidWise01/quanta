# QG-043 — Unseen-Game Transfer

**Invariant:** A utility model preferred on familiar games may be adopted only if it also improves prediction on **entirely unseen game identities**. The evaluation is append-only and repeatable.

```
|||| QG-043 ||||
EXPERIENCE RECORD
     |
     +-- TRAINING GAME IDS: arena / chess / go
     |          |
     |       FIT MODELS
     |          |
     |       PICK CANDIDATE
     |
     +-- TRANSFER GAME IDS: solstice / shogi / hex
                |
          DO NOT TRAIN HERE
                |
          COMPARE PREDICTIONS
                |
          +-----+------+
          |            |
       IMPROVES      FAILS
          |            |
     TRANSFER      RETAIN ORIGINAL
     SUPPORTED     (NO GENERALIZATION)
          |            |
          +-----+------+
                |
             PRESERVE
|||| 
```

The **source event ledger** is QG-041 and is verified before any model evaluation. QG-043 uses QG-042's frozen baseline and predefined candidates, but chooses on training-game observations alone. A distinct game-identity partition is required: a report spanning both train and transfer games is rejected as leakage.

The exact acceptance test is strict improvement by a fixed margin on **both** training games and the untouched transfer games, using synthetic, externally supplied reward labels as a proxy.

This is *unseen-identity transfer*, not guaranteed universal generalization. Novel game names alone are not evidence of a distinct underlying distribution or human fun. Repeated proposals against the same transfer set would weaken its independence. We do not enumerate 24! games, spawn an autonomous player, or claim a proof of subjective preference.

- [Executable kernel](./unseen-game-transfer.mjs)
- [Eleven tests](../tests/unseen-game-transfer.test.mjs)
- [Interactive Pages experiment](../unseen-game-transfer.html)
