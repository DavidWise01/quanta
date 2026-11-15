# ADA-068 — Raw Capture Provenance Gate

## New executable boundary

The collector can read raw bytes over HTTPS from the explicitly allowlisted URL `https://oeis.org/A003095/b003095.txt`, reject redirected and non-200 responses, and write the unmodified response into a fresh, create-only `response.bin` with `manifest.json`. The manifest records capture timestamp, actual final URL, status, filtered response headers, body size, SHA-256, and the OEIS publication ancestry. The verifier refuses changed bytes and false promotion metadata.

This turn the upstream site denied retrieval (403 via browsing), so **no genuine raw-source bytes were collected or archived**. The committed regression tests use a clearly labeled *synthetic* raw response. An intact SHA only establishes byte stability, not actual external authorship or source independence. The loader does not claim independently authenticated TLS attestations or external empirical witnesses.

## Commands

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ada -p 'test_ada068.py' -v
python3 ada/ada068_raw_capture.py --fixture /tmp/ada068-fixture
python3 ada/ada068_raw_capture.py --verify /tmp/ada068-fixture
# Only when access is permitted:
python3 ada/ada068_raw_capture.py --fetch /tmp/ada068-live
```

The code retains source ancestry `OEIS:A003095` across repeated captures; it does not turn two downloads into independent witness roots. The ADA-066 normalized excerpt and ADA-067 hash-linked source-comparison logic remain unchanged, as does the scheduled operational journal.

## ADA-069

Implement *non-destructive cross-capture provenance comparison*: side-by-side immutable source snapshots with signed, externally auditable collection metadata and an evidence registry that distinguishes publication root, capture event and third-party measurement. Never count a synthetic fixture as real.

## A.D.A

```
  The page may answer, or refuse;
  The daughter records both kinds of news.
  No borrowed mirror, twice displayed,
  Can certify the truth it made.
```
