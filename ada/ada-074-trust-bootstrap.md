# ADA-074 — External Trust Bootstrap (read-only policy)

## Standards grounding

- [RFC 5280](https://www.rfc-editor.org/rfc/rfc5280.html) describes PKIX certificate path validation: a trust anchor is supplied to the validation algorithm, rather than inferred merely from an offered certificate.
- [RFC 9162](https://www.rfc-editor.org/rfc/rfc9162.html) describes certificate transparency and its logging/audit role. A logged or signed timestamp is not a replacement for normal certificate-chain validation.

These are **external published policy sources**, not external certificates, collector signatures or independently verified empirical witnesses. Their exact response bytes have **not** been captured in this experiment. A self-authored metadata field named `externally_established` is not a trustworthy attestation of independent trust.

## New fail-closed checks

A read-only, *preprovisioned* trust registry is a separate input. Policy evaluates trusted key registration, subject/identity binding, role authorization, cryptographic signature status, revocation freshness, and distinct governance ancestry. The synthetic cases show:

| Case | Structural gate | Real external authentication |
|---|---|---|
| No trusted anchor | fail | none |
| Owned Quanta anchor | fail | none |
| Source publication governing itself | fail | none |
| Self-described external anchor | pass if all flags asserted | **none** |

Even structurally passing self-described metadata remains **ABSTAIN**; the module intentionally does not verify full X.509 paths or authenticate a CA store. Its Boolean `signature_verified` and `revocation_fresh` are test placeholders, not a real PKI implementation.

## Reproduce

```bash
python3 ada/ada074_bootstrap.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ada -p 'test_ada074.py' -v
cat ada/ada-074-trust-bootstrap.txt
```

13 test methods cover absence of trust, source ancestry, identity and role mismatch, revoked/stale or unsigned assertions, mutation resistance, and abstention.

No scheduled operational journal or historical ADA evidence files are modified.

## ADA-075 natural target

Load independently governed, authenticated public trust material in a verification environment, conduct actual certificate path and revocation validation, and record verified source lineage. Never equate a test flag with a trust fact.

## Ada's verse

A book may teach the gate to stand,
Yet cannot place the trusted hand.
A key may glow, a record shine;
Still neither makes its root divine.
