# QG-058 — Change Versus Noise

## ASCII invariant

```text
             BASELINE
             20 EVENTS
                 |
             FREEZE IT
                 |
          MONITOR 20 MORE
                 |
          BATCH COMPLETES?
            /          \
           NO          YES
           |            |
        CONTINUE       TEST
                        |
                 +------+------+
                 |             |
             NO ALERT       ALERT
                 |             |
              CONTINUE      INVESTIGATE
                 |             |
                 +------+------+
                        |
                     {{i}}
```

## What is tested

The outcome stream is binary: 1 means a low-cost price event, and 0 means a high-cost event. The first 20 outcomes form a fixed baseline; each subsequent non-overlapping group of 20 forms a monitoring batch. A screening comparison occurs **only after a complete batch**, not after every new observation.

Under the null hypothesis that all samples are independently drawn from the same stationary Bernoulli distribution, Hoeffding's inequality and the union bound yield a conservative threshold for the absolute difference between the baseline sample mean and monitor sample mean:

```text
delta_k = abs(mean_monitor_k - mean_baseline)
alpha_k = alpha / (k * (k+1))       for k = 1,2,...
threshold_k = sqrt(ln(4/alpha_k)/(2*n_baseline))
            + sqrt(ln(4/alpha_k)/(2*n_monitor))
alert_k = (delta_k > threshold_k)
```

Because the sum of `1/(k*(k+1))` across all positive integer k equals 1, the total familywise false-alert probability is bounded by `alpha` under the declared independent stationary model, even though every batch reuses the same baseline. At alpha=.05, the first of these tests spends .025. Both windows contain exactly 20 observations by default.

An alert means **investigate possible change**; it does not prove a causal mechanism or identify the physical reason. Failing to alert is **not** proof of stationarity. The example synthetic stream of 20 zeros followed by 20 ones triggers investigation. Forty zeros alone do not trigger investigation.

## Evidence, limitations

The record preserves each binary outcome, its index, the derived checkpoint state, and immutable-by-value prior snapshots. Replay recomputes all comparisons from the original events and detects inconsistent history edits. Coordinated rewriting of all stored data is not stopped by a value-only ledger, and a second copy of the same stream is not an independent witness.

The false-alert guarantee requires the stated independent, identically distributed stationary Bernoulli null hypothesis. Drift, serial correlations, selective sampling, and an unrepresentative baseline can invalidate it. Monitoring **stops at the first alert** pending review; this kernel does not autonomously reset a baseline, rewrite past data, or identify a new regime.

Run `node --test tests/forecast-reliability.test.mjs tests/change-versus-noise.test.mjs`.
