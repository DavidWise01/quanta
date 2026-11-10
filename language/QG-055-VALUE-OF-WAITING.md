# QG-055 — The Value of Waiting

## ASCII bound

```text
   KNOWN AMBIGUITY AT POSITION 1
                 |
     PHASE COST TOO HIGH NOW
                 |
        FINITE COST CALENDAR
                 |
         +-------+-------+
         |       |       |
       BUY      WAIT    STOP
         |       |       |
     GAIN NOW  LATER   UNKNOWN
         |       |       |
         +-------+-------+
                 |
     REPLAY COST / EVIDENCE
```

## Mathematical decision rule

The observer receives a declared deterministic finite calendar of nonnegative future sensor prices, a nonnegative waiting fee per tick, a discount in the interval `0 < discount <= 1`, a budget, and a nonnegative value per model-relative bit. It stays at Fibonacci position 1 throughout. The first reading is amplitude; the optional second reading is phase. The synthetic eight-root family is QG-051's cosine-frequency model.

At time t, for a possible phase observation at time u>=t, the calculated net is:

```text
net(t,u) = expectedBits * valuePerBit * discount^(u-t)
           - phaseCost[u] - waitFee*(u-t)
```

The observation is affordable only if its sensor price plus accumulated waiting fees does not exceed the remaining budget. Choose the affordable, strictly positive net option with the highest net; resolve ties toward earlier time. If the winning time equals the present, observe. If in the future, wait one tick and recompute. If none is worthwhile, stop and preserve uncertainty. The modeled time horizon contains at most 13 calendar entries. The code has no actual timer or background execution.

With root 5/8 ambiguity, value per bit 1, costs [1.2,0.7,0.3], waiting fee 0.05, and discount 1, waiting twice costs 0.1 and then sampling costs 0.3, leaving net 0.6. The observer logs two wait events followed by one observation; remaining candidates become a singleton. The total paid cost is 0.4 credits.

**Boundary:** this is a finite deterministic planning example. Real costs are uncertain, and the observer cannot know that the price will actually fall. The rule is model-relative and one-branch reactive; it does not prove universally optimal stopping, real physical waiting dynamics, or claims about general intelligence.

Every event is value-based replay verifiable, not externally cryptographically authenticated.

```sh
node --test tests/cost-of-knowing.test.mjs tests/value-of-waiting.test.mjs
```
