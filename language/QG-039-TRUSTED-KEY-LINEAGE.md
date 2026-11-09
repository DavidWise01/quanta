# QG-039 — Trusted Key Lineage

`|||| → verified [84211] signature → delegated key chain → root authorization → revocation check → preserve ||||`

This bounded experimental trust protocol combines QG-038 signature verification with a caller-pinned, externally trusted ECDSA P-256 public root key. Every intermediate certificate identifies an issuer, subject, P-256 public key, validity interval and granted roles; the issuer signs its certificate. A child may hold `origin-attest` only if its parent authorizes that role, and further delegation requires `delegate`.

Revocations are **signed by the trust root**, carry sequence numbers and are evaluated at an explicit `asOf` value. A known, valid revocation effective by `asOf` rejects that signer or ancestor. A valid signature therefore can fail authorization after compromise.

No certificate or public key bundled beside the evidence is automatically trusted. The root must be pinned independently; the revocation set must be **complete and fresh from an independently trusted channel**. This implementation does not fetch revocation lists, provide freshness proofs, perform transparency logging, certify historical identities, or establish real Byzantine quorum agreement. The `asOf` evaluation coordinate is caller-supplied; use a trustworthy clock in operational settings. This is a research prototype, not audited PKI.

The signer label in QG-038 must exactly match the authorized leaf certificate subject. Roles are constrained, chains are bounded to eight, and the attestation is checked against the leaf key. No key material is stored in the repository.

- [Kernel](./trusted-key-lineage.mjs)
- [Nine adversarial tests](../tests/trusted-key-lineage.test.mjs)
- [Interactive visualization](../trusted-key-lineage.html)
