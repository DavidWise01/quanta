# QG-076 — Withdrawal Must Reach Every Agent

## Invariant

**A withdrawn public artifact must not regain publication authority from an offline agent, a stale pre-withdrawal approval, or another cryptographically valid but outdated signed record.**

```text
                 QG-075 SIGNED WITHDRAWAL
                            |
             EXTERNAL SEQUENCE + HEAD PIN
                            |
             +--------------+--------------+
             |       |        |       |     |
           CURRENT STALE   OFFLINE  INVALID ALT HEAD
             |       |        |       |     |
          VERIFY    DENY     DENY     DENY  DENY
             |
         CHECK RELEASE
          /         \
      ACTIVE       WITHDRAWN
        |              |
     CHECK SCOPE      DENY
        |
       {{i}}
```

## Implementation

QG-076 uses the existing full QG-075 replay verifier. Each agent report supplies an ID, an `online` or `offline` connection status, and a complete local QG-075 approval-and-withdrawal snapshot. A caller must supply an **independent** QG-075 release/reviewer policy, `minWithdrawalSequence >= 1`, and the exact SHA-256 digest of the current trusted withdrawal ledger, `headDigest`. A snapshot cannot supply its own expected hash.

Online snapshots are categorized as `current` only when they verify all QG-074 original approvals and the signed QG-075 withdrawal chain, satisfy the independently pinned sequence floor, and match the exact pinned head digest. A correctly signed old pre-withdrawal state is `stale`; a divergent, otherwise valid post-withdrawal snapshot is also `stale`. An offline agent is denied regardless of cached information. Cryptographically malformed and tampered snapshots are `invalid`.

Publication is **a separate gate**: it replays all agent receipts against the external pin, requires the agent to be `current`, then calls QG-075's withdrawal-aware publisher, which rejects withdrawn artifacts and checks the active QG-072 signed publishing scope and QG-071 lease. In the fixture, `release-1` is withdrawn while `release-2` remains independently approved and active, demonstrating both deny and allow decisions under a current snapshot.

Each report and computed receipt is stored by value in a deterministic, replay-checked ledger, with duplicate identities rejected. The original QG-073 gated ancestry, QG-074 approval signatures, and QG-075 withdrawal records remain intact.

## Limits

- This implementation is a **synthetic policy simulator**, not a network propagation protocol or a security monitor installed on real agents. No live publication, removal, notification, synchronization or recall of already downloaded copies occurs.
- An independently pinned hash detects valid but divergent history, but it is only as authentic and fresh as the external head-distribution mechanism. The model does not build durable monotonic storage, trusted wall-clock time, quorum consensus or authenticated checkpoint distribution.
- Real publishing infrastructure must forbid calling older QG-074 or QG-075 helpers that bypass the **QG-076 current-head gate**. Otherwise a stale agent could still publish outside the modeled boundary.
- The reviewer ancestry identities and original confidentiality labels are pinned assertions, not externally verified real-world independence. GitHub and 0root.ai remain mirrors of one owned corpus but have separate confidentiality permissions; external sites have independent origins and access requirements.

Run:
```sh
node --test tests/release-withdrawal.test.mjs tests/hive-withdrawal-checkpoint.test.mjs
```
