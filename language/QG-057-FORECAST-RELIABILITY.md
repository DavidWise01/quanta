# QG-057 — Forecast Reliability

## Invariant

**A forecast must be issued before an outcome; a later outcome may update the next forecast, but may not rewrite the earlier one.**

```text
        FORECAST 60%
              |
        SEAL ISSUANCE
              |
         PRICE EVENT
         /        \
       LOW        HIGH
        1           0
         \         /
        BRIER SCORE
              |
       EMPIRICAL RATES
              |
        REVISE FUTURE
          FORECASTS
              |
             {{i}}
```

## Synthetic experiment

A Bernoulli outcome is `1` for a low-cost opportunity and `0` for a high-cost opportunity. The observer begins with an explicitly chosen **Beta(3,2) prior**, giving a starting predictive probability 3/5=0.6. After `n` measured outcomes with `s` low-price results, the next forecast is `p=(3+s)/(5+n)`. This is a model assumption and a reproducible update, not externally established knowledge of real prices.

The forecast is issued with an event ID and sequence index **before** an outcome can be added. Once a result arrives, its binary value is appended to the ledger alongside the original forecast and Brier score `(p-y)^2`. The accumulated mean Brier score is one proper scoring-rule diagnostic, where lower means better performance on these outcomes.

A fixed set of five probability bins reports count, average forecast, and observed low-price frequency. Empty bins have no empirical frequency. In small samples, the observer explicitly flags that calibration is uncertain. Even many samples do not independently establish calibrated predictions under distribution shift or selection bias.

This is one synthetic event stream. Repeated copies of the same record are **not independent witnesses**. The value-based replay detects internally inconsistent edits, but a coordinated rewrite of all state is not prevented without an external authenticated store. Forecasts do not cause or predict actual prices.

## Example

```text
Initial:         3/5 = 0.600
Outcome LOW:       y = 1
Brier:     (.6-1)^2 = .16
Next prediction: 4/6 = 0.667
Outcome HIGH:      y = 0
Brier: (.667-0)^2 ~= .444
Next prediction: 4/7 ~= .571
```

All tests: `node --test tests/uncertain-waiting.test.mjs tests/forecast-reliability.test.mjs`.
