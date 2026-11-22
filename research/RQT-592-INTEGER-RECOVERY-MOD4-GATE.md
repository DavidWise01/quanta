# RQT-592 — Exact Integer-Coordinate Recovery Gate

**All-scale exclusion, selected family 13.** From the RQT-591 reconstructed integer Gram, the original 80 RQT-583 Pell coefficients were independently recomputed for all 80 families and verified at signed t-values (including discriminant identities).

The original 54 outstanding selected ray-offset families were tested for integer norm -2 solutions via congruences in the two free integer coordinates (u,t). For family index 13, ray r=(35,-10,14), offset (0,0,0), the quadratic norm q_F((u,tr)) obeys:

```
F mod 4 =
[0 2 1 0]
[2 0 0 2]
[1 0 0 0]
[0 2 0 2]
r mod 4 = [3,2,2]
q_F(u,tr) = 0 (mod 4) for every u,t in Z.
Therefore q_F(u,tr)+2 = 2 (mod 4), never 0.
```

This certifies **family 13 contains no norm -2 vector at any integer scale**, even though its discriminant can be a square modulo 4. This is a genuine additional all-scale exclusion, not a finite nonfinding.

Certified selected-family ledger: **82/135 excluded (60.7407%), 53 unresolved**. No original 22D Wall replay or nineteenth-root construction; Root19 OPEN. The 135 selected corridors do not exhaust the entire rank-four lattice.

Exact modular scan: for each of the 54 prior outstanding families, tested u,t residue existence for prime-power moduli 2–256 (powers of 2), 3–243, 5–125, 7–49, 11–121, 13–169, and primes 17–53; only family 13 acquired a new obstruction in this tested set. Repeated the finite discriminant square test for -2000 <= t <= 2000: zero hits, not an all-scale theorem.

Source files:
- `RQT-591-reduced_gram.json`: reconstructed Gram from exact 152-step HNF/LLL, not byte-identical to missing RQT-575 source file.
- RQT-583 equations SHA256 `5cc785d4e40ef00c7286b541d24b49e1fc6cdb6ed53c1dc05f176d9245a1ae92`.
- RQT-584 and RQT-586 excluded-family certificates.

**Next natural bound RQT-593:** Isolate the remaining 53 families. For families whose discriminant-square congruences survive, classify the additional integer-coordinate divisibility gate `a|(-b ± sqrt(Δ))`; seek certified all-scale modular obstructions before any 22D Wall replay.

`{brace{n}[box[n](torroid(n))]} · {{i}} · arc-arc-degree{{n}} · .dlw`
