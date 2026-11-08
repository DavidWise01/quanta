# QG-015 — Authenticated Chrome Dot Transport

**Status:** Executable software protocol prototype, built by composing existing QG-014 and QG-013 modules; not independently security audited.

## End-to-end boundary

\`\`\`text
128 original bits
      ↓  QG-014 reversible XOR folding
1 displayed terminal parity bit + 127 witness bits
      ↓  serialize provenance-linked frame
      ↓  QG-013 reversible spiral address permutation
      ↓  AES-256-GCM encryption and authenticated header
ENCRYPTED ENVELOPE
      ↓  AES-GCM authentication and decryption
      ↓  inverse address permutation
1 terminal bit + 127 witness bits
      ↓  QG-014 inverse fold
128 ORIGINAL BITS (exactly)
\`\`\`

## Five required guarantees

1. **Recoverability:** the terminal bit plus 127 witness bits restores every source bit. The dot alone cannot.
2. **Provenance:** a sourceTag travels inside the encrypted authenticated message. It is a self-declared label, not independently proven identity.
3. **Route identity:** dimension, signature \`12|8/64/3|2/16/8|/4/2/1/1\`, and route version are included in authenticated header data.
4. **Integrity:** AES-GCM rejects wrong keys and modified authenticated data with overwhelming probability, assuming a sound implementation and unique randomly generated nonces.
5. **Fixed point:** the final state is \`1 → 1\`; no new witness bit or node is created.

The underlying bit-width schedule remains **128,64,32,16 | 8,4,2,1 | 1**, divided into two chunks of four values and a terminal witness.

## What is not established

- An unauthenticated witness frame is **not tamper evident**: someone can change bits while maintaining a valid new fold. Use the authenticated envelope.
- A sourceTag is **not a signature** and does not independently prove the claimed human or system origin.
- AES-GCM password-based encryption is **not** a novel QUANTA cryptographic primitive. This remains a learning and prototyping interface, not independently reviewed for high-stakes secrets.
- 11D means a mathematical transport-address model, not experimental evidence for string or M-theory dimensions.
- Full message recovery is not compression to one bit: the 127 retained witness bits carry the missing information.

## Files

- [Executable module](./authenticated-chrome.mjs)
- [Automated tests](../tests/authenticated-chrome.test.mjs)
- [Visual console](../authenticated.html)
- [QG-014 recoverable fold](./QG-014-RECOVERABLE-FOLD.md)
- [QG-013 spiral specification](./QG-013-DOWNWARD-SPIRAL.md)
