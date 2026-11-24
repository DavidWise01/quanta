# RQT-644 — Global-Novelty Pell Unit Gate

## Exact mathematical result

Replayed the full RQT-643 four-policy experiment (three reduced Pell coefficients, three held-out initial offsets, all 24 policy orders, 60 steps per policy). All **51,840 integer observations** were reduced to **1,376 globally distinct coefficient-group-scoped full states (a,b,k)**. Every archived candidate satisfies the exact identity `a²−d b²=k`.

For the first time, the globally deduplicated corpus was tested against *three nontrivial unit recovery mechanisms*: (1) an encountered state with `|k|=1`, (2) exact square-and-divide when `|k|` divides both `a²+d b²` and `2ab`, and (3) same-signed-norm composition of **two distinct full states**, with exact quotient integrality.

| Group | Unique full states | Distinct signed k | Smallest observed |k| | Different-state same-k pairs | Nontrivial unit recoveries |
|---|---:|---:|---:|---:|---:|
| 1 (s=5) | 462 | 462 | 714182761645757 | 0 | 0 |
| 2 (s=7) | 460 | 460 | 25392454990256 | 0 | 0 |
| 3 (s=4) | 454 | 454 | 1185925484330234 | 0 | 0 |
| **Total** | **1376** | **1376** | — | **0** | **0** |

Previously reported equal-norm comparisons were different *observations of the same full state*, giving only trivial quotient identities. **There is not even a pair of distinct full states of equal signed norm within the globally deduplicated sample.** This is a stronger finite explanation for the absence of nontrivial quotient units than merely counting failed pair tests.

The three groups account for **16 of the 27 unresolved canonical sign-orbits**. The other 11 are outside the tested reduced coefficients; the 1,376-state audit is not a whole-lattice proof.

## Reproducibility

- Standard-library exact replay: `research/rqt644-global-novelty-gates.py`.
- Exact local output `RQT-644-results.json` SHA-256: `9360bed29cd8f3db823c1e9ceebd1dee745aa59a95488203be3041a3b4037665`.
- Repeated observations by group: 16,818 / 16,820 / 16,826, summing to **50,464**.
- All three algebraic gates checked without floating-point arithmetic.
- No new global family exclusions, numerical norm-one unit, generalized Pell norm target seed, integer norm−2 vector, or original 22D Wall replay.

**Selected ledger unchanged:** 82/135 selected families excluded all scale (60.74%); **53 unresolved**, represented by 27 canonical sign-orbits; selected corridors do not exhaust the entire lattice. **Root 19 OPEN.**

## Next natural bound — RQT-645

Change the target from generic state novelty to *seed-relevant arithmetic*: analyze the 27 generalized Pell norm targets directly, including exact `z≡h (mod D)` and integer recovery `u`. Do not optimize computation that merely produces more states with different norms without a path to a target seed.

`{brace{n}[box[n](torroid(n))]} · {{i}} · .dlw`
