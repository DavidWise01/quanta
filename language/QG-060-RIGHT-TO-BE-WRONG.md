# QG-060 — The Right to Be Wrong

## ASCII invariant

```text
        OLD BASELINE
         [RETAINED]
              |
         SHIFT ALERT
              |
      CANDIDATE PROMOTED
       [HISTORY SEALED]
              |
      FRESH VALIDATION
        [20 OUTCOMES]
              |
       COMPARE RESULTS
        /          \
      MATCH     CONTRADICT
        |           |
     RETAIN       WITHDRAW
     AUTHORITY    AUTHORITY
        |           |
        +-----+-----+
              |
       KEEP ALL EVIDENCE
              |
            {{i}}
```

## Boundary

QG-059 may provisionally promote a candidate when one fresh 20-event confirmation batch is sufficiently compatible with its alerting batch. QG-060 asks a separate question: **Does further evidence still justify the promoted candidate's current authority?** A new 20-event validation sequence is collected with no reuse of the original baseline, alert, or confirmation outcomes.

A completed validation batch is compared with QG-059's confirming batch. Under the declared independent stationary Bernoulli null hypothesis, a single fixed Hoeffding union-bound threshold is used:

```text
n = 20
threshold = sqrt(ln(4/alpha)/(2*n)) + sqrt(ln(4/alpha)/(2*n))
delta = abs(mean(validation) - mean(promotion confirmation))
withdraw authority if delta > threshold
```

An incomplete batch does **not** authorize withdrawal. When the difference exceeds the bound, the model's *current provisional authority* becomes `withdrawn`, and a withdrawal certificate records both rates, the threshold, evidence source, and old versus new authority. The old QG-058 source alert and QG-059 promotion still exist unchanged in the retained record. Otherwise authority remains provisional; no claim of permanent validity is made.

The toy example is 20 baseline zeros, 20 alerting ones, 20 confirming ones and then 20 contradictory validation zeros. It withdraws authority **without erasing the historical reason promotion happened**. Twenty further ones retain provisional authority.

No system-wide production permission changes are made by this demo; 'authority' is an explicit symbolic field in the experiment. This is one confirmatory check, not a calibrated continuously monitored process. An alert suggests investigation under an independence assumption, not causal proof or scientific validation. The retained value objects are deterministically replayable, but are not immutable against an external actor rewriting every field.

Run: `node --test tests/sealed-model-handoff.test.mjs tests/right-to-be-wrong.test.mjs`.
