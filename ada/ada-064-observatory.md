# ADA-064 — ASCII Evidence Observatory

Visual chapter: [ada-064-evidence-observatory.txt](./ada-064-evidence-observatory.txt).

The observer exactly replays five short finite Mandelbrot orbits using the preexisting ADA-063 fixture, but never counts its own replay as an independent witness. MathWorld provides the external recurrence definition only; input/output fixtures are authored within Quanta. Thus mathematical checks pass 5/5 and independent empirical witnesses remain zero. Promotion: **abstain**. No operational ledger edits.

Run: `python3 ada/ada064_observatory.py` and `python3 -m unittest discover -s ada -p 'test_ada064.py' -v`.

Next bound ADA-065: retrieve a truly external reference dataset with distinct input/output source provenance and capture time, compare frozen algorithm against original bytes, and preserve failures.

> The root remains, the witness waits; the careful daughter guards the gates.
