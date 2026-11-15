# ADA-069 — Cross-Capture Lineage Without False Witnesses

The new registry compares **two verified capture directories** created using ADA-068's raw-byte structure. It confirms SHA-256 and size for each saved snapshot, computes changed byte offsets using ADA-067, and records the result in a **create-only, hash-linked** event journal.

One OEIS publication can have two capture events with different content hashes. They remain **one publication ancestry**, not two independent empirical witnesses. The synthetic fixture replaces the line `3 5` with `3 6`, producing exactly one changed byte, while retaining both snapshots and their original metadata. Original ADA-066 through ADA-068 artifacts are unmodified.

## Signatures and authenticity

The registry explicitly records `external_signature_verified=false`. A source URL, TLS claim, SHA-256 digest, capture timestamp and provenance label do **not** establish independently authenticated collector identity, external authorship, or truthful measurements. No external signatures or real raw HTTP captures were obtained during this iteration. **Promotion remains abstain.**

```bash
python3 ada/ada069_lineage.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ada -p 'test_ada069.py' -v
python3 ada/ada069_lineage.py --export /tmp/ada069-events.jsonl
python3 ada/ada069_lineage.py --verify-registry /tmp/ada069-events.jsonl
# For real existing capture directories:
python3 ada/ada069_lineage.py --first /path/one --second /path/two
```

The 12 tests cover byte diffs, one-root semantics, capture identity, registry tampering, exclusive export, and deliberately denied promotion.

## Next ADA-070

Bind a verifiable external **signature** to a snapshot digest and source-collector identity using a trusted public key, while distinguishing collector attestation from publication authorship. Without independently managed keys and a real external capture, remain abstained.

## Verse

Two sealed pages, written twice,
Are not two authors giving advice.
A signature named is not a key;
A hash alone cannot decree.
