# QG-053 — No-Wasted-Movement Bound

```text
     CURRENT VERTEX 1
             |
      AMPLITUDE KNOWN
             |
    WHAT CAN I MEASURE?
         /       \
       PHASE     MOVE
        |         |
      GAIN 1    COST > 0
        |         |
      STAY      NOT CHOSEN
        |
     OBSERVE
        |
   UNIQUE CANDIDATE
        |
       STOP
```

## Declared invariant

Among legally available next measurements on the fixed Fibonacci walk `1,1,2,3,5,8,13`, select an action that maximizes predicted *model-relative* information gain minus a nonnegative movement penalty. Stop if no action offers a strictly positive net gain. The two identical `1` entries are observation opportunities at the **same coordinate**, never extra distance traveled.

This extends QG-052's eight-root synthetic frequency model. Given amplitude at the first `1`, roots 5/8 and 6/7 remain ambiguous. Phase at the same point separates them with one expected bit; repeating amplitude supplies zero. At least one member of each pair can be identified without spatial movement. A root already unique after first amplitude observation requires no further measurements.

The bounded action menu is current-position unspent channels and, when the next Fibonacci step changes the position, the channels at that next position. `allowPhase` models sensor availability and `movementCost` is an invented dimensionless experiment score, not physics. The model intentionally stops when only redundant channels remain or a move has nonpositive net score. It does not guarantee optimal global information across an unbounded future walk, and does not infer Mandelbrot dynamics or Josephson hardware.

A replayable value ledger preserves observations and chosen actions and recomputes the selection rule. Ledger self-consistency is not cryptographic evidence of an external event.

```sh
node --test tests/independent-information.test.mjs tests/no-wasted-movement.test.mjs
```
