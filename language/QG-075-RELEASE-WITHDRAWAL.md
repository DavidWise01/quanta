# QG-075 — Release Can Be Withdrawn

## Invariant

**A signed release approval can lose current publication authority without its original evidence being rewritten, deleted, or made cryptographically invalid.** QG-075 wraps a fully replay-verified QG-074 approval ledger in an independent, append-by-value withdrawal ledger.

```text
             QG-074 APPROVED ARTIFACT
                       |
                 NEW RISK FOUND
                       |
              WITHDRAWAL PETITION
                       |
          +------------+------------+
          |            |            |
        ROOT A       ROOT B       ROOT C
          |            |            |
          +------------+------------+
                       |
                VALIDATE QUORUM
                       |
                 APPEND REVOCATION
                       |
             +---------+----------+
             |                    |
       PRIOR APPROVAL        NEW PUBLICATION
             |                    |
        PRESERVE BYTES           DENY
             |                    |
             +---------+----------+
                       |
                     {{i}}
```

## Signed withdrawal boundary

A separate **QG-075 withdrawal payload** binds an exactly approved release ID, the SHA-256 digest of that complete QG-074 release entry, its public artifact digest, destination `0root.ai`, exact QG-074 approval-history digest, monotonic withdrawal sequence, predecessor withdrawal hash and reason `risk_discovered`.

At least three signatures from distinct independently pinned reviewer IDs and distinct externally declared ancestry roots must verify using the **same** reviewer policy as the approved release. The subject cannot sign a withdrawal into existence by modifying a status flag. A duplicated reviewer, shared ancestry, wrong signature, changed release bytes, altered approval history, or forged sequence is rejected.

Once recorded, withdrawal affects **only future authorization**. The old approval and its provenance remain replay-verifiable. `authorizePublication()` must verify the entire release/withdrawal chain, reject withdrawn releases first, then enforce a currently valid QG-072 signed publication scope for active releases. Only callers of this QG-075 gate obtain the withdrawal guarantee: direct calls to the predecessor QG-074 helper bypass this additional policy and must be prohibited at the real enforcement perimeter.

An independent `minWithdrawalSequence` guards rollback to an earlier cryptographically valid but pre-withdrawal state **only if** this floor has been durably advanced and protected outside the untrusted ledger.

## Limitations

This is a **synthetic policy-and-signature laboratory**, not a live publication revocation service. It does not actually remove public material, notify consumers, erase downstream copies, identify real reviewers or scan an artifact for confidential information. Even a valid withdrawal cannot recall already published bytes. Every real publishing path would need to enforce the new withdrawal gate and trusted monotonic state.

Reviewers' ancestry roots and source classifications are externally pinned assertions; the simulation cannot prove real organizational independence or that a release was safe. No private GitHub or 0root.ai credentials are accessed, and no publication or deletion is performed.

Tests:
```sh
node --test tests/independent-declassification.test.mjs tests/release-withdrawal.test.mjs
```
