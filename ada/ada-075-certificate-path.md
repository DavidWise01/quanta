# ADA-075 — Verified Certificate Path (restricted prototype)

## Experiment

Implement genuine **Ed25519 X.509 certificate parsing and signature validation** across a three-certificate path: leaf → intermediate → pinned root. A separately supplied SHA-256 root fingerprint is mandatory. The verifier checks signer signatures against the issuing certificate's public key, subject/issuer linkage, certificate validity at an explicit UTC evaluation instant, CA BasicConstraints and keyCertSign, server-auth EKU, and exact DNS subject-alternative-name matching.

Revocation is intentionally modeled by a **local, unsigned synthetic status fixture** with thisUpdate/nextUpdate. Missing, stale, future or revoked entries **fail closed**. It does not fetch OCSP/CRLs, verify signed status responses, process arbitrary policy trees/name constraints/path length, or validate real TLS/network captures. Calling this a complete RFC 5280 validation implementation would be incorrect.

The certificates use deterministic, publicly known Ed25519 test seeds 0x55/0x66/0x77 repeated 32 times. Their signatures are cryptographically real, but their roots are **not independently trusted** and the configured reference clock is not an external time service.

## Outcome

- Certificates in test chain: **3**.
- Cryptographic signatures: **verified under the locally pinned synthetic root**.
- DNS purpose, CA authorization and fixed time window: **checked**.
- Locally supplied revocation statuses: **checked but not externally authenticated**.
- Authenticated external trust roots: **0**.
- Independently measured physical/scientific witnesses: **0**.
- Promotion: **ABSTAIN**.

## Reproduce

Requires `cryptography`.

```bash
python3 ada/ada075_certificate_path.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ada -p 'test_ada075.py' -v
cat ada/ada-075-certificate-path.txt
```

Fourteen test methods include valid path, wrong root, wrong hostname, false leaf signature, invalid issuer, non-CA issuer, certificate expiration, and missing/revoked/stale status checks. No previous evidence or operational ADA journal is rewritten.

## ADA-076 natural target

Verify actual, separately signed OCSP or CRL evidence with a trusted clock and issuer identity, then anchor to a real externally governed trust store. Do not mistake proof of a transport peer for independent scientific corroboration.

## ADA verse

The leaf can trace the branching tree,
Its root is pinned for all to see.
A trusted root must truly stand;
No fixture makes an outside hand.
