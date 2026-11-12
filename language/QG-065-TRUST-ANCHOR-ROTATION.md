# QG-065 — Trust Anchor Rotation

## Invariant

**Replacing a trusted key must not erase the chain that established authority.** QG-064 verifies one independently pinned Ed25519 public key. QG-065 permits an explicit, forward-only transition to a **different** key only when the currently trusted key and the incoming key both sign the same transition payload.

```text
        SEPARATE GENESIS PIN
                |
        CURRENT TRUST KEY
                |
        ROTATION PAYLOAD
          /          \
       OLD SIGN     NEW SIGN
          \          /
         BOTH VERIFY?
          /          \
        YES           NO
         |             |
      CHECK LINK      REJECT
         |
    CHECK SEQUENCE FLOOR
         |
      APPEND NEW EPOCH
         |
    HISTORICAL MANIFESTS
      OLD KEY   NEW KEY
         \       /
         PRESERVE ALL
             |
           {{i}}
```

### Transition rule

A rotation payload is serialized using canonical recursively sorted-key JSON and includes `schema`, sequential integer `sequence`, the retiring key's fingerprint, the incoming public JWK and fingerprint, and a SHA-256 `previousHash` linking to the preceding transition (or the literal genesis marker). Both Ed25519 signatures cover the **identical** transition bytes. The next key must differ from the previous one, and the chain verifier starts from a separately supplied trusted genesis JWK.

The ledger retains all historical public keys and signatures. Source manifests are themselves QG-064 signed envelopes and are recorded with a `keyEpoch` and a strictly increasing revision. A historical manifest is always verified against the public key for **its recorded epoch**; rotating never re-signs the original manifest or rewrites its old signature.

### Rollback and security boundaries

An external caller supplies `{publicJwk, minSequence, minManifestRevision}`. Replaying an earlier valid ledger is detected **only if** the independent minimum sequence/revision has been durably advanced. Without such a separately maintained floor, a cryptographically valid old state could be replayed. QG-065 is an append-by-value deterministic simulation, not an external immutable log, durable counter or production key-management service.

The prototype models ordinary authorized rotation where both old and new private keys are available. It intentionally does not handle recovery when the old private key has been lost or compromised; that requires separately specified multi-party recovery authority and revocation rules. Dual signatures demonstrate control of keys, not physical identity of a publisher. As in QG-062–064, GitHub and 0root.ai are one owned ancestry, and public-internet evidence still needs independent policy, source-admission and ancestry checks. No real credentials are accessed or changed.

```sh
node --test tests/signed-trust-anchor.test.mjs tests/trust-anchor-rotation.test.mjs
```
