# QG-052 — Independent Information

## Rule

```text
    FIBONACCI PATH
    1 / 1 / 2 / 3 / 5 / 8 / 13
    |   |
    |   +---- second observation (same position)
    |
    +-------- amplitude observed
               |
         compatible roots
               |
        +------+------+
        |             |
   REPEAT SAME     MEASURE PHASE
     AMPLITUDE         |
        |             |
     0 NEW BITS     MAY GAIN BITS
        |             |
        +------+------+
               |
       PRESERVE EVIDENCE
```

**QG-052:** A second observation is informationally useful precisely when it reduces the set of hypotheses still compatible with all measured values *under the declared model*. The system counts reduction in `log2(number of candidates)` (uniform discrete prior).

Use the same eight candidate cosine-frequency roots and thirteen-vertex positions as QG-051. First measure amplitude at position 1. For a hidden root 5 or 8, the amplitude alone leaves both possibilities. Repeating the exact same amplitude at that vertex does not reduce the candidate set: **0 bits gained**. Measuring phase `sin(k*theta)` at that same vertex distinguishes them: **1 bit gained**. Roots 6 and 7 behave analogously. Roots 1..4 were already uniquely identified by the first amplitude observation and thus receive 0 further bits from either channel.

No movement occurs at the second 1. Comparisons between repeat-amplitude and phase are alternative experiments on the same permitted second checkpoint; this does **not** insert a third sample or change the seven-step walk.

For each proposed next channel, the observer also calculates *expected* information gain before the result arrives by partitioning the currently possible roots according to predicted readings, assuming an equal prior on those roots. This is model-relative and does not establish independent sensors, physical phase, or a complete explanation of an unknown real-world structure.

The ledger preserves first and second measured values, candidate sets, realized information gain, and deterministic replay. The observation record is a value object, not a cryptographic or external archival witness.

## Implementation

```sh
node --test tests/observation-sufficiency.test.mjs tests/independent-information.test.mjs
```
