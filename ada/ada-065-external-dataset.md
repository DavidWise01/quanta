# ADA-065 — Externally Published Orbit Values

## Sources

- **OEIS A003095**: https://oeis.org/A003095 (independent published reference sequence for `a(n+1)=a(n)^2+1`, starting at zero).
- **Plus Maths, What is the Mandelbrot set?**: https://plus.maths.org/comment/8560 (published worked finite sequences for `c=0`, `c=-1`, and `c=1`).

The sources provide reference **numeric values** in addition to the recurrence. ADA-063's already-existing `evolve` implementation computes the actual values without reusing the expected sequence as computation input. Exact values match 4/4 transcribed reference cases.

Two publications are two external *reference ancestry roots*, not three laboratory witnesses. The `c=1` cases overlap and cannot be double-counted as independent novel measurements. The reference web pages were consulted on 2026-11-15, but their **original response bytes and snapshot hashes have not been archived**; the fixture preserves URLs, manually transcribed values, and the capture date. No artificial claim of external independent empirical verification is made.

## Run

```bash
python3 ada/ada065_published_replay.py
python3 -m unittest discover -s ada -p 'test_ada065.py' -v
cat ada/ada-065-external-dataset.txt
```

All computation uses Python exact integer/rational arithmetic. Results are finite checks and do not prove global boundedness, Julia/Mandelbrot physical equivalence, or quantum behavior. ADA remains unpromoted pending independently verified physical/empirical evidence.

## ADA-066

Archive immutable source-response bytes and independently scoped capture metadata. Validate capture hashes and detect changed content. Do not turn duplicate captures of one publication into independent witness roots.

## Verse

The distant page records the seed;
The local wheel repeats the deed.
Agreement sings, but does not swear
Three separate watchers stood out there.

-- A.D.A --
