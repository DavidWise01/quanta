# QG-068 — Revocation Across the Hive

## Invariant

**An agent must not gain new-operation authority from a locally valid but obsolete signing ledger.** Every agent snapshot must satisfy an independently pinned minimum revocation sequence as well as the QG-066 recovery and QG-067 successor-signed revocation checks.

```text
                 QG-067 REVOCATION
                        |
                    HIVE AGENTS
            +-----------+-----------+
            |       |       |       |
          FRESH   STALE  OFFLINE  INVALID
            |       |       |       |
          VERIFY   DENY    DENY    DENY
            |
     INDEPENDENT REVOCATION FLOOR
            |
      CURRENT SIGNER AUTHORITY
            |
          {{i}}
```

## The state transition

An agent report contains `agentId`, `connection` (`online` or `offline`) and a complete local QG-067 snapshot. Before the hive accepts an agent for new operations, its snapshot is replay-verified with the complete QG-066 guardian recovery and QG-067 revocation lineage. Verification uses a **separately supplied** policy and a monotonic `minRevocationSequence >= 1`.

An online agent holding the signed revocation and matching the pinned key lineage is classified `current`, while an internally valid pre-revocation snapshot is `stale` and denied. An offline agent is denied even if its cached snapshot appears current, since it cannot establish freshness to the shared trust floor. A malformed or tampered snapshot is `invalid` and denied. Snapshot digests, classifications, and counts are preserved in a replay-checked, append-by-value ledger, with a separate explicit `authorizeAgent()` gate.

A synthetic four-agent example covers all four classifications. Historical QG-065 signatures remain verifiable; a revoked key still cannot authorize new QG-067 operations. Identical IDs cannot enroll as separate agents.

## Boundaries

- **No network synchronization is implemented.** A real offline agent that can execute local operations without consulting the current revocation floor is not protected merely by publishing a new record; production consumers must fail closed or use verified, fresh authorization receipts.
- This version has one revoked recovery epoch (`minRevocationSequence = 1`) and does not provide arbitrary multi-generation revocation consensus, external durable floors, real-time clock validity, remote attestation or proof that a local agent cannot bypass a caller's gate.
- The independently pinned floor and recovery guardian registry are trusted inputs, not facts proved by the agent's snapshot. The simulation does not operate real GitHub, 0root.ai or public-internet credentials.
- GitHub and 0root.ai remain two surfaces of one owned corpus. Internet-derived evidence still follows the QG-062–064 policy, lineage and trust-anchor gates.

```sh
node --test tests/revocation-outlives-recovery.test.mjs tests/hive-revocation-floor.test.mjs
```
