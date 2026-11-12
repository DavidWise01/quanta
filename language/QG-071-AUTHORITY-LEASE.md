# QG-071 — Authority Has a Lifetime

## Natural invariant

**A successful fresh challenge is not an indefinite permission grant.** QG-070 establishes a replay-resistant *modeled* rejoin. QG-071 adds a separate Ed25519 issuer-signed lease that binds the exact challenge digest, signed session fingerprint, agent identity, checkpoint, revocation floor, and an explicit finite validity interval.

```text
       QG-070 FRESH CHALLENGE VERIFIED
                     |
               LEASE ISSUER
                     |
         SIGNED [START, EXPIRY)
                     |
         TRUSTED MONOTONIC CLOCK
              /           \
           ACTIVE         EXPIRED
              |              |
         AUTHORIZE          DENY
              |              |
              +------+-------+
                     |
          NEW UNUSED CHALLENGE
                     |
              SIGN NEW LEASE
                     |
                   {{i}}
```

## Contract

A lease payload includes a sequential index, previous signed-lease hash, agent identity, consumed QG-070 challenge digest, exact rejoin SHA-256 digest, expected checkpoint digest and revocation floor, plus `issuedAt` and exclusive `expiresAt` integer logical ticks. The maximum duration is `MAX_TICKS=300`; zero, negative, fractional or excessive durations are rejected.

Verification always replays the QG-070 trust record and verifies the issuer's signature against an independently pinned public key. Authorization is accepted only when `issuedAt <= clock.tick < expiresAt`. The **clock** and `clock.floor` are supplied as trusted independent inputs, not provided by the agent or lease itself. A clock lower than its floor is rejected. No signed lease alone establishes trustworthy real time.

Renewal requires a *different*, independently verified QG-070 challenge with the same pinned identity and trust policy. A previously used challenge digest cannot be reused; older leases and their signatures remain in the value-appended sequence. To avoid overlapping leases in this finite demonstrator, new leases may be issued at or after the previous expiration and are linked by a hash of the previous signed lease. A signed old lease remains historically verifiable after expiration but grants no current operation authority.

## Boundaries

- These are **logical ticks**, not seconds or UTC. There is no real authenticated time authority, key vault, durable issuer, expiration service, or distributed synchronization in this demonstration.
- This finite experiment does not persist consumed challenges outside its value ledger. Attackers able to rewind the ledger and external clock floor can replay earlier states. Production requires an immutable issuer-side nonce/lease register, a trusted monotonic clock, strongly scoped operation permissions and revocation checks at every action.
- The model preserves the QG-062–070 trust boundaries: our GitHub and 0root.ai surfaces share one owned ancestry, public-internet sources have separate policy/provenance controls, and offline agents do not authorize their own trust.
- Signatures establish key continuity, not real-world factual truth, agency or publisher identity. No real GitHub permissions are modified.

Run:
```sh
node --test tests/hive-fresh-challenge.test.mjs tests/hive-authority-lease.test.mjs
```
