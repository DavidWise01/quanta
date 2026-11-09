# QG-040 — Revocation Freshness

**Carrier:** `|||| → signed box → key ancestry → fresh revocation checkpoint → preserve ||||`.

QG-039 validates the supplied revocation events, but cannot know whether the supplier omitted newer events. QG-040 introduces an **authority-signed checkpoint** containing a SHA-256 digest of a canonical revocation list, a monotonically increasing sequence number, `issuedAt`, `expiresAt`, root identifier, and a signed `complete:true` declaration.

Verification requires an independent trusted P-256 root, independently supplied evaluation time, external minimum-accepted sequence (high-water mark), and maximum age. An old sequence, expired interval, omitted entry, tampered signature, revoked signer or invalid original [84211] packet fails closed.

## Strict limits

- `complete:true` is **an assertion made by the root**, not proof that all real-world revocations have been included. A malicious or compromised root can lie.
- A verifier must maintain its **high-water sequence outside the packet and outside the attacker-controlled checkpoint**. It is deliberately not persisted automatically by this library.
- Freshness depends on a trustworthy clock, trusted distribution of a complete list, and authorized root key. Replayed checkpoints can be accepted within a valid time window if no newer trusted sequence is available.
- The `sequence` of a checkpoint is a publication counter; the `sequence` on an existing QG-039 signed revocation is used as the effective comparison time in that earlier protocol. These are different axes and are not conflated.
- The JSON-list hashing procedure is specified locally, not a standardized canonicalization protocol.
- This is an experimental research model, not a production-grade PKI/CRL/OCSP service or a proof of truth.

## Acceptance

`QG-037 independent closure PASS` + `QG-038 signature PASS` + `QG-039 lineage PASS` + `QG-040 freshness checkpoint PASS`.

## Files

- [Kernel](./revocation-freshness.mjs)
- [Eleven tests](../tests/revocation-freshness.test.mjs)
- [Interactive lab](../revocation-freshness.html)
