# QG-059 — Sealed Model Handoff

```text
   QG-058 VERIFIED ALERT
             |
       OLD BASELINE
     [SEALED BY VALUE]
             |
       ALERTING BATCH
     [PROVISIONAL ROOT]
             |
    COLLECT NEW EVIDENCE
     [20 FRESH EVENTS]
             |
       COMPARE RATES
       /           \
    CONSISTENT    DIFFERENT
       |             |
     PROMOTE        REJECT
       |             |
       +------+------+
              |
     PRESERVE ALL THREE
              |
            {{i}}
```

## Boundary

A QG-058 `review` alert creates a candidate model. **It does not overwrite the old baseline** and does not establish that the generating process truly changed. The QG-059 handoff stores the full QG-058 evidence packet in a separate `sealedOld` field; the first baseline rate is retained independently from the alerting batch's candidate rate. Sealing here is by-value retention and deterministic replay, *not* cryptographic immutability.

After the alert, exactly one non-overlapping new batch of 20 binary outcomes is collected. The kernel abstains from promotion while the confirmation window is incomplete. At completion, it compares the confirming batch rate against the alerting candidate rate, using a fixed two-sample Hoeffding threshold with the original QG-058 alpha. A large difference **rejects this particular candidate**; an absence of a detected difference permits **provisional promotion for further use**.

The test does not prove the new regime, does not establish the old process is permanently gone, and does not give a general false-discovery guarantee over arbitrary repeated candidate searches. It is a single fresh confirmatory check selected after an initial alert. The old data, candidate seed, and all fresh outcomes survive either result. An explicit terminal decision stops further input to this candidate; a future new candidate requires a separate reviewed process.

```text
old:     20 zero outcomes  => rate 0.0
alert:   20 one outcomes   => rate 1.0
confirm: 20 one outcomes   => same candidate; promote provisionally
OR
confirm: 20 zero outcomes  => candidate contradicted; reject
```

The provenance ledger verifies the source alert, event ordering, result counts, and decision by replay. Copies of the same source do not become independent witnesses. This is a finite synthetic Bernoulli experiment, not external scientific or environmental proof.

Run: `node --test tests/change-versus-noise.test.mjs tests/sealed-model-handoff.test.mjs`.
