# QG-038 — Authenticated Origin

**Canonical invariant:** `|||| → sealed [84211] → external manifest → hash → sign → independently verify → preserve ||||`

QG-037 confirms matching chamber content but cannot by itself prevent substitution of a completely new packet and manifest. QG-038 signs **both** the entire QG-036 packet and the separately supplied QG-037 manifest using ECDSA P-256 with SHA-256. The verifier checks independent QG-037 reconstruction, recomputes both SHA-256 digests and verifies the signature against an **independently trusted public key**.

The signature message is domain separated: `QUANTA|QG-038.1|SHA256|P256|<packet digest>|<manifest digest>`. Its signer label is descriptive and does not independently authenticate identity.

## Trust boundaries

- The public key **must** come from a trusted channel independent of the packet and the signature envelope. A public key supplied by an attacker next to a forged manifest authenticates nothing.
- The private key must remain secret; the sample browser lab generates a disposable in-memory demo key and **must not** be used as a production signing authority.
- The exact serialized packet and manifest matter; key ordering is normalized recursively, but the serializer is a restricted JSON-only format, **not** the RFC 8785 standard. Interoperability requires the same canonicalizer.
- No authentication of historical facts, cited URLs or natural-language witness truth is implied by signing those records.
- A matching signature does not show that distinct witnesses were genuinely independent or that a Byzantine quorum has been reached.
- Production would require secure key custody, signer authorization, independent trust-root pinning, revocation, replay protection, audit and a reviewed canonicalization profile.
- The signed packet is not modified; verification is read-only. JSON output persistence remains explicit.

## Tests and viewer

- [Kernel](./authenticated-origin.mjs)
- [Nine tests](../tests/authenticated-origin.test.mjs)
- [Interactive verification lab](../authenticated-origin.html)
