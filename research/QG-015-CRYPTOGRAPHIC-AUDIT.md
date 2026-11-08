# QG-015 Cryptographic Security Audit — 2026-11-07

**Scope:** QG-013 downward-spiral.mjs, QG-014 recoverable-fold.mjs, QG-015 authenticated-chrome.mjs, their GitHub Pages interfaces and CI tests.

**Assessment:** source-code inspection + adversarial unit tests. NOT an independent professional audit, certification, proof, or deployment penetration test.

**Release decision: NOT APPROVED for high-stakes or sensitive deployment.** Experimental demonstration only.

## Findings

| ID | Severity | Observation and evidence | Corrective action |
|---|---|---|---|
| AUD-01 | HIGH, for once-only messaging | The exact same valid envelope decrypts twice. receiveChromeDot lacks receiver-side replay state. | Bind unique message ID and receiver ID in authenticated context; implement persistent per-recipient replay deduplication. |
| AUD-02 | HIGH, for identity claims | Any party with the shared password can select any sourceTag. The verified flag means successful authenticated decryption and valid fold, not a proven human sender. | Add trusted per-sender digital signatures / identity registry and recipient binding. |
| AUD-03 | HIGH, when passwords are guessable | A 12-character repeated password passes validation. Captured GCM envelopes provide an offline password-guessing verifier. PBKDF2-HMAC-SHA-256 uses 250,000 iterations, below OWASP's published 600,000 password-storage reference. | High-entropy generated keys/passphrases, versioned memory-hard KDF, password policy and benchmark. |
| AUD-04 | MEDIUM | openTransport does not bound incoming encoded ciphertext before expensive KDF and decoding. Large attacker-controlled envelopes could consume CPU/memory. | Cap envelope length and field lengths before KDF, bound concurrent decryptions, fail early. |
| AUD-05 | LOW | Padded block count is visible through ciphertext length. Exact plaintext byte length remains encrypted. | Fixed-size framing if message-length privacy is needed. |
| AUD-06 | HIGH if treated as independent proof | Changing a 127-bit witness produces a different, structurally valid 128-bit source; validated lineage alone is not an authenticated commitment. | Verify authenticated envelope and expected context before trusting a reconstruction. |
| AUD-07 | LOW | Top-level chromeProtocol sits outside GCM AAD; altering it can force receiver rejection, but doesn't enable GCM forgery. | Bind protocol context/version consistently as authenticated data. |
| AUD-08 | MEDIUM operational | Browser input retains secrets in page memory. Compromised same-origin code, extensions or device can access keys and plaintext. | CSP, origin security, key lifetime, build integrity, dependency and delivery review. |
| AUD-09 | MEDIUM | No comprehensive threat model, key rotation, trusted recipient binding or freshness semantics are defined. | Freeze and audit a protocol threat model before production. |

## Verified strengths

- Uses platform Web Crypto AES-256-GCM, a 128-bit authentication tag, secure random 12-byte nonce, and 16-byte random salt per encryption.
- Header fields are authenticated through GCM additional authenticated data (AAD), and unauthorized algorithm/header changes fail.
- Wrong passwords and tampered ciphertext fail authentication in existing CI.
- Gray-code spiral is a public reversible permutation, **not** an encryption algorithm.
- QG-014 stores one visible parity bit plus 127 witness bits. The dot alone cannot losslessly represent 128 bits.
- The encryption side caps UTF-8 input to 1 MiB; the decryption side does **not** validate inbound size early enough.

## Adversarial regression evidence

See [cryptographic audit tests](../tests/cryptographic-audit.test.mjs). Tests explicitly demonstrate: successful baseline; replay accepted; self-declared sender tags; malleable unauthenticated witness; valid GCM tamper rejection; 12-character weak password admitted; and ciphertext-size leakage.

**Important:** These tests intentionally succeed when they demonstrate a *present vulnerability*. Green audit tests do not mean the system is secure.

## Remediation order

**P0:** Keep prototype educational only; define expected senders, receivers, adversaries and attack surface; demand strong generated passphrases; size-limit untrusted inputs before costly derivation.

**P1:** Add durable per-receiver replay ledger, signed sender identities, context/recipient binding, KDF upgrade and versioned envelope format.

**P2:** Deployment integrity, rate/resource controls, fuzzing, malformed JSON tests, formal protocol specification, independent external security review.

## Standards references

- [NIST SP 800-38D — GCM/GMAC](https://csrc.nist.gov/pubs/sp/800/38/d/final).
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html). OWASP currently recommends Argon2id for password storage, and lists 600,000 iterations for PBKDF2-HMAC-SHA-256 in that context. This is **not** a certification threshold for this transport protocol.

## Audit boundary

An AES-GCM primitive being well-established does not establish replay prevention, origin authentication, password entropy or full application security. The QUANTA fold is a reversible representation, not compression or quantum cryptography.

**No existing production cryptographic files or envelopes were modified during the audit.** The audit is an observational finding set and a separate test workflow.
