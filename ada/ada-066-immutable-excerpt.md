# ADA-066 — Immutable Reference Excerpt

The source [OEIS b003095](https://oeis.org/A003095/b003095.txt) exposes published values of the sequence beginning `0,1,2,5,26,677,458330,210066388901`.

**Capture limitation:** Direct HTTP byte retrieval was unavailable in this execution environment. This artifact is an 8-line, normalized UTF-8 transcription from the web-readable source, **not a raw upstream response snapshot**. The source capture date is 2026-11-15; no original response headers or original byte stream are attested.

The 51-byte committed excerpt is SHA-256 pinned to `7ccd51e94cae1ec6d1fc0df3fce2d4adfb8737b618f9ea243c404c950f232169`. A separately versioned manifest states the source URL, transcript method, original-authentication limitations, and one publication ancestry. Replaying `z -> z²+1` from zero matches all 8 indexed terms.

The six regression tests require the exact capture hash, reject truncation and modified text, preserve the source excerpt and prohibit external-witness promotion. This verifies **archived transcription integrity**, not independently authenticated measurement or source truth. Existing operational ledger remains untouched.

Run:
```
python3 ada/ada066_capture.py
python3 -m unittest discover -s ada -p 'test_ada066.py' -v
```

Next ADA-067: acquire and pin a truly raw upstream response plus its HTTP metadata through an allowed environment, retain the original bytes separately, and test semantic change across independent retrievals. Avoid calling multiple copies of OEIS independent witnesses.
