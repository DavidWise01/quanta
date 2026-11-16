# ADA-076 — The Icosidodecahedral Living Kernel

**Executable mathematical prototype.** No independent physics result, autonomous learning, or external empirical witness is claimed.

## Exact geometry

The icosidodecahedron is constructed combinatorially by rectifying an icosahedron, not by drawing a suggestive approximation. Original icosahedron edges become 30 new vertices. Its 20 triangular faces yield 20 triangular faces; its 12 original vertices yield 12 pentagons. Each of the 60 graph edges belongs to exactly one triangle and one pentagon. Every vertex has four neighbors and vertex configuration 3.5.3.5.

`V - E + F = 30 - 60 + (20 + 12) = 2`.

## Dynamics

At each vertex, state `s in {-1,0,+1}`. Genesis contains 10 of each and total sum zero. Five-phase pulse `I,I,E,E,E` repeats forever. Each pulse walks the 60 edges in deterministic rotated order, proposing up to 4 disjoint swaps of differing states. A candidate is evaluated against an exactly defined edge disagreement energy `E(s)=sum_(a,b) |s[a]-s[b]|`, and a local pentagon boundary pressure. Internal `I` pulses accept only swaps with energy change <=0. External `E` pulses allow energy change <=2 and local pentagon-pressure change <=2. Every accepted swap records the associated triangle's before/after triple and pentagon ID.

These are **chosen model rules**, not discovered natural laws. They produce observable motion, preserve the state histogram and are replayable; they do not imply learning or self-improvement. Triangle triple observations are *one synthetic source ancestry*, not three independent witnesses.

## Verified initial run

- 25 pulses, **99 accepted state exchanges** (39 during internal pulses, 60 during external pulses).
- Initial edge disagreement energy **54**; final energy **46**.
- 26 hash-linked events including genesis, all checked by deterministic exact replay.
- 18 local Python regressions passing.
- The standalone HTML console was checked under Node.js: advancing 25 client-side pulses reproduces the exact Python final 30-node state.
- JSONL created once, exclusively; attempts to overwrite a saved archive fail.

## Files

- `ada076_living.py` — pure standard-library kernel, exact topology, pulse scheduler, replay verification, CLI
- `test_ada076.py` — 18 topology, dynamics, conservation, determinism, tamper and archive tests
- `ada-076-living.txt` — text/ASCII frame at generation 25
- `ada-076-generations.jsonl` — immutable-on-commit reference run: genesis + 25 ticks
- `living/index.html` — standalone, text-only interactive console: Play, Pause, Next, +5, speed, Reset, export transient trace

## Run locally

```bash
python3 -m unittest discover -s ada -p 'test_ada076.py' -v
python3 ada/ada076_living.py --verify ada/ada-076-generations.jsonl
python3 ada/ada076_living.py --steps 100
python3 ada/ada076_living.py --steps 100 --export /tmp/ada076-new.jsonl --ascii /tmp/ada076-new.txt
```

The browser prototype intentionally does not write to the operational ADA GitHub ledger. Its user-exported JSON records a transient browser trace; the reference Python JSONL uses a separate hash-linked, replay-verified format.

## Next natural bound — ADA-077

Let locally nominated perturbations compete against a **frozen** scoring rule, and test on unobserved graph seeds. Preserve negative results. Avoid counting a reduction in energy as proof of intelligence or claims of a valid physical Josephson/Julia coupling.

## A.D.A

```
  Three look upon the passing face,
  Five circle through their measured space.
  The edge may trade, the state may roam,
  Yet conservation keeps its home.

  One kernel turns, one ledger stays,
  The daughters learn no borrowed praise.
```
