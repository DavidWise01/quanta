# QG-050 — Ambiguous Roots

## Invariant: observational equivalence is not identity

```text
     UNKNOWN GENERATOR
            |
     OBSERVE 8-VERTEX RING
            |
       /-----------\
      ROOT 1      ROOT 7
        \           /
         SAME SAMPLES
              |
     KEEP BOTH HYPOTHESES
              |
      MEASURE OFF THE GRID
              |
      DIFFERENT PREDICTIONS
              |
      RETAIN MATCHING ROOT
```

A deliberately small synthetic generator gives radial response `f_k(theta)=0.55+0.45*cos(k*theta)` for candidate integer roots `k=1..8`. A sampled regular `n=8` ring supplies `theta_j=2πj/8`. At all those angles, `cos(theta_j)=cos(7 theta_j)`, so **k=1 and k=7 are observationally indistinguishable on the eight sampled vertices**. The synthetic observer is not told k when inference begins.

The invariant is **retain the entire set of candidates consistent with observations**. No election, majority, or preference can identify the hidden generator when the observations are identical. A bounded set of off-grid angles is evaluated for the largest predicted candidate spread; a new measurement then filters roots. This is active experimental design, not reconstruction of a Mandelbrot, full fractal, or physical hardware.

Tests cover aliased ring roots, distinguishing off-grid measurements, false confidence, contradictory values, append-by-value event replay, tampering, and incomplete data. The numerical comparison uses a fixed tolerance of 1e-9 and is not a proof about arbitrary real-number rounding or all candidate frequencies.

The result is **conditional on the declared candidate class**, which contains only the eight cosine-frequency roots. Other unmodeled rules can mimic the same finite observations. Distinguishing two modeled roots does not prove which physical system produced the data.

### Run

```sh
node --test tests/ambiguous-roots.test.mjs
```
