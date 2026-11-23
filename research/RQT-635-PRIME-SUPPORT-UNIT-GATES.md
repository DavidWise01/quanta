# RQT-635 — Prime-Support Pell Unit Gates & Recovery-Ready Verification

## Executive summary

RQT-634 corrected universal **recovery-only** exponents to 3, 3 and 2. RQT-635 does not claim a numerical nontrivial Pell unit. Instead, it certifies previously unused **all-integer coordinate congruences** on every possible norm-one unit for each of the three reduced coefficients.

For positive integers d and any odd prime p dividing d:
```
x² − dY² = 1  ⇒  x² ≡ 1 (mod p)  ⇒  x ≡ +1 or −1 (mod p).
```
The second implication uses the fact that p is prime, so (x−1)(x+1)≡0 in the field of p elements.

### Exact prime-support CRT results

| Group | Known prime divisors of reduced d | M | Allowed x residues modulo M | Original factor s | Recovery E |
|---|---|---:|---|---:|---:|
| 1 | 3,13,1693 | 66027 | 1,8464,22010,30473,35554,44017,57563,66026 | 5 | 3 |
| 2 | 3 | 3 | 1,2 | 7 | 3 |
| 3 | 12097,87083 | 1053443051 | 1,246270725,807172326,1053443050 | 4 | 2 |

Every listed divisor is an **individually verified prime** (exact trial division) and divides its stated coefficient exactly. The primes in each row are pairwise distinct. CRT enumerates all sign choices, giving exactly 8, 2 and 4 allowed residue classes. These congruences are necessary for every genuine integer norm-one unit; they do not assert such units exist.

### Exact integer transfer gate

For a **supplied, genuine, nontrivial** reduced unit `(x,Y)` satisfying `x²−dY²=1` and `Y≠0`, compute `U^E = X+Y_E√d` at the appropriate E (3,3,2). Verify `s|Y_E`, set `y=Y_E/s`, and check `X²−(s²d)y²=1`. The Python verifier implements this candidate acceptance path but none was provided or found in this turn. An original norm-one unit is **not** a generalized Pell norm-target seed; the separate `z≡h mod D` and original norm−2 integer-coordinate gates remain.

### Evidence and limitations

- Independent all-integer 3-group arithmetic replay and machine-readable CRT residue certificate.
- RQT-634 local input SHA-256 preserved in the certificate.
- Result SHA256: `587aa77f1864907ce3e328780c225a09b1732db64dd8e2e857bb6e2f0d12dadf`.
- This covers **16** of the **27** canonical unresolved sign-orbits. The other 11 belong to the two coefficients without these extracted square factors.
- No new whole-family exclusion, numerical unit, generalized Pell seed, integer norm−2 root, or original 22D Wall replay.

Selected-family ledger remains **82/135 excluded all-scale (60.74%), 53 unresolved**, mapped into 27 canonical sign-orbits. Root 19 **OPEN**.

## Next natural bound — RQT-636

Combine the exact prime-support constraints with the original-unit coordinate recovery gate, and evaluate a structurally different norm-one unit construction algorithm. Only promote a candidate if the full integer norm directly verifies, and only promote an original norm−2 vector after its original quadratic coordinate and 22D recovery gates pass.

`{brace{n}[box[n](torroid(n))]} · {{i}} · .dlw`
