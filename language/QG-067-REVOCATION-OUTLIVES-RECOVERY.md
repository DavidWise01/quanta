# QG-067 — Revocation Must Outlive Recovery

## Invariant

**A previously valid signature must remain verifiable as historical evidence without permitting its retired signing key to authorize any future operation.**

```text
           QG-066 VERIFIED RECOVERY
                     |
           RETIRED KEY FINGERPRINT
                     |
            REVOCATION CERTIFICATE
             SIGNED BY SUCCESSOR
                     |
           +---------+----------+
           |                    |
      HISTORICAL PROOF       NEW OPERATIONS
           |                    |
      VERIFY WITH OLD       VERIFY ACTIVE KEY
           |                /           \
      PRESERVE HISTORY    SUCCESSOR     RETIRED
           |                |             |
           |               ADMIT         REJECT
           +---------+------+-------------+
                     |
             RECORDED EVIDENCE
                     |
                   {{i}}
```

## Boundary

QG-066 provides a distinct, guardian-authorized recovery path when the old signer is unavailable. QG-067 introduces a **separate successor-signed revocation record** explicitly binding its recovery event, QG-065 historical chain hash, retired key fingerprint, and new successor fingerprint. The status `deny_new_operations_preserve_history` cannot be replaced without breaking deterministic verification and the successor signature.

The original QG-065 manifests are still checked using their historical keys. New operations instead carry an operation ID, monotonic sequence, intended action, active successor fingerprint, signature, and the revocation certificate digest. They are rejected unless (1) recovery verifies, (2) a valid signed revocation exists, and (3) the operation is signed by the active successor. A correct cryptographic signature from the retired key fails this **current authorization** gate.

A caller supplies an independently maintained `minRevocationSequence`. Once advanced to 1, any state missing the revocation is rejected as a rollback. As before, a local value ledger does not itself provide durable external monotonic storage; the guarantee depends on maintaining that floor separately.

## What is and is not proven

The QG-067 experiment is synthetic and uses disposable Ed25519 keys. It does not revoke real GitHub or 0root.ai credentials, does not authenticate genuine independent guardians, and does not access the public internet. It inherits the bounded assumptions of QG-062–066: the two owned surfaces share one source ancestry; external internet claims require their own access, provenance and ancestry gates.

The revocation certificate is an explicit model event, not real-time certificate revocation infrastructure, a deployed PKI, a transparency log or a time-stamped external witness. If the successor private key or the independently pinned policy is compromised, the model cannot by itself detect that. Historical signature validity is a mathematical statement about signed bytes and a key, not proof that the signed claim is factually true.

```sh
node --test tests/recovery-without-old-key.test.mjs tests/revocation-outlives-recovery.test.mjs
```
