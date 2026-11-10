# QG-056 — The Uncertainty of Waiting

```text
           UNKNOWN FUTURE
                 |
          FORECAST BRANCHES
          /             \
    LOW PRICE         HIGH PRICE
      p = .6            p = .4
          \             /
          EXPECTED UTILITY
                 |
          +------+------+ 
          |      |      |
         BUY    WAIT   STOP
          |      |
       MEASURE   REVEAL REALIZED PRICE
          |      |
          |     BUY IF STILL WORTHWHILE
          |      |
          +------+
                 |
             EVIDENCE
```

## Invariant

**A predicted future outcome is not an observed one.** Decide based on the complete declared prior distribution; only after waiting may the realized future price be disclosed and acted upon. An attractive hypothetical outcome is not retroactively assigned certainty.

Finite one-tick model with phase information benefit `B = expectedBits * valuePerBit`. Today a phase measurement costs `C0`. Waiting costs `W`; the next-tick cost is one of `C_i` with declared probabilities `p_i` summing to one. At the future tick the agent can choose **not** to buy. For remaining budget `Q`:

```text
buyNow = (C0 <= Q) ? B - C0 : -infinity
futureSurplus_i = (W + C_i <= Q) ? max(B-C_i,0) : 0
wait = (W <= Q) ? sum_i(p_i*futureSurplus_i)-W : -infinity
stop = 0
```

Select the **strictly positive** highest value; at a tie choose buy now, not wait. If the observer waits, charge W and later reveal one supported outcome; buy phase information only when its realized price is affordable and its net benefit is strictly positive. Never silently expose the hidden root or the realized branch before waiting.

Canonical example: root 5 (compatible set {5,8}) gives one expected phase bit, B=1 credit. Current price 0.8, waiting fee 0.05, future outcomes 0.2 (60%) or 1.4 (40%), and budget 2. Today net=0.2; wait net=0.6*(1-0.2)+0.4*0-0.05=0.43, so wait. At the cheap outcome buy and identify the synthetic root; at the costly outcome stop and preserve {5,8}. This outcome-dependent policy avoids treating a forecast as certain.

**Model boundary:** probabilities and prices are supplied assumptions and may be wrong. They are not measured event frequencies, claims about electricity, physical probabilities, or calibrated predictions. No real clock or asynchronous monitoring is started. The model is a one-step contingent decision, not a global optimum for general unknown environments.

Every state event retains its prior forecast and explicit realized price and is independently replayable against the declared model. It is not an externally signed record.

```sh
node --test tests/value-of-waiting.test.mjs tests/uncertain-waiting.test.mjs
```
