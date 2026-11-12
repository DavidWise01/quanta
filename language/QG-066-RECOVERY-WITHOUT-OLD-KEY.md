# QG-066 — Recovery Without the Old Key

## Next invariant

**A lost or compromised signer must not force historical evidence to be erased, and the recovery authority must not be fabricated from the signer it replaces.**

```text
            HISTORICAL QG-065 CHAIN
                    |
             SEPARATELY PINNED
              RECOVERY POLICY
                    |
            NEW KEY RECOVERY
                 REQUEST
                    |
       +------------+------------+
       |            |            |
  GUARDIAN 0    GUARDIAN 1    GUARDIAN 2
   ROOT A         ROOT B        ROOT C
       |            |            |
       +------------+------------+
                    |
       VERIFY 3 INDEPENDENT ROOTS
                    |
        NEW KEY PROOF OF POSSESSION
                    |
             RECOVERY SEALED
                    |
       HISTORICAL KEY STILL VERIFIES
                    |
                 {{i}}
```

## Distinct recovery path

QG-065 normal rotation requires both the old and successor private keys. QG-066 intentionally uses a **different schema** (`QUANTA-QG-066-RECOVERY`), preventing emergency guardian approval from being misrepresented as an old-key signature.

The caller supplies an independently pinned policy with: the existing QG-065 chain pin; an allowlist of Ed25519 guardian verification keys with stable IDs and declared ancestral roots; `minRecoverySequence` for rejecting old recovery states; and `minRecoveredRevision` for recovered manifest validation. This policy is not taken from the recovery request.

The request binds the exact SHA-256 digest of the retained historical QG-065 chain, the retired active key fingerprint, the successor public JWK and fingerprint, sequence `1`, and an explicit lost/compromised-key reason. It requires at least three distinct pinned guardian keys whose **policy-pinned ancestry roots are distinct**. The successor must also sign the same canonical recovery request, proving possession of the corresponding new private key.

Only after verification is a separate `recovery` field appended by value. All previous QG-065 transitions and QG-064 signed historical manifests stay untouched. New manifest revisions may be signed with the recovered key and are replay-checked. Forged guardian signatures, duplicate guardian IDs, shared guardian roots, broken historical hashes, bad successor signatures, or a replay below the independently persisted recovery sequence floor are rejected.

## Security and governance limitations

- Pinned guardian ancestry is **declared by external policy**, not independently established by this synthetic kernel. Three real-world people or sites might secretly share control; this prototype cannot prove their independence.
- The experiment generates temporary Ed25519 keys. It does not possess real guardian credentials, and never touches live GitHub or 0root.ai permissions.
- Historical validity does not confer current authority on a retired/compromised key. Real implementations require secure, durable external storage for the genesis key, guardian policy, recovery floors, audit logs, revocations, and recovery dispute procedures.
- This is a **single recovery event** from a QG-065 history, not a generalized subsequent recovery or a replacement for production key management.
- No real external website policies are checked, and gated content stays private. Source admission and witness deduplication from QG-062–064 remain separate gates.

Run:
```sh
node --test tests/trust-anchor-rotation.test.mjs tests/recovery-without-old-key.test.mjs
```
