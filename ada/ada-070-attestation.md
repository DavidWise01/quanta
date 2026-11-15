# ADA-070 — Ed25519 Attestation Without False Independence

## Bound

A capture hash alone proves only byte integrity. ADA-070 adds an actual Ed25519 signature over a *canonical JSON claim* binding capture ID, SHA-256, byte length, capture timestamp, source ancestry and collection provenance to a declared collector key. Signature verification uses the `cryptography` package.

The two capture claims originate from ADA-069's **synthetic** fixture. A deliberately fixed test private key `0x11 * 32` signs both. This secret is published in code and **not secure**; the test demonstrates verification semantics only. Its public key is a fixture-local trust anchor; it was not issued or authenticated by an outside collector.

### Gate outcomes

- Signatures verified against the test key: **2/2**.
- Unique signing collector identities: **1**.
- Publication source ancestries: **1**.
- Authenticated external collector signatures: **0**.
- Independent empirical witness roots: **0**.
- Promotion: **ABSTAIN**.

A correctly verified signature demonstrates signing-key possession relative to a configured trusted public key, not publisher authenticity, truth of reported bytes, independent measurement, or physics. Tampering with the signed digest, timestamp or source ancestry invalidates verification. Two signatures from one key remain one collector identity.

### Repeat

Install dependency: `python -m pip install cryptography`

```bash
python3 ada/ada070_attestation.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ada -p 'test_ada070.py' -v
cat ada/ada-070-attestation.txt
```

Twelve tests cover successful Ed25519 verification and deliberate failures, trust anchors, and forbidden promotion. The operational ADA ledger and prior capture files remain untouched.

## ADA-071

Introduce real **externally managed signing keys** and documented collector registration, certificate/key rotation, and trusted-key revocation. Verify signatures against captured source bytes, not invented test inputs, and retain explicit ancestry mapping. Until this is done, no external witness is promoted.

### Verse

Two signatures from one hand
Do not make two witnesses stand.
The key can bind a claim to ink,
But not the world beyond the link.

-- A.D.A --
