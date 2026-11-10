# QG-054 — The Cost of Knowing

```text
               POSITION 1
                   |
             AMPLITUDE READ
                   |
            AMBIGUOUS ROOTS
                   |
       EXPECTED INFORMATION BITS
                   |
       BENEFIT = BITS × VALUE/BIT
                   |
             - SENSOR COST
                   |
          +--------+--------+
          |                 |
      NET > 0            NET <= 0
      AND AFFORDABLE       OR TOO COSTLY
          |                 |
      MEASURE PHASE       STOP
          |                 |
        LEARN           PRESERVE UNKNOWN
```

## Precisely bounded decision

In the finite eight-root model of QG-051–053, after observing amplitude at permitted position 1, the observer has the second, repeated `1` checkpoint available for a separate channel. The only candidate second channels are amplitude or phase, both at **the same vertex**. Each has a declared nonnegative observation cost. There is a separate nonnegative budget and a user-selected nonnegative value per bit.

The observer calculates `expectedBits` from the uniform compatible-candidate partition. `benefit = expectedBits*valuePerBit`; `net = benefit - sensorCost`. It performs the most valuable affordable measurement **only when net is strictly positive**. At equality it stops; a sensor with cost greater than the remaining budget is not purchased even if it offers information.

For ambiguous roots 5/8 and 6/7, phase has 1 expected bit and repeating amplitude has 0. With valuePerBit=1, phase breaks even at cost 1 credit. At cost 0.35 the expected net is +0.65. Roots 1..4 already uniquely identified after the initial amplitude need no second reading.

This is a **one-step myopic value-of-information policy**, not proof of globally optimal search. Cost credits are abstract, not real electricity or capacitance. Learning the modeled root does not guarantee inference about unknown external physics.

## Evidence

The ledger records original amplitude, selected second channel, sample, expected bits, cost, compatible roots, and total spent; deterministic replay rejects inconsistent changes. It is not authenticated by an external trusted witness.

Run `node --test tests/no-wasted-movement.test.mjs tests/cost-of-knowing.test.mjs`.
