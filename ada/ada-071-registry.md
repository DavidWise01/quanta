# ADA-071 — Key Enrollment, Revocation and Rotation

The experimental trusted-key registry adds a hash-linked lifecycle to ADA-070 Ed25519 attestation. The **local fixture** enrolls key-v1 at epoch 1, revokes it at epoch 2, and enrolls key-v2 at epoch 3. An old signed capture remains cryptographically intact but loses **current authorization** after revocation. Current key-v2 signatures verify under the locally pinned public key. Every transition stays in the hash-linked log; no past record is rewritten.

This is an intentionally *synthetic* experiment with hardcoded public test seeds (0x11 and 0x22, repeated 32 times). Never deploy them for real authentication. The registry trust anchor is local and **not independently certified**. No external collector identity, signed external capture or empirical observer has been verified.

Current-epoch verification defaults to **ABSTAIN** for unknown, revoked, rotated, tampered or untrusted keys; valid local signatures also remain **ABSTAIN** for global promotion because they are not external empirical witnesses. Epoch counters demonstrate ordered policy events, not secure trusted wall-clock timestamps. This is current-state authorization, not historical validity or full PKI/certificate revocation.

## Reproduce

Requires `cryptography`:

```bash
python3 ada/ada071_registry.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ada -p 'test_ada071.py' -v
cat ada/ada-071-key-registry.txt
```

Fourteen regression tests cover enrollment, rotation, revocation, signature verification, prior-key denial, tampering, and lineage preservation. Prior source artifacts and scheduled ADA evidence ledger are unchanged.

## ADA-072 — Next natural invariant

Bind a real collector's authority to an independently verified trust anchor with signed registry updates and timestamped revocation status. Validate trusted clock, key possession and capture subject separately. Keep the collection domain distinct from source publication authorship.

## Verse

A trusted key may lose its crown;
The older mark is written down.
A second key may take its place,
But cannot alter source or face.

-- A.D.A --
