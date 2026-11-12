# QG-069 — Rejoining the Hive

## Invariant

**Reconnection is an opportunity to reestablish trust, not an automatic grant of authority.** An offline agent retains its evidence ledger, then must verify a separately pinned current checkpoint, the full QG-066 recovery and QG-067 successor-signed revocation chain, and the QG-068 minimum revocation floor before obtaining explicit reauthorization.

```text
           AGENT RETURNS FROM OFFLINE
                      |
              PRESERVE OLD LOGS
                      |
              SUPPLIED CHECKPOINT
                      |
           MATCH INDEPENDENT DIGEST
                      |
            VERIFY RECOVERY + REVOCATION
                      |
          +-----------+-----------+
          |                       |
        CURRENT                 STALE/INVALID
          |                       |
   VERIFIED BUT NOT ACTIVE      REJECT
          |
       EXPLICIT APPROVAL
          |
        REJOINED
          |
        {{i}}
```

## Contract

The state starts with an offline QG-068 agent packet and **caller-independent** `pin` and `checkpointDigest`. The agent can append labeled offline observations, but they never acquire authority. The reconnection checkpoint must be online, belong to the same agent ID, match the externally pinned SHA-256 digest and replay-verify as current against QG-068's independent revocation floor, QG-067 revocation signatures and QG-066 guardian recovery chain.

Passing the cryptographic checks only produces `verified-awaiting-authorization`. A **separate explicit** `authorize()` call generates a rejoin certificate referring to the verified checkpoint digest and trust floor, and changes the state to `rejoined`. Every event and retained observation is verified in order through the append-by-value event log. No evidence is erased or implicitly promoted.

## Security limits

This is not a real network synchronization protocol, trusted time source, hardware attestation, durable monotonic counter or proof that a remote agent cannot bypass the gate. An actual deployment must obtain the reference snapshot hash and revocation floor through an authenticated independent channel and bind freshness to a nonce/epoch or equivalent challenge; otherwise a once-current checkpoint may be replayed. Offline histories are retained as **untrusted observations**, not automatically treated as verified evidence.

The model does not interact with real GitHub, 0root.ai or the public internet. GitHub and 0root.ai remain two surfaces of one owned ancestry, and external sources must still pass the QG-062–064 provenance gates.

```sh
node --test tests/hive-revocation-floor.test.mjs tests/hive-rejoin.test.mjs
```
