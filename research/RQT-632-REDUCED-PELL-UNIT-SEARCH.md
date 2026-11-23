# RQT-632 — Reduced Pell Unit Search: Certified Convergent Bounds

## Exact executed result

Reopened the RQT-630 coefficient certificate with verified SHA-256 `25d228f0176e366deca4fa3401b66789650ad2ef2c0dcb68d054c95a1de83ea6`. Its three exact square-factor reductions `D=s²d` with `s=5,7,4` were used as the arithmetic search targets. For each reduced coefficient d, **20,000 simple continued-fraction convergents** of sqrt(d), indices 0 through 19,999 inclusive, were constructed using exact integer recurrences, and every candidate was checked directly against `p²-dq²`.

**Total:** 60,000 exact convergents tested, **0 norm+1 hits, 0 norm−1 hits**. No nontrivial numerical reduced unit was constructed and thus none was transferred to the original D equation.

| Reduced group | s | Recovery E from RQT-631 | q_19999 bits | SHA256 of q_19999 unsigned big-endian |
|---|---:|---:|---:|---|
| 1 | 5 | 6 | 34,341 | `74eaeb05ffd242d3173846e83b5719bbd0dd4d8c3a6c6f2780f92433f975117a` |
| 2 | 7 | 6 | 34,434 | `73b66568b49b5fb85e4f1978f1c49ab8e05a031e62482addfa7520873e64d675` |
| 3 | 4 | 4 | 34,251 | `67698644a32a8c2c96dbe28f1c8e92aeb0dd1176e29f16fef9580a4497b849e2` |

Any nontrivial positive integral solution `x²-dY²=1` with `Y>0` must correspond to a continued-fraction convergent of sqrt(d). Thus every such unit has `Y>q_19999` for its reduced group. This is a **lower bound**, not a nonexistence theorem: a unit may occur at a later convergent.

The full certificate `RQT-632-results.json` has SHA-256 `0c5cc30a499222457339908b0ff6556f898bd83ce0a7b0e17df2549b70286ed2`. Replayer: `research/rqt632-reduced-unit-search.py` (Python 3 standard library). An independent rerun reproduced the certificate bytes and checksum.

## Transfer gates and limits

The sharp residue-group exponents (6,6,4) from RQT-631 are **conditional**: only once a genuine reduced integer norm-one unit is found can we raise it to exponent E, verify its square-root coefficient divisible by s, and then recover an original unit `x²-Dy²=1`. None was found in this search.

This result does not construct any generalized Pell norm target seed, recover any original integer norm−2 vector, or replay the original 22D Wall conditions. Zero new whole-family exclusions. The selected-family ledger is unchanged: **82/135 excluded all-scale (60.74%), 53 unresolved**, represented by 27 canonical sign orbits. **Root 19 OPEN**.

## RQT-633 natural bound

Shift from linear convergent enumeration to structural period computation and certified modular factor constraints on reduced coefficients. A new unit should be reported only upon exact direct norm verification, with the recovery exponent, parameter congruence, and original coordinate gates separately checked.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`