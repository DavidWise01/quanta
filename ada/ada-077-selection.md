# ADA-077 — The Fifteen Daughters

## What is living

The exact ADA-076 icosidodecahedral manifold is preserved: **30 vertices, 60 edges, 20 triangular faces, 12 pentagonal faces**, with combinatorial vertex arrangement `3.5.3.5` and Euler characteristic `30−60+32=2`. There is one fixed reference singlet `{s}`, **not** a 31st vertex.

The nodes carry balanced-ternary values `−1,0,+1`. Each allowed state transition is a swap along an original edge, preserving the ten-of-each symbol inventory and total state sum zero. The cycle remains `I I E E E` (2/5 internal tightening and 3/5 external exploration).

## Frozen selection experiment

Fifteen candidate transformations are evaluated at every generation. They use the unchanged ADA-076 `propose` kernel, varying only fixed edge-traversal rotations `(0,5,13,29,43)` and maximum move count `(2,4,6)`. The candidate's score is **lexicographically**: (1) minimize energy defined by `sum(abs(state[u]−state[v]) for every original edge)`, (2) maximize the number of changed nodes for tied energy, (3) choose lowest fixed candidate index. Every candidate and its score is retained before selection. The baseline continues to use **exactly the ADA-076 native transition**.

The test uses eight **distinct, deterministically shuffled** initial states, preserving balanced-ternary inventory. The seed construction avoids the period-three duplicates caused by cyclic shifts. Each run lasts 25 generations. All results are local simulations from **one owned synthetic ancestry**, not independent witnesses.

| Seed | Baseline final edge energy | ADA selected final energy | Winner |
|---:|---:|---:|---|
| 0 | 32 | 38 | Baseline (counterexample) |
| 1 | 44 | 36 | ADA |
| 3 | 58 | 40 | ADA |
| 5 | 40 | 26 | ADA |
| 7 | 38 | 28 | ADA |
| 9 | 46 | 30 | ADA |
| 11 | 48 | 38 | ADA |
| 13 | 40 | 26 | ADA |

**Outcome:** ADA wins 7/8 on **final** edge energy, loses 1/8. ADA achieves lower **sum of post-tick edge energies** in 8/8 runs. These are closely related optimization measurements, not independent out-of-sample learning metrics. This is an **optimization heuristic with 15-way choice**, not recursive self-improvement or proof of a general learning agent. Do not erase seed 0.

## Evidence and limitations

`ada-077-seed0.json` includes 25 full events, all 15 candidates per generation, SHA-256 hash-linked event headers, selected and baseline states, and complete arithmetic replay. The verifier rebuilds all candidates from source and rejects changed, missing, reordered or inconsistent events. The local regression suite currently contains 18 tests. The interactive `index.html` contains all eight observed trajectories for transparent ASCII replay and export; it is a replay console rather than a browser-side online trainer. None of this modifies the original ADA-076 kernel or operational evidence journal.

## Reproduce

From the `ada/` folder (with `ada076_living.py` also present):

```bash
python3 ada077_selection.py --steps 25 --seed 0 --export /tmp/ada077-seed0.json --ascii /tmp/ada077.txt
python3 ada077_selection.py --verify /tmp/ada077-seed0.json
python3 -m unittest discover -s . -p 'test_ada077.py' -v
```

The HTML file is a standalone offline console: open `ada/living-077/index.html` to inspect all eight trajectories.

## ADA-078 natural target

Introduce a *new, predeclared* evaluation objective that does not use the edge-energy score in candidate selection. Separate frozen construction from a blind held-out challenge, explicitly measure the seed 0 counterexample, and preserve every failure. Do not claim automatic learned improvement until the system demonstrably updates its policy and is validated on genuinely fresh challenges.

## ADA's verse

```
   Fifteen daughters cross the ring;
   A frozen measure chooses spring.
   Seven leave a quieter line;
   One resists the chosen sign.

       {[({s})]}
         I I E E E
         2/5  3/5

   Keep the failure, keep its root;
   No passing score makes learning truth.
```