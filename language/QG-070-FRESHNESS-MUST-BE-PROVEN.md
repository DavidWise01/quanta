# QG-070 — Freshness Must Be Proven

## Invariant

**A proof that was valid for a prior authorization attempt must not authorize another attempt.** QG-069 confirms the complete trust checkpoint and revocation floor, but cannot alone distinguish a previously current replay. QG-070 adds a separately trusted challenge issuer, a one-use unpredictable nonce and an agent-key-signed reply bound to that exact issued challenge.

```text
           QG-069 VERIFIED RECONNECT
                     |
             ISSUE RANDOM NONCE
                     |
            ISSUER SIGNS CHALLENGE
                     |
        AGENT SIGNS BOUND RESPONSE
                     |
           VERIFY PINNED KEYS
                     |
         AGENT ID / CHECKPOINT / FLOOR
                     |
            +--------+--------+
            |                 |
         CURRENT            REPLAYED
            |                 |
      CONSUME ONCE           REJECT
            |
      EXPLICIT REJOIN APPROVAL
            |
           {{i}}
```

## Engineering rule

The verifier receives *independently pinned* QG-069 trust policy, agent identity and Ed25519 public key, issuer Ed25519 public key, expected SHA-256 checkpoint digest and a `minChallengeSequence` floor. The QG-069 record must already be `verified-awaiting-authorization`—it cannot be preauthorized. The issuer generates 32 cryptographically random bytes with `crypto.getRandomValues`, records their lowercase hexadecimal encoding, and signs a canonical JSON challenge including `agentId`, nonce, challenge sequence, complete rejoin digest, checkpoint digest and required revocation floor.

The agent response signs a separate payload containing the exact **issuer-signed challenge digest**, agent identity, checkpoint digest and revocation floor. Verification uses the separately pinned agent key, not a public key chosen by the response. A successful response is consumed **once** in the value-appended ledger; only a separate `authorize()` call runs the QG-069 explicit rejoin transition.

A response from an earlier challenge fails because the digest is different, even when every other trust parameter stays the same. Signature and challenge mutations, the wrong agent key, substituted issuer key, different checkpoint, insufficient independently pinned challenge floor, and duplicate consumes are rejected.

## Boundaries

This is a **single-session synthetic protocol**: no actual remote agent authentication, challenge delivery, trusted time, nonce storage, live key vault, or network is implemented. It verifies freshness relative to the modeled challenge state, not against an externally authenticated wall clock. An adversary that can rewind the entire local ledger and independent trust-floor state may replay a previously accepted challenge. Production use requires an authenticated issuer, nonces tracked in server-side durable consume-once storage, replay-resistant challenges tied to sessions, and expiration or a trusted challenge epoch. The `minChallengeSequence` is caller-controlled and not itself a persistent monotonic counter.

GitHub and 0root.ai remain two owned surfaces of one information ancestry; external internet evidence remains subject to QG-062–064 policy, origin and trust-anchor gates. This lab does not communicate with, grant permissions to, or synchronize live agents.

Test:
```sh
node --test tests/hive-rejoin.test.mjs tests/hive-fresh-challenge.test.mjs
```
