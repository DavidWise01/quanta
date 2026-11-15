# ADA-067 — Temporal Source Integrity Without Double Counting

## Result

The ADA-066 pinned 51-byte normalized OEIS excerpt remains unchanged and verifies against SHA-256 `7ccd51e94cae1ec6d1fc0df3fce2d4adfb8737b618f9ea243c404c950f232169`.

A fresh request for `https://oeis.org/A003095/b003095.txt` was denied with HTTP 403 on this turn. **No second raw capture was obtained**. This is an access result, not evidence that the source content changed.

The verifier runs three *clearly synthetic* comparisons against the frozen ADA-066 bytes:

| Diagnostic | Result | Byte offsets changed |
|---|---|---|
| Identical bytes | identical | 0 |
| Synthetic `5 677` -> `5 678` | content_changed | 1 |
| Remove last newline | length_changed | 1 |

The event stream is hash-linked, ordered, create-only upon export and never replaces the ADA-066 baseline. Every event retains the same publication ancestry `OEIS:A003095`: new capture time != new independent witness. There are no real independent empirical witnesses; promotion remains **abstain**.

## Reproduce

```bash
python3 ada/ada067_temporal.py
python3 -m unittest discover -s ada -p 'test_ada067.py' -v
python3 ada/ada067_temporal.py --export /tmp/ada067-events.jsonl
python3 ada/ada067_temporal.py --verify /tmp/ada067-events.jsonl
```

Twelve tests check bytes, delta offsets, failure preservation, digest-chain tampering, append-only exclusive export and no false promotion. The new experimental events are *not* written into the operational ADA scheduled ledger.

## ADA-068

Use a raw-byte-capable collection endpoint with authenticated response metadata or a separately archived third-party immutable snapshot; preserve upstream responses as distinct objects without conflating capture instances and source ancestry.
