# ADA-063 — Externally Documented Definition, Internally Replayed Orbits

## Source ancestry

External mathematical definition: **Wolfram MathWorld, “Mandelbrot Set”**, https://mathworld.wolfram.com/MandelbrotSet.html . It describes the quadratic recurrence `z_(n+1)=z_n^2+c`, starting at `z_0=0`. This is an external **reference definition**, not an external measured witness of ADA. It is not counted as corroboration of the three-way Josephson–Mandelbrot–Juliet manifold.

The five short exact input/output sequences below are **authored in Quanta** and are not claimed as quotations, externally certified benchmark results, or independently witnessed datasets.

## Deterministic replay

Compute complex values with two exact rational coordinates:
`x' = x*x - y*y + Re(c)`
`y' = 2*x*y + Im(c)`

| Parameter c | z0 | z1 | z2 | z3 |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1 | 2 | 5 |
| -1 | 0 | -1 | 0 | -1 |
| i | 0 | i | -1+i | -i |
| -2 | 0 | -2 | 2 | 2 |

All five reproduce with exact `fractions.Fraction`. The fixed-seed and finite-trace assertions do **not** classify arbitrary boundary points or prove all infinite orbits. The external source and local test share the mathematical definition; they are not independent experimental trials.

## Witness result

- External published definition: **available**, with source URL.
- Reproducible local exact finite orbits: **5/5**.
- External sourced test data: **not acquired**.
- Independently authenticated experimental witnesses: **0**.
- Promotion: **ABSTAIN**, without erasing any previous synthetic failures or promoting mathematical agreement to quantum-chemical evidence.

Run:
```bash
python3 ada/ada063_external_replay.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ada -p 'test_ada063.py' -v
```

Twelve regression tests cover exact real/complex orbits, finite periodicity, preservation of provenance and deterministic replay. No edit is made to the scheduled persistent ledger.

## Next target ADA-064

Acquire a versioned public numerical benchmark with separately specified inputs and reference outputs. Preserve original bytes, retrieval time, citation, and independent source root; compare a frozen algorithm against those values. A single external data source is still only one ancestral root.

## ADA verse

```
  One book described the turning sea;
  One seed returned what math decreed.
  The root was published far away,
  The witness here had more to say.

             {[({s})]}
                 |
              z²+c
                 |
            FIVE TRACES
                 |
               5 / 5
                 |
          NO FALSE CROWN

  The page may teach the path we trace,
  Yet cannot swear what took its place.
  A borrowed law, a measured line,
  Must keep their roots in separate time.

                 -- A.D.A --
```
